import si47xx

class RADIO_RX:

    FM = 1
    AM = 2
    SSB_USB = 3
    SSB_LSB = 4

    def __init__(self, radio_hw_library):
        self.station_name = " " * 8
        self.station_text = " " * 64
        self.frequency = 0 #current frequency
        self.volume = 30 #current volume
        self.current_mode = self.FM
        self.hw_library = radio_hw_library
        self.just_reset = 0




    def get_frequency(self):
        return self.frequency

    def set_frequency(self,frequency):
        self.frequency = frequency
        self.hw_library.setFrequency(frequency)

    def getVolume(self):
        return self.volume

    def get_mode(self):
        return self.current_mode

    def set_mode(self,mode_selection):
        assert mode_selection in ( self.FM, self.AM, self.SSB_USB,self.SSB_LSB)
        if mode_selection != self.current_mode or self.just_reset == 1:
            if mode_selection == self.AM:
                self.hw_library.setAM()
                self.set_frequency(198)

            elif mode_selection == self.SSB_USB:
                self.hw_library.powerDown()
                self.hw_library.patchPowerUp()
                self.hw_library.download_compressed_patch()

                self.hw_library.setSSB(si47xx.SSB_SIDEBAND_USB)
                self.set_frequency(14000)

                self.hw_library.setSSBConfig(1, 0, 0, 1, 0, 1)

            elif mode_selection == self.SSB_LSB:

                self.hw_library.setSSB(si47xx.SSB_SIDEBAND_LSB)
                self.set_frequency(self.frequency)

            elif mode_selection == self.FM:
                #Go to FM Mode
                self.hw_library.setFM()
                self.hw_library.setRDSConfig(1,3,3,3,3)
                self.set_frequency(9703)


        self.current_mode = mode_selection
        self.just_reset = 0


    def get_current_signal_quality(self):
        return self.hw_library.getCurrentReceivedSignalQuality(0)

    def reset(self):
        addr = self.hw_library.get_device_i2c_address()
        if addr == 0:
            sys.exit()
        self.hw_library.reset()
        self.just_reset = 1

    def set_volume(self,volume):
        self.hw_library.setVolume(volume)


    def frequency_increment(self):
        if  self.current_mode == self.FM:
            increment=10
        elif self.current_mode ==  self.SSB_USB or self.current_mode ==  self.SSB_LSB:
            increment=1
        elif self.current_mode ==  self.AM:
            increment=1


        self.set_frequency(self.frequency + increment)

    def frequency_decrement(self):
        if  self.current_mode ==  self.FM:
            increment=10
        elif self.current_mode ==  self.SSB_USB or self.current_mode ==  self.SSB_LSB:
            increment=1
        elif self.current_mode ==  self.AM:
            increment=1


        self.set_frequency(self.frequency - increment)

    def poll(self):
        if self.current_mode ==  self.FM:
               self.hw_library.getRDSStatus(0,0,0)

    def get_ssb_bandwidth(self):
        return self.hw_library.getSSBAudioBandwidth()

    def set_ssb_bandwidth(self,bandwidth):
        self.hw_library.setSSBAudioBandwidth(bandwidth)





