from piratslib.components.ADS_1018.ADS1018 import ADS1018
from piratslib.components.ADS_1018.ADS1018Consts import ADS1018Consts

class VoltageSense():
    """
    Class to abstract and interface with the ADS1018 and read voltages sof the PI-Rats Boards
    """
    def __init__(self):
        self.ads1018 = ADS1018()
        self.ads1018.set_full_scale_range(ADS1018Consts.FSR_4096)
        self.ads1018.set_sampling_rate(ADS1018Consts.RATE_3300SPS)

    def get_single_voltage(self, input_pin):
        """
        Returns the voltage measured by the designated pin
        :param input_pin:
        :return:
        """
        return self.ads1018.get_single_voltage(input_pin)

    def get_voltages_list(self, channel_list):
        return [{channel:self.get_single_voltage(channel)} for channel in channel_list]

if __name__ == '__main__':
    """
    This demo tests the ADCSense Module  
    """
    from piratslib.common.logger import log
    import logging
    import time
    log.setLevel(logging.INFO)
    volt_sense = VoltageSense()
    while(True):
        log.info(f'A0: {volt_sense.get_single_voltage(ADS1018Consts.AIN_0)}V\t\t'
                 f'A1: {volt_sense.get_single_voltage(ADS1018Consts.AIN_1)}V\t\t'
                 f'A2: {volt_sense.get_single_voltage(ADS1018Consts.AIN_2)}V\t\t'
                 f'A3: {volt_sense.get_single_voltage(ADS1018Consts.AIN_3)}V\t\t'
                 f'D0: {volt_sense.get_single_voltage(ADS1018Consts.DIFF_0_1)}V\t\t'
                 f'D1: {volt_sense.get_single_voltage(ADS1018Consts.DIFF_0_3)}V\t\t'
                 f'D2: {volt_sense.get_single_voltage(ADS1018Consts.DIFF_1_3)}V\t\t'
                 f'D3: {volt_sense.get_single_voltage(ADS1018Consts.DIFF_2_3)}V')
        time.sleep(1.0)