from piratslib.components.GPIO_In.GPIOIn import GPIOIn
from piratslib.components.GPIO_Out.GPIOOut import GPIOOut

class DigitalInputSense():
    """
    Class to abstract and interface with the GPIO Inputs of the PI-Rats Boards
    """
    ADDRESS_GPIO_ZERO_MCP = 0
    ADDRESS_GPIO_IN_MCP = 1
    def __init__(self):
        self.gpio_in = GPIOIn(DigitalInputSense.ADDRESS_GPIO_IN_MCP)
        self.gpio_zero = GPIOOut(DigitalInputSense.ADDRESS_GPIO_ZERO_MCP)
        self.gpio_zero.write_gpio(0xFFFFF)
        self.gpio_zero.write_gpio(0x00000)
        self.gpio_zero.write_gpio(0xFFFFF)

    def digital_read(self, input_pin):
        """
        Returns the digital state of the designated GPIO_PIN
        :param input_pin:
        :return:
        """
        return self.gpio_in.digital_read(input_pin)

    def digital_read_all(self):
        """
        Returns the values of all the digital pins in teh GPIO
        :return:
        """
        return self.gpio_in.digital_read_all()



if __name__ == "__main__":
    from piratslib.common.logger import log
    import logging
    import time
    digital_input_sense = DigitalInputSense()
    log.setLevel(logging.INFO)
    while True:
        log.info(digital_input_sense.digital_read_all())
        time.sleep(0.5)
