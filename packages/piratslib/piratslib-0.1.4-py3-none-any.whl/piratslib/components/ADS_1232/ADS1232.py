from piratslib.common.BaseClasses import ADC
import RPi.GPIO as GPIO
from piratslib.common.logger import log as log
import time

class ADS1232(ADC):
    """
    Provides 2 differential 24 bits depth and 10Hz-80Hz of sampling rate analog inputs using an ADS1232
    connected to the SPI bus. This characteristics makes them suitable for converting Load Cells signals
    with high precision.
    """
    GR_STEP = 1.24
    CHANNEL_0 = 0
    CHANNEL_1 = 1
    GAIN_1 = 1
    GAIN_2 = 2
    GAIN_64 = 3
    GAIN_128 = 4
    RATE_80SPS = 1
    RATE_10SPS = 2
    PW_UP = 1
    PW_DWN = 2
    TEMP_ON = 1
    ADC_ON = 2
    GAIN_VALUES = [1, 2, 64, 128]

    def __init__(self):
        self.GAIN_PIN_0 = 27     # pin BCM  13
        self.GAIN_PIN_1 = 22    # pin BCM 15
        self.PWDN_PIN =  26     # pin BCM 37. cheapskate to enable power down
        self.SCLK_PIN = 12      # pin BCM 32. SCLK pin
        self.TEMP_PIN = 4     # pin BCM 7
        self.SPEED_PIN = 25   # pin BCM 22
        self.ADDRESS_PIN = 13  # pin BCM 33   cheapskate at pin 17 to enable el A0 through pin 33
        self.INPUT_DATA_PIN = 1  # pin BCM 28
        self.TIME_READ = 0.5    # sampling intervals
        self.VDD = 3.3

    def setup(self):
        """
        Initializes the module and communication with the chip, called in the instantiation of the object.
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PWDN_PIN, GPIO.OUT)
        GPIO.setup(self.SCLK_PIN, GPIO.OUT)
        GPIO.setup(self.ADDRESS_PIN, GPIO.OUT)
        GPIO.setup(self.GAIN_PIN_0, GPIO.OUT)
        GPIO.setup(self.GAIN_PIN_1, GPIO.OUT)
        GPIO.setup(self.TEMP_PIN, GPIO.OUT)
        GPIO.setup(self.SPEED_PIN, GPIO.OUT)
        GPIO.setup(self.INPUT_DATA_PIN, GPIO.IN)
        self._power_up_sequence()

    # def analog_read(self, input_number):
    #     """
    #     Returns the last reading of the analog input of the ADC.
    #     """
    #     self.set_channel(input_number)
    #     return self._signal_read()

    def analog_read(self, input_number):
        """
        Returns the last reading of the analog input of the ADC.
        """
        self.set_channel(input_number)
        return self._signal_read()

    def analog_read_all(self):
        """
        Returns the readings of all the inputs of the ADC.
        """
        values_list = []
        for input in range(0,2):
            values_list.append(self.analog_read(input))
        return values_list

    def set_channel(self, channel):
        """
        Selects the input channel on which perform the reading
        """
        if channel == ADS1232.CHANNEL_0:
            GPIO.output(self.ADDRESS_PIN, GPIO.LOW)
        elif channel == ADS1232.CHANNEL_1:
            GPIO.output(self.ADDRESS_PIN, GPIO.HIGH)

    def select_temperature_read(self, is_temp_on):
        """
        Selects if the output value is the temperature or the actual input reading.
        Selectable values are TEMP_ON and ADC_ON
        """
        if is_temp_on == ADS1232.TEMP_ON:
            GPIO.output(self.TEMP_PIN, GPIO.HIGH)
        elif is_temp_on == ADS1232.ADC_ON:
            GPIO.output(self.TEMP_PIN, GPIO.LOW)

    def set_power_up(self, is_power_up):
        """
        Sets the power up of the ADC. Selectable values are PW_UP, PW_DWN
        """
        if is_power_up == ADS1232.PW_UP:
            GPIO.output(self.PWDN_PIN, GPIO.HIGH)
            GPIO.output(self.SCLK_PIN, GPIO.LOW)
        elif is_power_up == ADS1232.PW_DWN:
            GPIO.output(self.PWDN_PIN, GPIO.LOW)
            GPIO.output(self.SCLK_PIN, GPIO.HIGH)

    def set_sampling_rate(self, sampling_rate):
        """
        Sets sampling rate acquisition speed. Selectable values are RATE_80SPS or  RATE_80SPS
        """
        if sampling_rate == ADS1232.RATE_80SPS:
            GPIO.output(self.SPEED_PIN, GPIO.HIGH)  # speed 1 : 80 SPS
        elif sampling_rate == ADS1232.RATE_80SPS:
            GPIO.output(self.SPEED_PIN, GPIO.LOW)  # speed 0 : 10 SPS

    def set_gain(self, gain):
        """
        Sets the gain in the programmable gain amplifier. Selectable values are GAIN_1, GAIN_2, GAIN_64 and GAIN_128
        """
        if gain == ADS1232.GAIN_1:
            GPIO.output(self.GAIN_PIN_0, GPIO.LOW)
            GPIO.output(self.GAIN_PIN_1, GPIO.LOW)
        elif gain == ADS1232.GAIN_2:
            GPIO.output(self.GAIN_PIN_0, GPIO.HIGH)
            GPIO.output(self.GAIN_PIN_1, GPIO.LOW)
        elif gain == ADS1232.GAIN_64:
            GPIO.output(self.GAIN_PIN_0, GPIO.LOW)
            GPIO.output(self.GAIN_PIN_1, GPIO.HIGH)
        elif gain == ADS1232.GAIN_128:
            GPIO.output(self.GAIN_PIN_0, GPIO.HIGH)
            GPIO.output(self.GAIN_PIN_1, GPIO.HIGH)

    def is_ready(self):
        """
        Returns true when the DRDY pin is high indicating there’s data in the output buffer.
        """
        return GPIO.input(self.INPUT_DATA_PIN)

    def _signal_read(self):
        recv = 0
        for i in range(25):
            GPIO.output(self.SCLK_PIN, GPIO.HIGH)
            time.sleep(0.0001)
            recv = recv << 1
            GPIO.output(self.SCLK_PIN, GPIO.LOW)
            time.sleep (0.0001)
            if self.is_ready():
                recv = recv | 0x1
        time.sleep(0.005)
        recv >>= 1
        value = recv >> 6
        return value

    def _power_up_sequence(self):
        GPIO.output(self.ADDRESS_PIN, GPIO.LOW)
        GPIO.output(self.PWDN_PIN, GPIO.LOW)
        time.sleep(0.0001)
        GPIO.output(self.PWDN_PIN, GPIO.HIGH)
        time.sleep(0.0001)
        GPIO.output(self.PWDN_PIN, GPIO.LOW)
        time.sleep(0.0001)
        GPIO.output(self.PWDN_PIN, GPIO.HIGH)
        time.sleep(0.002)

if __name__ == '__main__':
    """
    This demo tests the ADCLoadCells Module
    """
    import logging
    CH = 1
    log.setLevel(logging.INFO)
    ads1232 = ADS1232()
    ads1232.setup()
    ads1232.set_power_up(ADS1232.PW_UP)
    ads1232.set_sampling_rate(ADS1232.RATE_80SPS)
    ads1232.set_gain(ADS1232.GAIN_64)
    ads1232.set_channel(CH)

    while(True):
        if(ads1232.is_ready()):
            log.info(f'CH{CH}:{ads1232.analog_read(CH)}')
            time.sleep(1)
