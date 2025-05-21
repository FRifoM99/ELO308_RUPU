from gpiozero import RotaryEncoder
from time import sleep

# Configura los pines del encoder (GPIO, no BOARD)
A_PIN = 11  # Cambia al GPIO correspondiente para el pin A
B_PIN = 8  # Cambia al GPIO correspondiente para el pin B

# Inicializa el encoder
encoder = RotaryEncoder(a=A_PIN, b=B_PIN, max_steps=0, wrap=False)

# Variable para almacenar la posición anterior y detectar cambios
previous_position = 0

# Función para imprimir la posición actual del encoder
def print_position():
    global previous_position
    current_position = encoder.steps
    
    if current_position != previous_position:
        if current_position > previous_position:
            print(f"Encoder movido en dirección positiva, posición actual: {current_position}")
        else:
            print(f"Encoder movido en dirección negativa, posición actual: {current_position}")
        previous_position = current_position

# Callback para cuando el encoder detecta un cambio de rotación
encoder.when_rotated = print_position

try:
    while True:
        sleep(0.1)  # Añade un pequeño retardo para reducir la carga de CPU

except KeyboardInterrupt:
    print("Detenido por el usuario")
