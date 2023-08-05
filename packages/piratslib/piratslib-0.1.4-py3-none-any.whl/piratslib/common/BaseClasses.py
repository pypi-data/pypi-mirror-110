from abc import ABC, abstractmethod
from piratslib.components.MCP_23S17.MCP23S17 import MCP23S17

class GPIO():
    N_PORTS = 16
    BUS = 1
    DEVICE = 0
    SPI_MODE = 0
    def __init__(self, address):
        self._mcp = MCP23S17(bus=GPIO.BUS, pin_cs=GPIO.DEVICE, pin_reset=-1, device_id=address)

    def setup(self, mode):
        """
        Initializes the module and communication with the chip, called in the instantiation of the object.
        """
        self._mcp.open()
        for pin_number in range(0, GPIO.N_PORTS):
            self._mcp.setDirection(pin_number, mode)

    def write_gpio(self, value):
        """
        Writes a raw value to the output register
        """
        self._mcp.writeGPIO(value)

    def write_register(self, register, value):
        """
        Writes a raw value to the designated register
        """
        self._mcp._writeRegister(register, value)

class DigitalIn(GPIO, ABC):
    @abstractmethod
    def digital_read(self, input_number):
        pass
    @abstractmethod
    def digital_read_all(self):
        pass

class DigitalOut(GPIO, ABC):
    @abstractmethod
    def digital_write(self, output_number, value):
        pass
    @abstractmethod
    def digital_write_to_all(self, value):
        pass
    @abstractmethod
    def digital_write_for_all(self, values_list):
        pass

class ADC(ABC):
    @abstractmethod
    def setup(self):
        pass
    @abstractmethod
    def analog_read(self, input_number):
        pass
    @abstractmethod
    def analog_read_all(self):
        pass
