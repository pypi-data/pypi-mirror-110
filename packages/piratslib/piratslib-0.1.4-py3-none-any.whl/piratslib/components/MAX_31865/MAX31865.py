import spidev
import math
from piratslib.common.logger import log as log


class MAX31865():
    """
    Provides reading of up to 16 PTC100s which signal is converted with a MAX31865 each connected to the SPI Bus.
    To provide the needed CS signal for each MAX31865 an MCP23S17, also connected to the SPI bus,
    is used to activate the selected chip according to the PTC that has to be read.
    """
    N_REGS = 8
    CONFIG_ADR = 0
    RTD_MSB_ADR = 1
    RTD_LSB_ADR = 2
    HFT_MSB_ADR = 3
    HFT_LSB_ADR = 4
    LFT_MSB_ADR = 5
    LFT_LSB_ADR = 6
    FAULT_STATUS_ADR = 7

    def __init__(self):
        self._spiB = spidev.SpiDev()
        self._R_REF = 400.0
        self._Res0 = 100.0
        self.setup()

    def setup(self):
        """
        Initializes the module and communication with the 16 MAX31865 and the 16 gpios
        of the MCP23S17 that provide the CSs, called in the instantiation of the object.
        """
        self._spiB.open(1, 1)
        self._spiB.mode = 2
        self._spiB.max_speed_hz = 10000000

    def analog_read(self):
        """
        Returns the adc reading of the PTC100 designated by the index.
        """
        reading = self._read_registers_get_read_data()
        return reading

    def read_temperature(self):
        """
        Returns the temperature reading in ºC of the PTC100 designated by the index.
        """
        adc_reading = self.analog_read()
        temp_reading = self._calc_pt100_temp(adc_reading)
        return temp_reading

    def set_reference_resistance(self, r_ref):
        """
        Sets the reference resistance which default value is 400 Ohms (as placed in the board)
        """
        self._R_REF = r_ref


    def _calc_pt100_temp(self, rtd_adc_code):
        a = .00390830
        b = -.000000577500
        log.debug(f'RTD ADC Code: {rtd_adc_code}')
        res_rtd = (rtd_adc_code * self._R_REF) / 32768.0
        # print(f'PT100 Resistance: {res_rtd} ohms')
        temp_C = -(a * self._Res0) + \
                 math.sqrt(a * a * self._Res0 * self._Res0 - 4 * (b * self._Res0) * (self._Res0 - res_rtd))
        temp_C = temp_C / (2 * (b * self._Res0))
        # temp_C_line = (rtd_adc_code / 32.0) - 256.0
        # print(f'Straight Line Approx. Temp: {temp_C_line} degC')
        # print(f'Callendar-Van Dusen Temp (degC > 0): {temp_C} degC')
        if (temp_C < 0):
            temp_C = (rtd_adc_code / 32) - 256
        return temp_C

    def _read_registers_get_read_data(self):
        adc_reg_read = []
        for register in range(0, MAX31865.N_REGS):
            resp = self._spiB.xfer2([register, 0x00])
            adc_reg_read.append(resp[1])
        log.debug(f'ADC REG READ: {adc_reg_read}')
        rtd_data = ((adc_reg_read[MAX31865.RTD_MSB_ADR] << 8) |
                    adc_reg_read[MAX31865.RTD_LSB_ADR]) >> 1
        # hft = ((adc_reg_read[ADCPTCArray.MAX31865_HFT_MSB_ADR]<< 8) |
        #        adc_reg_read[ADCPTCArray.MAX31865_HFT_LSB_ADR]) >> 1
        # print(f'high fault threshold: {hft}')
        # lft = ((adc_reg_read[ADCPTCArray.MAX31865_LFT_MSB_ADR] << 8) |
        #         adc_reg_read[ADCPTCArray.MAX31865_LFT_LSB_ADR]) >> 1
        # print(f'low fault threshold: {lft}')
        if ((adc_reg_read[MAX31865.FAULT_STATUS_ADR] & 0x80) == 1):
            raise FaultError("High threshold limit (Cable fault/open)")
        if ((adc_reg_read[MAX31865.FAULT_STATUS_ADR] & 0x40) == 1):
            raise FaultError("Low threshold limit (Cable fault/short)")
        if ((adc_reg_read[MAX31865.FAULT_STATUS_ADR] & 0x04) == 1):
            raise FaultError("Overvoltage or Undervoltage Error")
        return rtd_data

class FaultError(Exception):
    pass


if __name__ == '__main__':
    """
    This demo tests the ADCPTC100Array
    """
    import logging
    log.setLevel(logging.INFO)
    max31865 = MAX31865()
    TEST_RTC_NUMBER = 14 # 9, 10, 12, 14 <-The only working ones.
    temperature = max31865.read_temperature()
    log.info(f'Temperature on PTC100 #{TEST_RTC_NUMBER} is {temperature:.3f}ºC')
