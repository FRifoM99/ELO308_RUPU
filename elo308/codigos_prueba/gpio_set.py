import RPi.GPIO as GPIO

try:
    GPIO.cleanup()  # Reset GPIO settings
    GPIO.setmode(GPIO.BOARD)  # Attempt to set the GPIO mode
    print("GPIO mode set successfully.")
except Exception as e:
    print(f"Error: {e}")
finally:
    GPIO.cleanup()  # Always clean up
