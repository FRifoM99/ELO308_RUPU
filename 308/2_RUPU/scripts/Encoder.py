import pigpio
import time
class Encoder:
    """
    Optimized Encoder class for handling high-speed rotary encoders
    with pigpio on Raspberry Pi. It uses XOR-based quadrature decoding
    to quickly determine rotation direction and update position.
    """

    def __init__(self, gpio_a, gpio_b, pi):
        self.gpio_a = gpio_a
        self.gpio_b = gpio_b
        self.pi = pi
        self.position = 0
        self.last_state = 0

        # Set pins as inputs
        self.pi.set_mode(self.gpio_a, pigpio.INPUT)
        self.pi.set_mode(self.gpio_b, pigpio.INPUT)

        # Initial state
        self.last_state = (self.pi.read(self.gpio_a) << 1) | self.pi.read(self.gpio_b)

        # Set up callbacks for both rising and falling edges
        self.callback_a = self.pi.callback(self.gpio_a, pigpio.EITHER_EDGE, self._update)
        self.callback_b = self.pi.callback(self.gpio_b, pigpio.EITHER_EDGE, self._update)

    def _update(self, gpio, level, tick):
        # Read the current state of A and B
        state = (self.pi.read(self.gpio_a) << 1) | self.pi.read(self.gpio_b)
        
        # Calculate direction based on state transition
        transition = (self.last_state << 2) | state
        if transition in (0b0001, 0b0111, 0b1110, 0b1000):  # Clockwise
            self.position += 1
        elif transition in (0b0010, 0b0100, 0b1101, 0b1011):  # Counter-clockwise
            self.position -= 1
        
        # Update the last state
        self.last_state = state

    def read(self):
        """Return the current position of the rotary encoder."""
        return self.position

    def write(self, value):
        """Set the encoder position to a specified integer value."""
        if isinstance(value, int):
            self.position = value
        else:
            raise ValueError("Position must be an integer")

    def cancel(self):
        """Cancel callbacks when done."""
        self.callback_a.cancel()
        self.callback_b.cancel()

# Main program for testing
if __name__ == "__main__":
    pi = pigpio.pi()

    # Define GPIO pins for encoder A and B
    gpio_a = 10  # Replace with your GPIO pin for A
    gpio_b = 9  # Replace with your GPIO pin for B

    encoder = Encoder(gpio_a, gpio_b, pi)

    try:
        while True:
            print("Position:", encoder.read())
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")

    encoder.cancel()
    pi.stop()
