class ADS1018Consts():
    STOP = 0
    START_NOW = 1  # Start of conversion in single-shot mode
    # Input multiplexer configuration used by "MUX" bits
    DIFF_0_1 = 0b000  # Differential input: Vin=A0-A1
    DIFF_0_3 = 0b001  # Differential input: Vin=A0-A3
    DIFF_1_3 = 0b010  # Differential input: Vin=A1-A3
    DIFF_2_3 = 0b011  # Differential input: Vin=A2-A3
    AIN_0 = 0b100  # Single ended input: Vin=A0
    AIN_1 = 0b101  # Single ended input: Vin=A1
    AIN_2 = 0b110  # Single ended input: Vin=A2
    AIN_3 = 0b111  # Single ended input: Vin=A3
    # Full scale range (FSR) selection by "PGA" bits
    FSR_6144 = 0b000  # Range: ±6.144 v. LSB SIZE = 3mV
    FSR_4096 = 0b001  # Range: ±4.096 v. LSB SIZE = 2mV
    FSR_2048 = 0b010  # Range: ±2.048 v. LSB SIZE = 1mV ***DEFAULT
    FSR_1024 = 0b011  # Range: ±1.024 v. LSB SIZE = 0.5mV
    FSR_0512 = 0b100  # Range: ±0.512 v. LSB SIZE = 0.25mV
    FSR_0256 = 0b111  # Range: ±0.256 v. LSB SIZE = 0.125mV
    # Used by "MODE" bit
    CONTINUOUS = 0  # Continuous conversion mode
    SINGLE_SHOT = 1  # Single-shot conversion and power down mode
    # Sampling rate selection by "DR" bits
    # Warning: this could increase the noise and the effective number of bits (ENOB)
    RATE_128SPS = 0b000  # 128 samples/s, Tconv=125ms
    RATE_250SPS = 0b001  # 250 samples/s, Tconv=62.5ms
    RATE_490SPS = 0b010  # 490 samples/s, Tconv=31.25ms
    RATE_920SPS = 0b011  # 920 samples/s, Tconv=15.625ms
    RATE_1600SPS = 0b100  # 1600 samples/s, Tconv=7.8125ms ***DEFAULT
    RATE_2400SPS = 0b101  # 2400 samples/s, Tconv=4ms
    RATE_3300SPS = 0b110  # 3300 samples/s, Tconv=2.105ms
    # Used by "TS_MODE" bit
    ADC_MODE = 0  # External (inputs) voltage reading mode ***DEFAULT
    TEMP_MODE = 1  # Internal temperature sensor reading mode
    # Used by "PULL_UP_EN" bit
    INT_PULLUP = 1  # Internal pull-up resistor enabled for DOUT ***DEFAULT
    NO_PULLUP = 0  # Internal pull-up resistor disabled
    # Used by "NOP" bit
    VALID_CFG = 0b01  # Data will be written to Config register
    NO_VALID_CFG = 0b00  # Data won't be written to Config register
    # Used by "Reserved" bit
    RESERVED = 1  # Its value is always 1, reserved
    PGA_FSR = [3, 2, 1, 0.5, 0.25, 0.125, 0.125, 0.125]  #
    CONV_TIME = [125, 63, 32, 16, 8, 4, 3, 2]  # Array containing the conversions time in ms
    N_MUX_INPUTS = 84
    N_BYTES_READ = 4