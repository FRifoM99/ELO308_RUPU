import RPi.GPIO as GPIO
from time import sleep
import Adafruit_ADS1x15

# Configuración de GPIO
GPIO.setmode(GPIO.BOARD)

# Definiciones de pines
S0 = 31
S1 = 33
S2 = 35
S3 = 37

# Configuración de pines GPIO
GPIO.setup(S0, GPIO.OUT)
GPIO.setup(S1, GPIO.OUT)
GPIO.setup(S2, GPIO.OUT)
GPIO.setup(S3, GPIO.OUT)

# Configuración del ADC
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1  # +/- 4.096V

def main(args=None):
    # Configuración inicial de GPIO
    GPIO.output(S0, GPIO.LOW)
    GPIO.output(S1, GPIO.HIGH)
    GPIO.output(S2, GPIO.HIGH)
    GPIO.output(S3, GPIO.LOW)
    
    try:
        while True:
            values = [0] * 4
            # Lectura de los 4 canales del ADC
            for i in range(4):
                values[i] = adc.read_adc(i, gain=GAIN)
            print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
            sleep(0.5)
    except KeyboardInterrupt:
        print("Programa interrumpido por el usuario.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
