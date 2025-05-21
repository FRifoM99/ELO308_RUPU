#!/usr/bin/env python

import pigpio

class Encoder:

    """Clase para decodificar pulsos de un encoder de cuadratura mecánico."""

    def __init__(self, pi, gpioA, gpioB, callback):
        """
        Inicializa la clase con la instancia `pi` de pigpio y los pines GPIO
        conectados a los contactos A y B del encoder rotativo. El contacto común 
        debe estar conectado a tierra. `callback` es la función que se llama 
        cuando el encoder rota. Esta función recibe un parámetro: +1 para giro 
        en sentido horario y -1 para giro antihorario.
        """
        self.pi = pi
        self.gpioA = gpioA
        self.gpioB = gpioB
        self.callback = callback

        # Niveles iniciales de los pines A y B
        self.levA = 0
        self.levB = 0

        # Último pin que cambió
        self.lastGpio = None

        # Configuración de los pines como entradas con pull-up
        self.pi.set_mode(gpioA, pigpio.INPUT)
        self.pi.set_mode(gpioB, pigpio.INPUT)
        self.pi.set_pull_up_down(gpioA, pigpio.PUD_UP)
        self.pi.set_pull_up_down(gpioB, pigpio.PUD_UP)

        # Callbacks para ambos pines A y B
        self.cbA = self.pi.callback(gpioA, pigpio.EITHER_EDGE, self._pulse)
        self.cbB = self.pi.callback(gpioB, pigpio.EITHER_EDGE, self._pulse)

    def _pulse(self, gpio, level, tick):
        """
        Decodifica el pulso del encoder rotativo, incrementando o decrementando el 
        contador de pasos según la dirección del giro.
        """
        if gpio == self.gpioA:
            self.levA = level
        else:
            self.levB = level

        # Comprobar si el pin actual es diferente al último que cambió para evitar rebotes
        if gpio != self.lastGpio:
            self.lastGpio = gpio

            # Determinar la dirección según el estado de A y B
            if gpio == self.gpioA and level == 1:  # Flanco ascendente en A
                if self.levB == 1:
                    self.callback(1)  # Sentido horario
            elif gpio == self.gpioB and level == 1:  # Flanco ascendente en B
                if self.levA == 1:
                    self.callback(-1)  # Sentido antihorario

    def cancel(self):
        """
        Cancela el decodificador del encoder rotativo y detiene los callbacks.
        """
        self.cbA.cancel()
        self.cbB.cancel()
