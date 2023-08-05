from piratslib.common.BaseClasses import ADC
from piratslib.components.GPIO_Out.GPIOOut import GPIOOut
from piratslib.common.logger import log as log
from piratslib.components.MCP_23S17.MCP23S17 import  MCP23S17
import spidev
import math
import time

class ADCPTCArray(ADC):
    """
    Provides reading of up to 16 PTC100s which signal is converted with a MAX31865 each connected to the SPI Bus.
    To provide the needed CS signal for each MAX31865 an MCP23S17, also connected to the SPI bus,
    is used to activate the selected chip according to the PTC that has to be read.
    """
    MAX31865_N_REGS = 8
    MAX31865_CONFIG_ADR = 0
    MAX31865_RTD_MSB_ADR = 1
    MAX31865_RTD_LSB_ADR = 2
    MAX31865_HFT_MSB_ADR = 3
    MAX31865_HFT_LSB_ADR = 4
    MAX31865_LFT_MSB_ADR = 5
    MAX31865_LFT_LSB_ADR = 6
    MAX31865_FAULT_STATUS_ADR = 7

    def __init__(self):
        self._MCP_ADDRESS = 0
        self._mcp = GPIOOut(self._MCP_ADDRESS)
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
        self._spiB.max_speed_hz = 100000
        self._startup_routine()

    def analog_read(self, input_number):
        """
        Returns the adc reading of the PTC100 designated by the index.
        """
        reading = self._read_registers_get_read_data(input_number)
        return reading

    def analog_read_all(self):
        """
        Returns a list with the adc readings of the whole array of PTC100s in the array
        """
        readings = []
        for port_number in range(0, self._mcp.N_PORTS):
            readings.append(self.analog_read(port_number))
        return readings

    def read_temperature(self, input_number):
        """
        Returns the temperature reading in ºC of the PTC100 designated by the index.
        """
        adc_reading = self.analog_read(input_number)
        temp_reading = self._calc_pt100_temp(adc_reading)
        return temp_reading

    def read_all_temperatures(self):
        """
        Returns a list with the temperature readings in ºC of all the PTC100s in the array
        """
        temperatures = []
        for adc_value in self.analog_read_all():
            temperatures.append(self._calc_pt100_temp(adc_value))
        return temperatures

    def set_reference_resistance(self, r_ref):
        """
        Sets the reference resistance which default value is 400 Ohms (as placed in the board)
        """
        self._R_REF = r_ref

    def _startup_routine(self):
        self._mcp.write_gpio(0xFFFFF)
        self._mcp.write_gpio(0x0000)
        self._mcp.write_gpio(0xFFFFF)
        for x in range(0, self._mcp.N_PORTS):
            if x <= 7:
                self._mcp.write_register(MCP23S17.MCP23S17_GPIOA, ~(1 << x) & 0xFF)
            elif x > 7:
                self._mcp.write_register(MCP23S17.MCP23S17_GPIOA + 1, (~(1 << x) & 0xFFFF) >> 8)
            # self._mcp.write_gpio(~(1 << x))
            self._spiB.xfer2([0x80, 0xC0])
            self._mcp.write_gpio(0xFFFF)
            time.sleep(0.01)
        self.analog_read_all()


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

    def _read_registers_get_read_data(self, input_number):
        adc_reg_read = []
        for register in range(0, self.MAX31865_N_REGS):
            # self._mcp.write_gpio(~(1 << input_number))
            if input_number <= 7:
                self._mcp.write_register(MCP23S17.MCP23S17_GPIOA, ~(1 << input_number) & 0xFF)
            else:
                self._mcp.write_register(MCP23S17.MCP23S17_GPIOB, (~(1 << input_number) & 0xFFFF) >> 8)
            resp = self._spiB.xfer2([register, 0x00])
            adc_reg_read.append(resp[1])
            self._mcp.write_gpio(0xFFFFF)
            # time.sleep(0.01)
        log.debug(f'INPUT{input_number}')
        log.debug(f'ADC REG READ: {adc_reg_read}')
        rtd_data = ((adc_reg_read[ADCPTCArray.MAX31865_RTD_MSB_ADR] << 8) |
                    adc_reg_read[ADCPTCArray.MAX31865_RTD_LSB_ADR]) >> 1
        hft = ((adc_reg_read[ADCPTCArray.MAX31865_HFT_MSB_ADR]<< 8) |
               adc_reg_read[ADCPTCArray.MAX31865_HFT_LSB_ADR]) >> 1
        log.debug(f'high fault threshold: {hft}')
        lft = ((adc_reg_read[ADCPTCArray.MAX31865_LFT_MSB_ADR] << 8) |
                adc_reg_read[ADCPTCArray.MAX31865_LFT_LSB_ADR]) >> 1
        log.debug(f'low fault threshold: {lft}')
        if ((adc_reg_read[ADCPTCArray.MAX31865_FAULT_STATUS_ADR] & 0x80) == 1):
            log.error("High threshold limit (Cable fault/open)")
        if ((adc_reg_read[ADCPTCArray.MAX31865_FAULT_STATUS_ADR] & 0x40) == 1):
            log.error("Low threshold limit (Cable fault/short)")
        if ((adc_reg_read[ADCPTCArray.MAX31865_FAULT_STATUS_ADR] & 0x04) == 1):
            log.error("Overvoltage or Undervoltage Error")
        return rtd_data

class FaultError(Exception):
    pass


if __name__ == '__main__':
    """
    This demo tests the ADCPTC100Array
    """
    import logging
    log.setLevel(logging.INFO)
    ptc100_array = ADCPTCArray()
    # TEST_RTC_NUMBER = 0 # 9, 10, 12, 14 <-The only working ones.
    # temperature = ptc100_array.read_temperature(TEST_RTC_NUMBER)
    # log.info(f'Temperature on PTC100 #{TEST_RTC_NUMBER} is {temperature:.3f}ºC')
    while True:
        start_time = time.time()
        for n_rtd, temp in enumerate(ptc100_array.read_all_temperatures()):
            log.info(f'->RTD #{n_rtd} is @ {temp:.3f}ºC')
        log.info("--- %s seconds ---" % (time.time() - start_time))
        time.sleep(0.5)
