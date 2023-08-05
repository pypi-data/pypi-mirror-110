class CalcWeight():
    """
    Class to manage the parameters and calculate the weight of Load Cells
    """
    def __init__(self, nominal_load, nominal_output, voltage_ref, gain):
        self.nominal_load = nominal_load
        self.nominal_output = nominal_output
        self.voltage_ref = voltage_ref
        self.gain = gain
        self.full_scale_range = self.voltage_ref / self.gain

    def _adc_counts_to_voltage(self, adc_counts):
        volts_per_count = self.full_scale_range / pow(2, 18)
        return adc_counts * volts_per_count

    def perform(self, adc_counts):
        """
        Performs calculation using the parameters
        :param adc_counts: adc counts of sensor
        :return:
        """
        voltage_reading = self._adc_counts_to_voltage(adc_counts)
        weight = ( ( voltage_reading * self.nominal_load ) / ( self.nominal_output * self.voltage_ref ) ) / 9.8
        return weight

if __name__ == "__main__":
    nom_load = 10000
    nom_output = 0.002
    full_scale_volt = 5
    gain = 64
    weight_calc = CalcWeight(nom_load, nom_output, full_scale_volt, gain)
    print(weight_calc.perform(23))
