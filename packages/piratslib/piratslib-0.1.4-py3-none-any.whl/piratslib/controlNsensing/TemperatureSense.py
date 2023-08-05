from piratslib.components.ADC_PTC_Array.ADCPTCArray import ADCPTCArray
from piratslib.common.logger import log
import logging

class TemperatureSense():
    """
    Class to abstract and interface with the temperature sensors, the PTC100 array, of the PI-Rats Boards
    """
    def __init__(self):
        self.ptc100_array = ADCPTCArray()

    def get_temp(self, sensor_id):
        """
        Returns the temperature in ºC measured by the designated sensor
        :param sensor_id:
        :return:
        """
        return self.ptc100_array.read_temperature(sensor_id)

    def get_all_temp(self):
        """
        Returns all the temperatures of the array on a list
        :return:
        """
        return self.ptc100_array.read_all_temperatures()

    def get_temps_list(self, channel_list):
        return [{channel:self.get_temp(channel)} for channel in channel_list]

if __name__ == "__main__":

    import time
    log.setLevel(logging.INFO)
    temp_sense = TemperatureSense()
    sens_id = 1
    ch_list = [1,0]
    while True:
        # log.info(f'Temperature on sensor #{sens_id}: {temp_sense.get_temp(sens_id)}ºC')
        # log.info(f'{temp_sense.get_all_temp()}')
        log.info(temp_sense.get_temps_list(ch_list))
        time.sleep(1)
    # for sens_id, temp in enumerate(temp_sense.get_all_temp()):
    #     log.info(f'Temperature on sensor #{sens_id}: {temp_sense.get_temp(sens_id)}ºC')


