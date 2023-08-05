from piratslib.components.GPIO_Out.GPIOOut import GPIOOut

class DigitalOutputControl():
    """
    Class to abstract and interface with the GPIO Outputs of the PI-Rats Boards
    """
    ADDRESS_GPIO_ZERO_MCP = 0
    ADDRESS_GPIO_OUT_MCP = 2

    def __init__(self):
        self.gpio_out = GPIOOut(DigitalOutputControl.ADDRESS_GPIO_OUT_MCP)
        self.gpio_zero = GPIOOut(DigitalOutputControl.ADDRESS_GPIO_ZERO_MCP)
        self.gpio_zero.write_gpio(0xFFFFF)
        self.gpio_zero.write_gpio(0x00000)
        self.gpio_zero.write_gpio(0xFFFFF)

    def digital_write(self, output_pin, value):
        """
        Writes to the output pin the designated digital state
        :param output_pin:
        :param value:
        :return:
        """
        self.gpio_out.digital_write(output_pin, value)

    def digital_write_to_all(self, value):
        """
        Writes the same value to all the digital outputs
        :param value:
        :return:
        """
        self.gpio_out.digital_write_to_all(value)

    def digital_write_for_all(self, values_list):
        """
        Writes a list of digital values corresponding with the digital outputs
        :param values_list:
        :return:
        """
        self.gpio_out.digital_write_for_all(values_list)


if __name__ == "__main__":
    from piratslib.common.logger import log
    import logging
    import time
    digital_output_control = DigitalOutputControl()
    log.setLevel(logging.INFO)
    while True:
        log.info(digital_output_control.digital_write_to_all(True))
        time.sleep(0.5)
        log.info(digital_output_control.digital_write_to_all(False))
        time.sleep(0.5)