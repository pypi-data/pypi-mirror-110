import yaml
from piratslib.common.logger import log
import numpy as np
import scipy.ndimage


class LoadCellsZeroCalibration:
    """
    Class to manage the Calibration of LoadCells. Maintains a yaml file to store the calibrated data
    """
    def __init__(self, data_file_name, calibration_samples = 100):
        self.data_file_name = data_file_name
        self.calibration_samples = calibration_samples
        self.calibration_array = np.zeros(calibration_samples)
        self.current_sample_idx = 0
        self.calibration_data = {'CH0':0, 'CH1':0}

    def get_zero(self, channel):
        """
        Returns zero value for the desired channel.
        :param channel:
        :return:
        """
        return self.calibration_data[f'CH{channel}']

    def input_calibration_sample(self, calibration_sample):
        """
        When calibrating zero, used to input a new sample onto the calibration array
        :param calibration_sample:
        :return:
        """
        log.info(f'Current sample index: {self.current_sample_idx}')
        self.calibration_array[self.current_sample_idx] = calibration_sample
        self.current_sample_idx += 1

    def is_calibration_over(self):
        """
        Returns true when the zero calibration is over as index has gone over the top
        :return:
        """
        return not self.current_sample_idx < self.calibration_samples

    def compute_calibration_data(self, channel):
        """
        Computes the zero calibration data
        :param channel:
        :return:
        """
        self.calibration_array = scipy.ndimage.median_filter(self.calibration_array, self.calibration_samples)
        calibration_result = np.average(self.calibration_array)
        calibration_result = int(calibration_result)
        log.info(calibration_result)
        self.calibration_data[f'CH{channel}'] = calibration_result
        log.info(f'Calibration data: {self.calibration_data}')


    def save_to_yaml(self):
        """
        Saves the zero data into the yaml file
        :return:
        """
        with open(self.data_file_name, 'w') as file:
            documents = yaml.dump(self.calibration_data, file)
            log.info(documents)
            log.info('Successfully written to file!')

    def load_from_yaml(self):
        """
        Retrieves the stored zero data in the yaml file
        :return:
        """
        with open(self.data_file_name ) as file:
            self.calibration_data = yaml.load(file, Loader=yaml.FullLoader)
            log.info('Successfully load from file!')


if __name__ == '__main__':
    import logging
    log.setLevel(logging.INFO)
    calibration = LoadCellsZeroCalibration('load_cells_calibration.yaml')
    print(calibration.load_from_yaml())
    calibration.save_to_yaml()
