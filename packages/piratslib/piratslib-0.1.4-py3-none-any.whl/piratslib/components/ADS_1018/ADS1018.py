import logging
import spidev
import time
from piratslib.common.BaseClasses import ADC
from piratslib.components.ADS_1018.ConfReg import ConfReg
from piratslib.components.ADS_1018.ADS1018Consts import ADS1018Consts
from piratslib.common.logger import log as log

class ADS1018(ADC):
    """
    Provides 4 discrete / 2 differential 12 bits depth and 3.3kHz of sampling rate analog inputs using
    an ADS1018 connected to the SPI bus.
    """

    def __init__(self):
        self._SCLK = 1000000 # ADS1018 SCLK frequency: 4000000 Hz Maximum for ADS1018 (4Mhz)
        self._spi = spidev.SpiDev()
        self._conf_reg = ConfReg()
        self.setup()

    def setup(self):
        """
        Initializes the module and communication with the chip, called in the instantiation of the object.
        """
        self._spi.open(0, 0)  # bus 0, chip select 0
        self._spi.mode = 1
        self._spi.max_speed_hz = self._SCLK

    def start(self):
        """
        Starts the acquisition of the ADC
        """
        self._conf_reg.run_mode = ADS1018Consts.START_NOW
        self._load_config()

    def stop(self):
        """
        Stops the acquisition of the ADC
        """
        self._conf_reg.run_mode = ADS1018Consts.STOP
        self._load_config()

    def set_run_mode(self, mode):
        """
        Sets the acquisition mode of the ADC between the two macros: CONTINUOUS, SINGLE_SHOT
        """
        self._conf_reg.run_mode = mode
        self._load_config()

    def analog_read(self, input):
        """
        Returns the last reading of the analog input of the ADC.
        """
        return self._get_single_value(input)

    def analog_read_all(self):
        adc_reads = []
        for i in range(0, ADS1018Consts.N_MUX_INPUTS):
            adc_reads.append(self.analog_read(i))

    def get_single_voltage(self, input):
        """
        Returns the reading of the selected input converted into Volts.
        Selectable input_selection constants are : DIFF_0_1, DIFF_0_3, DIFF_1_3, DIFF_2_3, AIN_0, AIN_1, AIN_2 or AIN_3
        """
        value = self._get_single_value(input)
        return self.convert_to_voltage(value)

    def convert_to_voltage(self, value):
        """
        Returns the conversion into voltage of the adc reading passed as value
        """
        return value * ADS1018Consts.PGA_FSR[self._conf_reg.fsr_value] / 1000

    def get_chip_temperature(self):
        """
        Returns the actual temperature measured in the chip in ºC
        """
        self._conf_reg.mux_mode = ADS1018Consts.AIN_0
        self._conf_reg.adc_mode = ADS1018Consts.TEMP_MODE
        self._conf_reg.run_mode = ADS1018Consts.SINGLE_SHOT
        temp_data = self._read_single()
        if temp_data >= 0x0800:
            temp_data =((~temp_data)+1 & 0x0fff) # Applying binary twos complement format
            return temp_data * 0.125
        return temp_data * 0.125

    def set_full_scale_range(self, fsr):
        """
        Sets the full scale range of the measurement which translates into the voltage per adc count.
        Selectable fsr macro values are: FSR_6144, FSR_4096, FSR_2048, FSR_1024, FSR_0512, FSR_0256
        """
        self._conf_reg.fsr_value = fsr
        self._load_config()

    def set_sampling_rate(self, sampling_rate):
        """
        Sets the sampling rate of the ADC. Selectable sampling rate macro values are:RATE_128SPS,
        RATE_250SPS, RATE_490SPS, RATE_920SPS, RATE_1600SPS, RATE_2400SPS or RATE_3300SP
        """
        self._conf_reg.acq_rate = sampling_rate
        self._load_config()

    def set_internal_pullup(self, mode):
        """
        Enables/Disables the internal pullup resistor connected to the input.
        Selectable mode macro values are: INT_PULLUP and NO_PULLUP
        """
        self._conf_reg.input_mode = mode
        self._load_config()

    def _get_single_value(self, input):
        self._conf_reg.mux_mode = input
        self._conf_reg.adc_mode = ADS1018Consts.ADC_MODE
        self._conf_reg.run_mode = ADS1018Consts.SINGLE_SHOT
        adc_data = self._read_single()
        return adc_data

    def _read_single(self):
        config_reg_data = self._conf_reg.get_bytes()
        data_bytes = self._spi_transaction(config_reg_data)
        read_data = (data_bytes[0] << 8) | data_bytes[1]
        read_data = read_data >> 4
        # print(read_data)
        return read_data

    def _load_config(self):
        config_reg_data = self._conf_reg.get_bytes()
        self._spi_transaction(config_reg_data)

    def _spi_transaction(self, data):
        self._spi.writebytes(data)
        time.sleep(ADS1018Consts.CONV_TIME[self._conf_reg.acq_rate] / 1000.0)
        resp = self._spi.readbytes(ADS1018Consts.N_BYTES_READ)
        # print('[{}]'.format(', '.join(hex(j) for j in resp)))
        return resp

    def decode_config_register(self):
        self._conf_reg.get_reg_values()

if __name__ == '__main__':
    """
    This demo tests the ADCSense Module  
    """
    log.setLevel(logging.INFO)
    ads = ADS1018()
    ads.set_full_scale_range(ADS1018Consts.FSR_4096)
    ads.set_sampling_rate(ADS1018Consts.RATE_3300SPS)
    while(True):
        # print(f'Temp: {ads.get_single_temperature()}ºC')
        # print(f'Voltage on AIN_0: {ads.get_single_voltage(ADS1018.AIN_0)}V')
        # print(f'Voltage on AIN_1: {ads.get_single_voltage(ADS1018.AIN_1)}V')
        # print(f'Voltage on AIN_2: {ads.get_single_voltage(ADS1018.AIN_2)}V')
        # print(f'Voltage on AIN_3: {ads.get_single_voltage(ADS1018.AIN_3)}V')
        log.info(f'T: {ads.get_chip_temperature()}ºC \t\t A0: {ads.get_single_voltage(ADS1018Consts.AIN_0)}V \t\t '
                f'A1: {ads.get_single_voltage(ADS1018Consts.AIN_1)}V\t\tA2: {ads.get_single_voltage(ADS1018Consts.AIN_2)}V\t\t '
                f'A3: {ads.get_single_voltage(ADS1018Consts.AIN_3)} V\t\tD0: {ads.get_single_voltage(ADS1018Consts.DIFF_0_1)}V \t\t '
                f'D1: {ads.get_single_voltage(ADS1018Consts.DIFF_0_3)}V\t\tD2: {ads.get_single_voltage(ADS1018Consts.DIFF_1_3)}V\t\t '
                f'D3: {ads.get_single_voltage(ADS1018Consts.DIFF_2_3)} V')
        time.sleep(1.0)
