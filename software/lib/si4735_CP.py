import time
from struct import pack, unpack
from micropython import const

from radarcplatform import RADARCi2cdev, setpin

SI473X_ADDR_SEN_LOW = const(0x11)  # SI473X I2C bus address when the SEN pin (16) is set to low 0V.
SI473X_ADDR_SEN_HIGH = const(0x63) # SI473X I2C bus address when the SEN pin (16) is set to high +3.3V

POWER_UP = const(0x01)       # Power up device and mode selection.
GET_REV = const(b"\x10")        # Returns revision information on the device.
POWER_DOWN = const(b"\x11")     # Power down device.
SET_PROPERTY = const(0x12)   # Sets the value of a property.
GET_PROPERTY = const(0x13)   # Retrieves a property’s value.
GET_INT_STATUS = const(0x14) # Read interrupt status bits.

MAX_DELAY_AFTER_SET_FREQUENCY = const(0.030) # In ms - This value helps to improve the precision during of getting frequency value
MAX_DELAY_AFTER_POWERUP = const(0.010)       # In ms - Max delay you have to setup after a power up command.
MIN_DELAY_WAIT_SEND_LOOP = const(300)     # In uS (Microsecond) - each loop of waitToSend sould wait this value in microsecond
MAX_SEEK_TIME = const(8000)               # defines the maximum seeking time 8s is default.

FM_TUNE_FREQ = const(0x20)
AM_TUNE_FREQ = const(0x40)
NBFM_TUNE_FREQ = const(0x50)

# Parameters
SI473X_RDS_OUTPUT_ONLY = const(0b00000000)      # RDS output only (no audio outputs) Si4749 only
SI473X_ANALOG_AUDIO =const(0b00000101)         # Analog Audio output
SI473X_DIGITAL_AUDIO1 =const(0b00001011)       # Digital audio output (DCLK, LOUT/DFS, ROUT/DIO)
SI473X_DIGITAL_AUDIO2 =const(0b10110000)       # Digital audio output (DCLK, DFS, DIO)
SI473X_ANALOG_DIGITAL_AUDIO =const(0b10110101) # Analog and digital audio outputs (LOUT/ROUT and DCLK, DFS,DIO)

XOSCEN_CRYSTAL =const(1) # Use crystal oscillator
XOSCEN_RCLK =const(0)    # Use external RCLK (crystal oscillator disabled).

FM_CURRENT_MODE = const(0)
AM_CURRENT_MODE = const(1)
SSB_CURRENT_MODE = const(2)
NBFM_CURRENT_MODE = const(3)

SSB_SIDEBAND_LSB = 1
SSB_SIDEBAND_USB = 2

DEFAULT_CURRENT_AVC_AM_MAX_GAIN = const(36)

AM_AUTOMATIC_VOLUME_CONTROL_MAX_GAIN = const(0x3103)
SSB_MODE = const(0x0101)

AM_RSQ_STATUS = const(0x43)  # Queries the status of the Received Signal Quality (RSQ) for the current channel.
FM_RSQ_STATUS = const(0x23)
SSB_RSQ_STATUS = const(0x43)
NBFM_RSQ_STATUS = const(0x53)

FM_RDS_STATUS = const(0x24)
FM_RDS_CONFIG = const(0x1502)

RX_VOLUME = const(0x4000)

class Si47xProperty:
    def __init__(self):
        self.raw = {'byteLow': 0, 'byteHigh': 0}
        self.value = 0

    def set_value(self, value):
        self.value = value
        self.raw['byteLow'], self.raw['byteHigh'] = unpack('BB', pack('H', value))

    def get_value(self):
        return self.value

class Si47xPowerup:
    def __init__(self):
        # Initialize the fields of the structure
        self.func = 0  # Function (0 = FM Receive; 1–14 = Reserved; 15 = Query Library ID)
        self.xoscen = 0  # Crystal Oscillator Enable (0 = crystal oscillator disabled; 1 = Use crystal oscillator and OPMODE=ANALOG AUDIO)
        self.patch = 0  # Patch Enable (0 = Boot normally; 1 = Copy non-volatile memory to RAM)
        self.gpo2oen = 0  # GPO2 Output Enable (0 = GPO2 output disabled; 1 = GPO2 output enabled)
        self.ctsien = 0  # CTS Interrupt Enable (0 = CTS interrupt disabled; 1 = CTS interrupt enabled)
        self.opmode = 0  # Application Setting. See page 65

    def setPowerUp(self, ctsien, gpo2oen, patch, xoscen, func, opmode):

        self.func = func  # Function (0 = FM Receive; 1–14 = Reserved; 15 = Query Library ID)
        self.xoscen = xoscen  # Crystal Oscillator Enable (0 = crystal oscillator disabled; 1 = Use crystal oscillator and OPMODE=ANALOG AUDIO)
        self.patch = patch  # Patch Enable (0 = Boot normally; 1 = Copy non-volatile memory to RAM)
        self.gpo2oen = gpo2oen  # GPO2 Output Enable (0 = GPO2 output disabled; 1 = GPO2 output enabled)
        self.ctsien = ctsien  # CTS Interrupt Enable (0 = CTS interrupt disabled; 1 = CTS interrupt enabled)
        self.opmode = opmode  # Application Setting. See page 65

    def get_raw(self):
        """ Convert the structured data to raw byte representation """
        return bytearray([self.func | (self.xoscen << 4) | (self.patch << 5) | (self.gpo2oen << 6) | (self.ctsien << 7), self.opmode])


class Si47xSetFrequency:

    def __init__(self):
        self.fast_tuning = 0  # ARG1 - FAST Tuning. If set, executes fast and invalidated tune. The tune status will not be accurate.
        self.freeze = 0       # Valid only for FM (Must be 0 to AM)
        self.dummy1 = 0       # Always set 0
        self.usblsb_selection = 0  # SSB Upper Side Band (USB) and Lower Side Band (LSB) Selection.
        self.tune_frequency_high_byte = 0  # ARG2 - Tune Frequency High byte.
        self.tune_frequency_low_byte = 0   # ARG3 - Tune Frequency Low byte.
        self.antenna_tuning_capacitor_high_byte = 0  # ARG4 - Antenna Tuning Capacitor High byte.
        self.antenna_tuning_capacitor_low_byte = 0   # ARG5 - Antenna Tuning Capacitor Low byte. Note used for FM.
        #self.raw_data = bytearray(5)

    def __repr__(self):
        return f"""Si47xSetFrequency(Fast tuning={self.fast_tuning}, Freeze={self.freeze}, 
        usblsb={self.usblsb_selection}, FrequencyHighByte = {self.tune_frequency_high_byte}, FrequencyLowByte = {self.tune_frequency_low_byte}, 
        TuningCapacitorHighByte = {self.antenna_tuning_capacitor_high_byte}, TuningCapacitorLowByte = {self.antenna_tuning_capacitor_low_byte})"""

    def setFrequency(self,fast_tuning,freeze,usblsb_selection,tune_frequency_high_byte,tune_frequency_low_byte,antenna_tuning_capacitor_high_byte,antenna_tuning_capacitor_low_byte):
        self.fast_tuning = fast_tuning
        self.freeze = freeze
        self.dummy1 = 0
        self.usblsb_selection = usblsb_selection
        self.tune_frequency_high_byte = tune_frequency_high_byte
        self.tune_frequency_low_byte = tune_frequency_low_byte
        self.antenna_tuning_capacitor_high_byte = antenna_tuning_capacitor_high_byte
        self.antenna_tuning_capacitor_low_byte = antenna_tuning_capacitor_low_byte
    def get_raw(self):
        """ Convert the structured data to raw byte representation """
        return bytearray([
            (self.fast_tuning << 7) | (self.freeze << 6) | (self.dummy1 << 2) | self.usblsb_selection,
            self.tune_frequency_high_byte,
            self.tune_frequency_low_byte,
            self.antenna_tuning_capacitor_high_byte,
            self.antenna_tuning_capacitor_low_byte
        ])


class Si47xFirmwareInformation:
    def __init__(self):
        # status ("RESP0")
        self.stc_int = 0  # Status interrupt
        self.dummy1 = 0
        self.rds_int = 0
        self.rsq_int = 0
        self.dummy2 = 0  # Dummy bits
        self.err = 0  # Error flag
        self.cts = 0  # Clear to send flag
        self.part_number = 0  # RESP1 - Final 2 digits of Part Number (HEX)
        self.firmware_major = 0  # RESP2 - Firmware Major Revision (ASCII)
        self.firmware_minor = 0  # RESP3 - Firmware Minor Revision (ASCII)
        self.patch_id_high = 0  # RESP4 - Patch ID High byte (HEX)
        self.patch_id_low = 0  # RESP5 - Patch ID Low byte (HEX)
        self.component_major = 0  # RESP6 - Component Major Revision (ASCII)
        self.component_minor = 0  # RESP7 - Component Minor Revision (ASCII)
        self.chip_revision = 0  # RESP8 - Chip Revision (ASCII)
        # RESP9 to RESP15 not used

    def get_raw(self):
        """ Convert the structured data to raw byte representation """
        return bytearray([
            self.stc_int | (self.dummy1 << 1) | (self.rds_int << 2) |
            (self.rsq_int << 3) | (self.dummy2 << 4) | (self.err << 6) | (self.cts << 7),
            self.part_number,
            self.firmware_major,
            self.firmware_minor,
            self.patch_id_high,
            self.patch_id_low,
            self.component_major,
            self.component_minor,
            self.chip_revision
        ])


class Si47xSsbMode:
    def __init__(self):
        self.audio_bandwidth = 0  # 0 = 1.2kHz (default); 1=2.2kHz; 2=3kHz; 3=4kHz; 4=500Hz; 5=1kHz
        self.ss_cutoff_filter = 0  # SSB side band cutoff filter for band pass and low pass filter
        self.avc_divider = 0  # set 0 for SSB mode; set 3 for SYNC mode;
        self.avc_enabled = 0  # SSB Automatic Volume Control (AVC) enable; 0=disable; 1=enable (default);
        self.soft_mute_selection = 0  # SSB Soft-mute Based on RSSI or SNR
        self.dummy1 = 0  # Always write 0;
        self.dsp_afc_disabled = 0  # 0=SYNC MODE, AFC enable; 1=SSB MODE, AFC disable.

    def setSsbMode(self,audio_bandwidth,ss_cutoff_filter,avc_divider,avc_enabled,soft_mute_selection,dsp_afc_disabled):
        self.audio_bandwidth = audio_bandwidth  # 0 = 1.2kHz (default); 1=2.2kHz; 2=3kHz; 3=4kHz; 4=500Hz; 5=1kHz
        self.ss_cutoff_filter = ss_cutoff_filter  # SSB side band cutoff filter for band pass and low pass filter
        self.avc_divider = avc_divider  # set 0 for SSB mode; set 3 for SYNC mode;
        self.avc_enabled = avc_enabled # SSB Automatic Volume Control (AVC) enable; 0=disable; 1=enable (default);
        self.soft_mute_selection = soft_mute_selection  # SSB Soft-mute Based on RSSI or SNR
        self.dummy1 = 0  # Always write 0;
        self.dsp_afc_disabled = dsp_afc_disabled  # 0=SYNC MODE, AFC enable; 1=SSB MODE, AFC disable.

    def get_raw(self):
        """ Convert the structured data to raw byte representation """
        return [(self.audio_bandwidth & 0x0F) | \
                     ((self.ss_cutoff_filter & 0x0F) << 4),
                     (self.avc_divider & 0x0F) | \
                     ((self.avc_enabled & 0x01) << 4) | \
                     ((self.soft_mute_selection & 0x01) << 5) | \
                     ((self.dummy1 & 0x01) << 6) | \
                     ((self.dsp_afc_disabled & 0x01) << 7)]


class SI47xRDSCommand:
    def __init__(self):
        self.INTACK = 0        # Interrupt Acknowledge; 0 = RDSINT status preserved; 1 = Clears RDSINT.
        self.MTFIFO = 0        # Empty FIFO; 0 = If FIFO not empty; 1 = Clear RDS Receive FIFO.
        self.STATUSONLY = 0    # Determines if data should be removed from the RDS FIFO.

    def set_intack(self, value):
        self.INTACK = value

    def set_mtfifo(self, value):
        self.MTFIFO = value

    def set_statusonly(self, value):
        self.STATUSONLY = value

    def get_raw(self):
        """ Convert the structured data to raw byte representation """
        return (self.INTACK & 0x01) | ((self.MTFIFO & 0x01) << 1) | ((self.STATUSONLY & 0x01) << 2)


class Si47xRdsConfig:
    def __init__(self):
        self.rds_processing_enable = 0  # RDS Processing Enable (1 bit)
        self.dummy1 = 0                  # Dummy bits (7 bits)
        self.block_error_threshold_d = 0 # Block Error Threshold BLOCKD (2 bits)
        self.block_error_threshold_c = 0 # Block Error Threshold BLOCKC (2 bits)
        self.block_error_threshold_b = 0 # Block Error Threshold BLOCKB (2 bits)
        self.block_error_threshold_a = 0 # Block Error Threshold BLOCKA (2 bits)

    def get_raw(self):
        """ Convert the structured data to raw byte representation """
        return [(self.rds_processing_enable & 0x01) | \
                        ((self.dummy1 & 0x7F) << 1),
                        ((self.block_error_threshold_d & 0x03)) | \
                        ((self.block_error_threshold_c & 0x03) << 2) | \
                        ((self.block_error_threshold_b & 0x03) << 4) | \
                        ((self.block_error_threshold_a & 0x03) << 6)]


class Si47xRdsStatus:
    def __init__(self):
        self.STCINT = 0  
        self.DUMMY1 = 0                  # Dummy bits (1 bit)
        self.RDSINT = 0
        self.RSQINT = 0
        self.DUMMY2 = 0 #(2 bits)
        self.ERR = 0
        self.CTS = 0          

        self.RDSRECV = 0
        self.RDSSYNCLOST = 0
        self.RDSSYNCFOUND = 0
        self.DUMMY3 = 0
        self.RDSNEWBLOCKA = 0
        self.RDSNEWBLOCKB = 0
        self.DUMMY4 = 0 #(2 bits)

        self.RDSSYNC = 0
        self.DUMMY5 = 0
        self.GRPLOST = 0
        self.DUMMY6 = 0

        self.RDSFIFOUSED = 0 #(8 bits)

        self.BLOCKAH = 0 #(8 bits)

        self.BLOCKAL = 0 #(8 bits)

        self.BLOCKBH = 0 #(8 bits)

        self.BLOCKBL = 0 #(8 bits)

        self.BLOCKCH = 0 #(8 bits)

        self.BLOCKCL = 0 #(8 bits)

        self.BLOCKDH = 0 #(8 bits)

        self.BLOCKDL = 0 #(8 bits)

        self.BLED = 0 #(2 bits)
        self.BLEC = 0 #(2 bits)
        self.BLEB = 0 #(2 bits)
        self.BLEA = 0 #(2 bits)

        #Storage of byte blocks

        self.BLOCKA = 0
        self.BLOCKB = 0
        self.BLOCKC = 0
        self.BLOCKD = 0

        self.BLOCKA_REFINED = 0

        self.raw = bytearray(13)

    def from_raw(self):
        # Convert the raw byte representation back to structured data

        self.RDSRECV = self.raw[1] & 0x01
        self.RDSSYNCLOST = (self.raw[1] >> 1) & 0x01
        self.RDSSYNCFOUND = (self.raw[1] >> 2) & 0x01
        self.RDSNEWBLOCKA = (self.raw[1] >> 3) & 0x01
        self.RDSNEWBLOCKB = (self.raw[1] >> 4) & 0x01


        self.RDSSYNC =  self.raw[2] & 0x01
        self.GRPLOST = (self.raw[2] >> 2) & 0x01

        self.RDSFIFOUSED = self.raw[3]

        self.BLOCKAH = self.raw[4]
        
        self.BLOCKAL = self.raw[5]

        self.BLOCKBH = self.raw[6]

        self.BLOCKBL = self.raw[7]

        self.BLOCKCH = self.raw[8]

        self.BLOCKCL = self.raw[9]

        self.BLOCKDH = self.raw[10]

        self.BLOCKDL = self.raw[11]

        self.BLED = self.raw[12] & 0x03
        self.BLEC = (self.raw[12]) >> 2 & 0x03
        self.BLEB = (self.raw[12]) >> 4 & 0x03
        self.BLEA = (self.raw[12]) >> 6 & 0x03

        self.BLOCKA = (self.BLOCKAH << 8) + self.BLOCKAL
        self.BLOCKB = (self.BLOCKBH << 8) + self.BLOCKBL
        self.BLOCKC = (self.BLOCKCH << 8) + self.BLOCKCL
        self.BLOCKD = (self.BLOCKDH << 8) + self.BLOCKDL


        self.BLOCKB_REFINED = {"content": self.BLOCKB & 0x0F,
                    "textABFlag": (self.BLOCKB >> 4) & 0x01,
                    "programType": (self.BLOCKB >> 5) & 0x1F,
                    "trafficProgramCode": (self.BLOCKB >> 10) & 0x01,
                    "versionCode": (self.BLOCKB >> 11) & 0x01,
                    "groupType": (self.BLOCKB >> 12) & 0x0F}

        self.BLOCKB_GROUP0 = {"address": self.BLOCKB & 0x03,
                    "DI": (self.BLOCKB >> 2) & 0x01,
                    "MS": (self.BLOCKB >> 3) & 0x01,
                    "TA": (self.BLOCKB >> 4) & 0x01,
                    "programType": (self.BLOCKB >> 5) & 0x1F,
                    "trafficProgramCode": (self.BLOCKB >> 10) & 0x01,
                    "versionCode": (self.BLOCKB >> 11) & 0x01,
                    "groupType": (self.BLOCKB >> 12) & 0x0F}

        self.BLOCKB_GROUP2 = {"address": self.BLOCKB & 0x0F,
                    "textABFlag": (self.BLOCKB >> 4) & 0x01,
                    "programType": (self.BLOCKB >> 5) & 0x1F,
                    "trafficProgramCode": (self.BLOCKB >> 10) & 0x01,
                    "versionCode": (self.BLOCKB >> 11) & 0x01,
                    "groupType": (self.BLOCKB >> 12) & 0x0F}



class SI4735:
    def __init__(self, i2c, device_i2c_address, reset_pin):
        """ i2c and reset_pin are CircuitPython or MicroPython objects """

        assert device_i2c_address in [SI473X_ADDR_SEN_LOW, SI473X_ADDR_SEN_HIGH]

        # stash parameters
        self.device_address = device_i2c_address
        self.i2c = i2c
        self.reset_pin = reset_pin

        # TODO get rid of self.i2c? what right do we have to go messing
        # with other devices??
        self.si4735_i2c = RADARCi2cdev(self.i2c, self.device_address)

        # 1 = LSB and 2 = USB; 0 = AM, FM or WB
        self.currentSsbStatus = 0
        self.currentTune = FM_TUNE_FREQ
        self.currentClockType = XOSCEN_CRYSTAL
        self.currentMode = FM_CURRENT_MODE
        self.currentAvcAmMaxGain = DEFAULT_CURRENT_AVC_AM_MAX_GAIN
        self.lastMode = FM_CURRENT_MODE

        self.powerUp = Si47xPowerup()
        self.ssbMode = Si47xSsbMode()
        self.frequencyData = Si47xSetFrequency()
        self.rdsStatus = Si47xRdsStatus()

        self.station_name = " " * 8
        self.station_text = " " * 64

        self.rdsLastABFlag = 0

        self.frequency = 0.0 #current frequency
        self.volume = 30 #current volume

    def getFrequency(self):
        return self.frequency

    def getVolume(self):
        return self.volume

    def getMode(self):
        return self.currentMode

    def getSSBbandwidth(self):
        return self.ssbMode.audio_bandwidth

    def getSSBsideband(self):
        return self.currentSsbStatus


    def reset(self):
        print("Reset")
        pin_level_delay = 0.010

        time.sleep(pin_level_delay)
        setpin(self.reset_pin, 0)

        time.sleep(pin_level_delay)
        setpin(self.reset_pin, 1)

        time.sleep(pin_level_delay)
    
    def get_device_i2c_address(self):
        return self.device_address

    def waitToSend(self):
        while True:
            #print("loop.")
            time.sleep(MIN_DELAY_WAIT_SEND_LOOP/1_000_000)

            out = self.si4735_i2c.readfrom(1)

            if out[0] & 0B10000000:
                break

    def sendProperty(self, propertyNumber, parameter):

        Property = Si47xProperty()
        Param = Si47xProperty()

        Property.set_value(propertyNumber)
        Param.set_value(parameter)

        self.waitToSend()
        self.si4735_i2c.writeto(bytearray((SET_PROPERTY,0,Property.raw['byteHigh'],Property.raw['byteLow'],Param.raw['byteHigh'],Param.raw['byteLow'])))
        self.waitToSend()
        time.sleep(550/1_000_000)
        print("Send property")

    def setAvcAmMaxGain(self,gain):
        self.sendProperty(AM_AUTOMATIC_VOLUME_CONTROL_MAX_GAIN, gain * 340)
        self.currentAvcAmMaxGain = gain

    def radioPowerUp(self):
        self.waitToSend()
        self.si4735_i2c.writeto(bytearray((POWER_UP,self.powerUp.get_raw()[0],self.powerUp.get_raw()[1])))
        self.waitToSend()
        time.sleep(MAX_DELAY_AFTER_POWERUP)
        print("Powerup")

    def getFirmware(self):
        self.waitToSend()

        self.si4735_i2c.writeto(GET_REV)

        self.waitToSend()

        firmware = self.si4735_i2c.readfrom(9)

        print(", ".join(hex(b) for b in firmware))

        outdata = {"partnumber": hex(firmware[1]),
                   "firmware": chr(firmware[2]) + "." + chr(firmware[3]),
                   "patchid": hex((firmware[4] << 8) | firmware[5]),
                   "component": chr(firmware[6]) + "." +chr(firmware[7]),
                   "chiprevision": chr(firmware[8])}

        print(outdata)
        return outdata

    def setFrequency(self,frequency):
        print("setFrequency")
        self.waitToSend()

        if self.currentTune == FM_TUNE_FREQ:
            freeze = 1
        else:
            freeze = 0

        self.frequency = frequency

        #ba = bytearray(struct.pack("h", frequency))
        freq = frequency.to_bytes(2,'little')
        #print(struct.unpack("b",ba))
        #print(freq[0])
        #print(freq[1])
        if self.currentSsbStatus != 0:
            self.frequencyData.setFrequency(1,0,self.currentSsbStatus,freq[1],freq[0],0,0)
            print("FrequencySSB")
        else:
            self.frequencyData.setFrequency(0,freeze,0,freq[1],freq[0],0,0)
            print("FrequencyNonSSB")

        print(repr(self.frequencyData))

        if self.currentTune == AM_TUNE_FREQ:

            barray =bytearray((self.currentTune,
                               self.frequencyData.get_raw()[0],
                               self.frequencyData.get_raw()[1],
                               self.frequencyData.get_raw()[2],
                               self.frequencyData.get_raw()[3],
                               self.frequencyData.get_raw()[4]))
            print("AM")
        else:

            barray =bytearray((self.currentTune,
                               self.frequencyData.get_raw()[0],
                               self.frequencyData.get_raw()[1],
                               self.frequencyData.get_raw()[2],
                               self.frequencyData.get_raw()[3]))
            print("FM")


        #print(barray)
        self.si4735_i2c.writeto(barray)
        time.sleep(MAX_DELAY_AFTER_SET_FREQUENCY)
        print("setFrequencyEnd")
        print(self.currentTune)



    def downloadPatch(self):

        with open('patch.csg', mode="rt") as f:
            line = f.readline()
            while line:
                if not line.startswith("#"):
                    chunkstrlist = line.strip().split(',')
                    #print(chunkstrlist)

                    chunk = [int(item, 0) for item in chunkstrlist]
                    #print(chunk)
                    self.si4735_i2c.writeto(bytearray(chunk))
                line = f.readline()
                time.sleep(MIN_DELAY_WAIT_SEND_LOOP/1_000_000)
            print("Download patch")

    def patchPowerUp(self):
        self.waitToSend()
        self.powerUp.setPowerUp(1,0,1,self.currentClockType,0,SI473X_ANALOG_AUDIO)
        self.waitToSend()
        print(self.si4735_i2c.writeto(bytearray((POWER_UP,self.powerUp.get_raw()[0],self.powerUp.get_raw()[1]))))
        self.waitToSend()
        time.sleep(MAX_DELAY_AFTER_POWERUP)
        print("Patch power up")

    def setSSB(self,usblsb):
        self.currentMode = SSB_CURRENT_MODE
        # No power down here as patch is volatile memory needs to be preserved
        self.powerUp.setPowerUp(1,0,0,self.currentClockType,self.currentMode,SI473X_ANALOG_AUDIO)
        self.radioPowerUp()
        print("Set SSB")
        self.currentTune = AM_TUNE_FREQ
        self.currentSsbStatus = usblsb
        self.lastMode = SSB_CURRENT_MODE

    def setAM(self):
        self.currentMode = AM_CURRENT_MODE
        self.powerDown()
        self.powerUp.setPowerUp(1,0,0,self.currentClockType,self.currentMode,SI473X_ANALOG_AUDIO)
        self.radioPowerUp()
        self.setAvcAmMaxGain(self.currentAvcAmMaxGain)
        print("Set AM")
        self.currentTune = AM_TUNE_FREQ
        self.currentSsbStatus = 0
        self.lastMode = AM_CURRENT_MODE

    def disableFMDebug(self):
        barray = bytearray((0x12,0x0,0xff,0x0,0x0,0x0))
        self.si4735_i2c.writeto(barray)
        time.sleep(2500/1_000_000)
        print("Disable FM debug")

    def setFM(self):
        self.powerDown()
        self.currentMode = FM_CURRENT_MODE
        self.powerUp.setPowerUp(1,0,0,self.currentClockType,self.currentMode,SI473X_ANALOG_DIGITAL_AUDIO)
        
        self.radioPowerUp()
        print("Set FM")
        self.currentTune = FM_TUNE_FREQ
        self.currentSsbStatus = 0
        self.lastMode = FM_CURRENT_MODE
        self.disableFMDebug()

    def powerDown(self):
        self.waitToSend()
        self.si4735_i2c.writeto(POWER_DOWN)
        self.waitToSend()
        time.sleep(2500/1_000_000)
        print("Power down")

    def sendSSBModeProperty(self):
        Property = Si47xProperty()
        Property.set_value(SSB_MODE)
        #self.ssbMode.raw()
        self.waitToSend()
        print(SET_PROPERTY)
        print(Property.raw['byteHigh'])
        print(Property.raw['byteLow'])
        print(self.ssbMode.get_raw()[1])
        print(self.ssbMode.get_raw()[0])
        print(self.ssbMode.get_raw())
        barray = bytearray((SET_PROPERTY, 0, Property.raw['byteHigh'], Property.raw['byteLow'], self.ssbMode.get_raw()[1], self.ssbMode.get_raw()[0]))
        print(barray)
        print(self.si4735_i2c.writeto(barray))
        self.waitToSend()
        time.sleep(MAX_DELAY_AFTER_POWERUP)
        print("send SSB Mode")

    def setSSBAudioBandwidth(self,AUDIOBW):
        self.ssbMode.audio_bandwidth = AUDIOBW
        self.sendSSBModeProperty()

    def setSSBAutomaticVolumeControl(self,AVCEN):
        self.ssbMode.avc_enabled = AVCEN
        self.sendSSBModeProperty()

    def setSSBConfig(self,audio_bandwidth,ss_cutoff_filter,avc_divider,avc_enabled,soft_mute_selection,dsp_afc_disabled):
        self.ssbMode.setSsbMode(audio_bandwidth,ss_cutoff_filter,avc_divider,avc_enabled,soft_mute_selection,dsp_afc_disabled)
        self.sendSSBModeProperty()

    def getCurrentReceivedSignalQuality(self,INTACK):
   
        if self.currentTune == FM_TUNE_FREQ:
            # FM TUNE
            cmd = FM_RSQ_STATUS
            sizeResponse = 8
        elif self.currentTune == NBFM_TUNE_FREQ:
            cmd = NBFM_RSQ_STATUS
            sizeResponse = 8
        else:
            # AM TUNE
            cmd = AM_RSQ_STATUS
            sizeResponse = 6

        self.waitToSend()

        arg = INTACK
        barray = bytearray((cmd,arg))
        #print(barray)
        self.si4735_i2c.writeto(barray)
        self.waitToSend()
        signal = self.si4735_i2c.readfrom(sizeResponse)
        #print(", ".join(hex(b) for b in signal))
        print("getCurrentReceivedSignalQuality")

        if sizeResponse == 8:
            outdata = {"rssi": signal[4],"SNR": signal[5]}
        else:
            outdata = {"rssi": signal[4],"SNR": signal[5]}

        print(outdata)

        return outdata

    def getRDSStatus(self,INTACK,MTFIFO,STATUSONLY):
        if self.currentTune != FM_TUNE_FREQ:
            return

        rds_cmd = SI47xRDSCommand()
        rds_cmd.INTACK = INTACK
        rds_cmd.MTFIFO = MTFIFO
        rds_cmd.STATUSONLY = STATUSONLY
        #rds_cmd.update_raw()

        self.waitToSend()
        barray = bytearray((FM_RDS_STATUS,rds_cmd.get_raw()))
        print(", ".join(hex(b) for b in barray))
        self.si4735_i2c.writeto(barray)
        self.waitToSend()
        rds = self.si4735_i2c.readfrom(13)
        print(", ".join(hex(b) for b in rds))
        print("getRDSStatus")
        self.rdsStatus.raw = rds
        self.rdsStatus.from_raw()
#         print(self.rdsStatus.RDSRECV)
#         print(self.rdsStatus.RDSFIFOUSED)
#         print(self.rdsStatus.BLOCKA)
#         print(self.rdsStatus.BLOCKB_REFINED)
#         print(self.rdsStatus.BLOCKB_GROUP0)
#         print(self.rdsStatus.BLOCKDL)
#         print(self.rdsStatus.BLOCKDH)
#         print(chr(self.rdsStatus.BLOCKDL))
#         print(chr(self.rdsStatus.BLOCKDH))
#         
#         print(self.rdsStatus.BLOCKB_GROUP0["address"])
        if self.rdsStatus.RDSRECV == 1:

            print("valid rds")
            print("Group 0")
            print(self.rdsStatus.BLOCKB_GROUP0)

            if self.rdsStatus.BLOCKB_GROUP0["groupType"] == 0:
                if self.rdsLastABFlag != self.rdsStatus.BLOCKB_REFINED["textABFlag"]:
                    self.rdsLastABFlag = self.rdsStatus.BLOCKB_REFINED["textABFlag"]
                    self.station_name = " " * 8

                self.station_name = list(self.station_name)

                self.station_name[self.rdsStatus.BLOCKB_GROUP0["address"]*2] = chr(self.rdsStatus.BLOCKDH)
                self.station_name[(self.rdsStatus.BLOCKB_GROUP0["address"]*2)+1] = chr(self.rdsStatus.BLOCKDL)

#                 if self.rdsStatus.BLOCKB_GROUP0["address"] == 0:
#                     self.char_list[0], self.char_list[1] = chr(self.rdsStatus.BLOCKDH),chr(self.rdsStatus.BLOCKDL)
#                 elif self.rdsStatus.BLOCKB_GROUP0["address"] == 1:
#                     self.char_list[2], self.char_list[3] = chr(self.rdsStatus.BLOCKDH),chr(self.rdsStatus.BLOCKDL)
#                 elif self.rdsStatus.BLOCKB_GROUP0["address"] == 2:
#                     self.char_list[4], self.char_list[5] = chr(self.rdsStatus.BLOCKDH),chr(self.rdsStatus.BLOCKDL)
#                 elif self.rdsStatus.BLOCKB_GROUP0["address"] == 3:
#                     self.char_list[6], self.char_list[7] = chr(self.rdsStatus.BLOCKDH),chr(self.rdsStatus.BLOCKDL)

                self.station_name = "".join(self.station_name)
                #print(self.char_list)

            elif self.rdsStatus.BLOCKB_GROUP0["groupType"] == 2:
                station_text = list(self.station_text)
                station_text[self.rdsStatus.BLOCKB_GROUP2["address"]*4] = chr(self.rdsStatus.BLOCKCH)
                station_text[(self.rdsStatus.BLOCKB_GROUP2["address"]*4)+1] = chr(self.rdsStatus.BLOCKCL)
                station_text[(self.rdsStatus.BLOCKB_GROUP2["address"]*4)+2] = chr(self.rdsStatus.BLOCKDH)
                station_text[(self.rdsStatus.BLOCKB_GROUP2["address"]*4)+3] = chr(self.rdsStatus.BLOCKDL)
                self.teststring = "".join(station_text)

                #print(self.teststring)

            elif self.rdsStatus.BLOCKB_GROUP0["groupType"] == 4:
                print("TIME")

    def setRDSConfig(self,RDSEN,BLETHA,BLETHB,BLETHC,BLETHD):
        rds_config = Si47xRdsConfig()
        rds_config.rds_processing_enable = RDSEN
        rds_config.block_error_threshold_a = BLETHA
        rds_config.block_error_threshold_b = BLETHB
        rds_config.block_error_threshold_c = BLETHC
        rds_config.block_error_threshold_d = BLETHD
        #rds_config.to_raw()

        Property = Si47xProperty()
        Property.set_value(FM_RDS_CONFIG)

        self.waitToSend()
        
        #barray = bytearray((SET_PROPERTY,0,Property.raw['byteHigh'],Property.raw['byteLow'],ssbMode.raw_data[1],ssbMode.raw_data[0]))
        barray = bytearray((SET_PROPERTY,0,Property.raw['byteHigh'],Property.raw['byteLow'],rds_config.get_raw()[1],rds_config.get_raw()[0]))
        print(", ".join(hex(b) for b in barray))
        self.si4735_i2c.writeto(barray)
        time.sleep(550/1_000_000)
        print("Set RDS Config")

    def setVolume(self, level):

        self.volume = level
        Property = Si47xProperty()
        Property.set_value(RX_VOLUME)
        Param = Si47xProperty()
        Param.set_value(level)

        self.waitToSend()

        barray = bytearray((SET_PROPERTY,0,Property.raw['byteHigh'],Property.raw['byteLow'],Param.raw['byteHigh'],Param.raw['byteLow']))
        print(barray)
        self.si4735_i2c.writeto(barray)
        self.waitToSend()
        time.sleep(0.0055)
        print("set volume")
