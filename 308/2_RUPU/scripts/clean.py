import spidev
import RPi.GPIO as GPIO
import time

spi = spidev.SpiDev()
spi.open(1, 0)  # Use SPI1, device 0

GPIO.cleanup()
spi.close()