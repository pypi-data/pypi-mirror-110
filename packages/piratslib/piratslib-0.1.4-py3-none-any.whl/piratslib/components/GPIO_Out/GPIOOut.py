from piratslib.common.BaseClasses import DigitalOut
from piratslib.common.logger import log as log

class GPIOOut(DigitalOut):
    """
    Provides 16 optocoupled general purpose outputs using an MCP23S17 connected to the SPI Bus
    """
    def __init__(self, address):
        super().__init__(address)
        self.setup(self._mcp.DIR_OUTPUT)

    def digital_write(self, output_number, value):
        """
        Writes a digital value onto the designated output.
        """
        self._mcp.digitalWrite(output_number, value)

    def digital_write_for_all(self, values_list):
        """
        Writes a list with digital value for each of the 16 outputs.
        """
        for pin_number,value in enumerate(values_list):
            self._mcp.digitalWrite(pin_number, value)

    def digital_write_to_all(self, value):
        """
        Writes the same digital value for all the 16 outputs.
        """
        self._mcp.writeGPIO(value)

if __name__ == '__main__':
    import time
    """
    This demo tests the GPIOOut Module
    """
    import logging

    log.setLevel(logging.INFO)
    ADDRESS_GPIO_ZERO_MCP = 0
    ADDRESS_GPIO_OUT_MCP = 2
    gpio_out = GPIOOut(ADDRESS_GPIO_OUT_MCP)
    gpio_zero = GPIOOut(ADDRESS_GPIO_ZERO_MCP)
    gpio_zero.write_gpio(0xFFFFF)
    gpio_zero.write_gpio(0x00000)
    gpio_zero.write_gpio(0xFFFFF)
    while(True):
        gpio_out.digital_write_to_all(0)
        log.info("ALL OUTPUTS OFF")
        time.sleep(1)
        gpio_out.digital_write_to_all(65535)
        log.info("ALL OUTPUTS ON")
        time.sleep(1)
        # for input_number in range(0, gpio_out.N_PORTS):
        #     gpio_out.digital_write_to_all(0)
        #     gpio_out.digital_write(input_number,True)
        #     print(f'Pin #{input_number} is ON')
        #     time.sleep(1)
