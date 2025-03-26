import si47xx

class RADIO:

    FM = 1
    LW = 2
    AM = 3
    SW = 4
    SW_SSB_USB = 5
    SW_SSB_LSB = 6

    def __init__(self, hw):
        self.station_name = " " * 8
        self.station_text = " " * 64
        self.frequency = [0,0,0,0,0,0,0]
        self.frequency[RADIO.FM] = 6400  #current frequency
        self.frequency[RADIO.LW] = 153
        self.frequency[RADIO.AM] = 520
        self.frequency[RADIO.SW] = 2300
        self.frequency[RADIO.SW_SSB_USB] = 2300
        self.frequency[RADIO.SW_SSB_LSB] = 2300
        self.volume = 30 #current volume
        self.current_mode = self.FM
        self.hw = hw
        self.just_reset = False

    def get_frequency(self):
        return self.frequency[self.current_mode]

    def set_frequency(self,frequency):
        self.frequency[self.current_mode] = frequency
        self.hw.setFrequency(self.frequency[self.current_mode])

    def getVolume(self):
        return self.volume

    def get_mode(self):
        return self.current_mode

    def set_mode(self,mode_selection):
        assert mode_selection in ( self.FM,self.LW, self.AM, self.SW, self.SW_SSB_USB,self.SW_SSB_LSB)
        if mode_selection != self.current_mode or self.just_reset is True:
            previous_mode_selection = self.current_mode
            self.current_mode = mode_selection
            if mode_selection == self.AM:
                self.hw.setAM()
                self.set_frequency(self.frequency[RADIO.AM])

            elif mode_selection == self.LW:
                self.hw.setAM()
                self.set_frequency(self.frequency[RADIO.LW])

            elif mode_selection == self.SW:
                self.hw.setAM()
                self.set_frequency(self.frequency[RADIO.SW])

            elif mode_selection == self.SW_SSB_USB:
                if previous_mode_selection not in (self.SW_SSB_USB,self.SW_SSB_LSB):
                    self.hw.powerDown()
                    self.hw.patchPowerUp()
                    self.hw.download_compressed_patch()
                self.hw.setSSB(si47xx.SSB_SIDEBAND_USB)
                self.set_frequency(self.frequency[RADIO.SW_SSB_USB])

                self.hw.setSSBConfig(1, 0, 0, 1, 0, 1)

            elif mode_selection == self.SW_SSB_LSB:
                if previous_mode_selection not in (self.SW_SSB_USB,self.SW_SSB_LSB):
                    self.hw.powerDown()
                    self.hw.patchPowerUp()
                    self.hw.download_compressed_patch()
                self.hw.setSSB(si47xx.SSB_SIDEBAND_LSB)
                self.set_frequency(self.frequency[RADIO.SW_SSB_LSB])

                #self.hw.setSSBConfig(1, 0, 0, 1, 0, 1)

            elif mode_selection == self.FM:
                #Go to FM Mode
                self.hw.setFM()
                self.hw.setRDSConfig(1,3,3,3,3)
                self.set_frequency(self.frequency[RADIO.FM])


        
        self.just_reset = 0


    def get_current_signal_quality(self):
        return self.hw.getCurrentReceivedSignalQuality(0)

    def reset(self):
        self.hw.reset()
        self.just_reset = True

    def set_volume(self,volume):
        self.hw.setVolume(volume)


    def frequency_increment(self):
        increment=0
        if  self.current_mode == self.FM:
            increment=10
        elif self.current_mode in (self.SW_SSB_USB,self.SW_SSB_LSB,self.SW):
            increment=1
        elif self.current_mode in (self.AM,self.LW):
            increment=1
        print("inc")

        self.set_frequency(self.frequency[self.current_mode] + increment)

    def frequency_decrement(self):
        increment = 0
        if  self.current_mode ==  self.FM:
            increment=10
        elif self.current_mode in (self.SW_SSB_USB,self.SW_SSB_LSB,self.SW):
            increment=1
        elif self.current_mode in (self.AM,self.LW):
            increment=1

        self.set_frequency(self.frequency[self.current_mode] - increment)

    def update_rds(self):
        if self.current_mode ==  self.FM:
            self.hw.getRDSStatus(0,0,0)

    def get_ssb_bandwidth(self):
        return self.hw.getSSBBandwidth()

    def set_ssb_bandwidth(self,bandwidth):
        self.hw.setSSBBandwidth(bandwidth)





