from gpiozero import RotaryEncoder
from time import sleep

# Configura el encoder en el pin adecuado (pin A)
# Aquí suponemos que usas BOARD, debes pasar el pin GPIO correspondiente
encoder = RotaryEncoder(a=8, b=11, max_steps=0)  # Ajusta el pin 'a' según tu configuración

def get_position():
    """Devuelve la posición actual del encoder."""
    return encoder.steps

try:
    while True:
        # Lee y muestra la posición del encoder
        print(f"Posición actual: {get_position()}")
        sleep(0.1)  # Añade un pequeño retardo para evitar saturar el CPU
except KeyboardInterrupt:
    print("Script detenido")
