import si47xx

class RADIO:

    FM = 1
    AM = 2
    SSB_USB = 3
    SSB_LSB = 4

    def __init__(self, hw):
        self.station_name = " " * 8
        self.station_text = " " * 64
        self.frequency = 0 #current frequency
        self.volume = 30 #current volume
        self.current_mode = self.FM
        self.hw = hw
        self.just_reset = False

    def get_frequency(self):
        return self.frequency

    def set_frequency(self,frequency):
        self.frequency = frequency
        self.hw.setFrequency(frequency)

    def getVolume(self):
        return self.volume

    def get_mode(self):
        return self.current_mode

    def set_mode(self,mode_selection):
        assert mode_selection in ( self.FM, self.AM, self.SSB_USB,self.SSB_LSB)
        if mode_selection != self.current_mode or self.just_reset == True:
            if mode_selection == self.AM:
                self.hw.setAM()
                self.set_frequency(198)

            elif mode_selection == self.SSB_USB:
                self.hw.powerDown()
                self.hw.patchPowerUp()
                self.hw.download_compressed_patch()
                self.hw.setSSB(si47xx.SSB_SIDEBAND_USB)
                self.set_frequency(14000)

                self.hw.setSSBConfig(1, 0, 0, 1, 0, 1)

            elif mode_selection == self.SSB_LSB:
                self.hw.setSSB(si47xx.SSB_SIDEBAND_LSB)
                self.set_frequency(self.frequency)

            elif mode_selection == self.FM:
                #Go to FM Mode
                self.hw.setFM()
                self.hw.setRDSConfig(1,3,3,3,3)
                self.set_frequency(9703)


        self.current_mode = mode_selection
        self.just_reset = 0


    def get_current_signal_quality(self):
        return self.hw.getCurrentReceivedSignalQuality(0)

    def reset(self):
        #addr = self.hw.get_device_i2c_address()
        #if addr == 0:
        #    sys.exit()
        self.hw.reset()
        self.just_reset = True

    def set_volume(self,volume):
        self.hw.setVolume(volume)


    def frequency_increment(self):
        increment=0
        if  self.current_mode == self.FM:
            increment=10
        elif self.current_mode ==  self.SSB_USB or self.current_mode ==  self.SSB_LSB:
            increment=1
        elif self.current_mode ==  self.AM:
            increment=1


        self.set_frequency(self.frequency + increment)

    def frequency_decrement(self):
        increment = 0
        if  self.current_mode ==  self.FM:
            increment=10
        elif self.current_mode ==  self.SSB_USB or self.current_mode ==  self.SSB_LSB:
            increment=1
        elif self.current_mode ==  self.AM:
            increment=1

        self.set_frequency(self.frequency - increment)

    def update_rds(self):
        if self.current_mode ==  self.FM:
            self.hw.getRDSStatus(0,0,0)

    def get_ssb_bandwidth(self):
        return self.hw.getSSBAudioBandwidth()

    def set_ssb_bandwidth(self,bandwidth):
        self.hw.setSSBAudioBandwidth(bandwidth)





