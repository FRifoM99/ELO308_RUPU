import spidev
import RPi.GPIO as GPIO
import time

# Pin setup using BOARD mode (Physical Pins)
CS1_PIN = 29  # Physical Pin 29 (for MCP3208 #1, channels 0-7)
CS2_PIN = 22   # Physical Pin 7 (for MCP3208 #2, channels 8-15)

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)  # Use BOARD mode
GPIO.setwarnings(False)   # Suppress GPIO warnings
GPIO.setup(CS1_PIN, GPIO.OUT)
GPIO.setup(CS2_PIN, GPIO.OUT)

# Set CS pins to high (inactive) initially
GPIO.output(CS1_PIN, GPIO.HIGH)
GPIO.output(CS2_PIN, GPIO.HIGH)

# Initialize SPI on bus 1
spi = spidev.SpiDev()
spi.open(1, 0)  # Use SPI1, device 0
spi.max_speed_hz = 1500000

# Function to read ADC value from MCP3208 on a given channel and CS pin
def read_adc(channel, cs_pin):
    if channel < 0 or channel > 7:
        raise ValueError("Channel must be between 0 and 7")

    # Select the device by pulling its CS pin low
    GPIO.output(cs_pin, GPIO.LOW)
    adc = spi.xfer([6 | (channel & 4) >> 2, (channel & 3) << 6, 0])
    data = ((adc[1] & 15) << 8) + adc[2]
    GPIO.output(cs_pin, GPIO.HIGH)

    # return value
    return data

# Main function
def main():
    values = [0] * 16  # Array to store 16 channels (8 from each MCP3208)
    maximo = [0] * 16  # Array to store maximum values for each channel
    minimo = [4095] * 16  # Array to store minimum values (initialized to max ADC value 4095 for 12-bit)

    print("Calibrando...")  # Calibration phase
    for i in range(50):
        for ch in range(16):
            if ch < 8:
                valor = read_adc(ch, CS1_PIN)  # Read from MCP3208 #1 (channels 0-7)
            else:
                valor = read_adc(ch - 8, CS2_PIN)  # Read from MCP3208 #2 (channels 8-15)
            
            # Update max and min values for calibration
            maximo[ch] = max(valor, maximo[ch])
            minimo[ch] = min(valor, minimo[ch])
            time.sleep(0.01)
    
    print("Máximos:", maximo)
    print("Mínimos:", minimo)

    # Main loop to read values and perform math operations
    try:
        while True:
            t_inicio = time.time()  # Start time for measurement
            
            for ch in range(16):
                if ch < 8:
                    valor = read_adc(ch, CS1_PIN)  # Read from MCP3208 #1
                else:
                    valor = read_adc(ch - 8, CS2_PIN)  # Read from MCP3208 #2
                
                # Perform scaling and math operations based on calibration
                if maximo[ch] != minimo[ch]:  # Prevent division by zero
                    values[ch] = valor
                    # values[ch] = round(((1 - 2 * 1) * 100 * (valor - minimo[ch]) / (maximo[ch] - minimo[ch])) + 100 * 1, 2)
                else:
                    values[ch] = 0  # Fallback if min and max are equal

            t_final = time.time() - t_inicio  # Calculate elapsed time

            # Print formatted results 
            print(t_final)
            print("-------------------------------------------------------------------------")
            print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} |'.format(*values[:8]))
            print("|                                                                       |")
            print("|                                                                       |")
            print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} |'.format(*values[8:]))
            print("-------------------------------------------------------------------------")
            
            time.sleep(0.02)  # Delay for stability

    except KeyboardInterrupt:
        # Cleanup GPIO and SPI on exit
        GPIO.cleanup()
        spi.close()

if __name__ == "__main__":
    main()
