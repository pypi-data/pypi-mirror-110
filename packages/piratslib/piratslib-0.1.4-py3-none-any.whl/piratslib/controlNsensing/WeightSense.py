from piratslib.components.ADS_1232.ADS1232 import ADS1232
from piratslib.common.logger import log
from piratslib.utils.CalcWeight import CalcWeight
from piratslib.utils.LoadCellsZeroCalibration import LoadCellsZeroCalibration
from os import path

N_SAMPLES = 100
NOMINAL_LOAD = 10000
NOMINAL_OUTPUT = 0.002
FULL_SCALE_VOLT = 5.0

class WeightSense():
    """
    Class to abstract and interface with the weight sensors, the ADS1232 with load cells, of the PI-Rats Boards
    """
    def __init__(self, nom_load, nom_output, full_scale_volt):
        self.ads1232 = ADS1232()
        self.ads1232.setup()
        self.ads1232.set_power_up(ADS1232.PW_UP)
        self.ads1232.set_sampling_rate(ADS1232.RATE_80SPS)
        self.ads1232.set_gain(ADS1232.GAIN_64)
        self.calc_weight = CalcWeight(nom_load, nom_output, full_scale_volt, ADS1232.GAIN_VALUES[ADS1232.GAIN_64-1])
        file_path = path.abspath('WeightSense.py').rstrip('WeightSense.py') + 'load_cells_calibration.yaml'
        self.calibration = LoadCellsZeroCalibration(file_path, N_SAMPLES)
        self.calibration.load_from_yaml()

    def calibrate_zero(self, channel):
        """
        Calibrates the offset weight for the sensor by calling LoadCellsCalibration routines
        :return: None
        """
        log.info("Starting calibration")
        while not self.calibration.is_calibration_over():
            if load_cells.is_ready():
                sample = self.ads1232.analog_read(channel)
                log.info(f'Sample: {sample}')
                self.calibration.input_calibration_sample(sample)
        log.info("Calibration ended, saving to yaml")
        self.calibration.compute_calibration_data(channel)
        self.calibration.save_to_yaml()

    def get_weight(self, channel):
        """
        Returns the last weight reading in gr of the designated load cell.
        """
        adc_read = self.ads1232.analog_read(channel)
        weight = self.calc_weight.perform(adc_read - self.calibration.get_zero(channel))
        # weight = self._calc_weight(adc_read - self.calibration.get_zero(channel))
        return weight

    def set_channel(self, channel):
        """
        Sets the channel on which to perform measurements
        :param channel: selected channel
        :return: none
        """
        self.ads1232.set_channel(channel)

    def get_all_weights(self):
        """
        Returns a list with the weight readings in gr of all the load cells.
        """
        weights_list = []
        for adc_read in self.ads1232.analog_read_all():
            weights_list.append(self._calc_weight(adc_read))
        return weights_list

    def get_weights_list(self, channel_list):
        return [{channel:self.get_weight(channel)} for channel in channel_list]

    @staticmethod
    def _calc_weight(adc_read):
        return adc_read

    def is_ready(self):
        return self.ads1232.is_ready()

if __name__ == '__main__':
    """
    This demo tests the ADCLoadCells Module
    """
    import time
    import logging
    log.setLevel(logging.INFO)
    load_cells = WeightSense(NOMINAL_LOAD, NOMINAL_OUTPUT ,FULL_SCALE_VOLT)
    # load_cells.calibrate_zero(ADS1232.CHANNEL_0)
    while True:
        if load_cells.is_ready():
            log.info(f'CH{ADS1232.CHANNEL_0} weight is: {load_cells.get_weight(ADS1232.CHANNEL_0)}')
            time.sleep(0.05)
