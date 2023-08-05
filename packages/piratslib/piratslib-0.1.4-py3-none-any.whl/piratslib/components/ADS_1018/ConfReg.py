from piratslib.common.logger import log as log
from piratslib.components.ADS_1018.ADS1018Consts import ADS1018Consts

class ConfReg():
    def __init__(self):
        self._run_mode = ADS1018Consts.STOP
        self._mux_mode = ADS1018Consts.DIFF_0_1
        self._fsr_value = ADS1018Consts.FSR_2048
        self._acq_mode = ADS1018Consts.SINGLE_SHOT
        self._acq_rate = ADS1018Consts.RATE_1600SPS
        self._adc_mode = ADS1018Consts.ADC_MODE
        self._input_mode = ADS1018Consts.INT_PULLUP
        self._cfg_mode = ADS1018Consts.VALID_CFG

    @property
    def run_mode(self):
        return self._run_mode
    @run_mode.setter
    def run_mode(self, run_mode):
        self._run_mode = run_mode

    @property
    def mux_mode(self):
        return self._mux_mode
    @mux_mode.setter
    def mux_mode(self, mode):
        self._mux_mode = mode

    @property
    def fsr_value(self):
        return self._fsr_value
    @fsr_value.setter
    def fsr_value(self, value):
        self._fsr_value = value

    @property
    def acq_mode(self):
        return self._acq_mode
    @acq_mode.setter
    def acq_mode(self, mode):
        self._acq_mode = mode

    @property
    def acq_rate(self):
        return self._acq_rate
    @acq_rate.setter
    def acq_rate(self, rate):
        self._acq_rate = rate

    @property
    def adc_mode(self):
        return self._adc_mode
    @adc_mode.setter
    def adc_mode(self, mode):
        self._adc_mode = mode

    @property
    def input_mode(self):
        return self._input_mode
    @input_mode.setter
    def input_mode(self, mode):
        self._input_mode = mode

    @property
    def cfg_mode(self):
        return self._cfg_mode
    @cfg_mode.setter
    def cfg_mode(self, mode):
        self._cfg_mode = mode

    def get_reg_values(self):
        return [ADS1018Consts.RESERVED, self._cfg_mode, self._input_mode, self._adc_mode, self._acq_rate, self._acq_mode,
                self._fsr_value, self._mux_mode, self._run_mode]

    def _compose_reg_bits_list(self):
        config_reg_bits_lists = [_itoblist(ADS1018Consts.RESERVED, 1), _itoblist(self.cfg_mode, 2), _itoblist(self.input_mode, 1),
                                 _itoblist(self.adc_mode, 1), _itoblist(self.acq_rate, 3), _itoblist(self.acq_mode, 1),
                                 _itoblist(self.fsr_value, 3), _itoblist(self.mux_mode, 3), _itoblist(self.run_mode, 1)]
        config_reg_bits = []
        for bit_list in config_reg_bits_lists:
            for bit in bit_list:
                config_reg_bits.append(bit)
        return config_reg_bits

    def get_bytes(self):
        config_reg_bits = self._compose_reg_bits_list()
        value = _bool_list_to_int(config_reg_bits)
        hi_byte = int(value / 256)
        lo_byte = value - (256 * hi_byte)
        return [int(hex(hi_byte),16), int(hex(lo_byte),16), int(hex(hi_byte),16), int(hex(lo_byte),16)]

def _itoblist(num, n_bits):
    return [bool(num & (1 << n)) for n in range(n_bits)]

def _bool_list_to_int(bool_list, reverse_list=False):
    uint_result = 0
    if reverse_list:
        bool_list = bool_list[::-1]
    for i, value in enumerate(bool_list):
        uint_result |= value << i
    return uint_result


if __name__ == '__main__':
    conf_reg = ConfReg()
    conf_reg.run_mode = ADS1018Consts.START_NOW
    conf_reg.acq_mode = ADS1018Consts.CONTINUOUS
    conf_reg.adc_mode = ADS1018Consts.TEMP_MODE
    import logging
    log.setLevel(logging.INFO)
    log.info(conf_reg.get_bytes())
    log.info(f'{hex(conf_reg.get_bytes()[0])}   {hex(conf_reg.get_bytes()[1])}')  # [0xE5, 0x9B]