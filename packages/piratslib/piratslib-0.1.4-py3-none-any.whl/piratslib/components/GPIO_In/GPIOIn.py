from piratslib.common.BaseClasses import DigitalIn
from piratslib.common.logger import log as log

class GPIOIn(DigitalIn):
    """
    Provides 16 optocoupled general purpose inputs using an MCP23S17 connected to the SPI Bus.
    """
    def __init__(self, address):
        super().__init__(address)
        self.setup(self._mcp.DIR_INPUT)

    def digital_read(self, input_number):
        """
        Returns the reading of the input designated by the input value.
        """
        return self._mcp.digitalRead(input_number)

    def digital_read_all(self):
        """
        Returns a list with the reading of all the 16 inputs.
        """
        return self._mcp.readGPIO ()

    def get_digital_input_list(self, channel_list):
        return [{channel:self.digital_read(channel)} for channel in channel_list]

if __name__ == '__main__':
    """
    This demo tests the GPIOIn Module
    """
    from piratslib.components.GPIO_Out.GPIOOut import GPIOOut
    import time
    import logging
    ADDRESS_GPIO_ZERO_MCP = 0
    ADDRESS_GPIO_IN_MCP = 1
    gpio_in = GPIOIn(ADDRESS_GPIO_IN_MCP)
    gpio_zero = GPIOOut(ADDRESS_GPIO_ZERO_MCP)
    log.setLevel(logging.INFO)
    gpio_zero.write_gpio(0xFFFFF)
    gpio_zero.write_gpio(0x00000)
    gpio_zero.write_gpio(0xFFFFF)
    while(True):
        values = []
        for pin in range(0, gpio_in.N_PORTS):
            values.append(gpio_in.digital_read(pin))
        log.info(f'Reading of all GPIO is: {values}')
        log.info(f'Reading GPIO values is: {gpio_in.digital_read_all() }')
        time.sleep(0.1)