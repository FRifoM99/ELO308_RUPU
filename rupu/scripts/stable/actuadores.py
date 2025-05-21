# coding=utf-8
# Función de motor  
import configuracion
from numpy import interp
import pigpio

pi = configuracion.pi


def motor(velocidadMotorIzq, velocidadMotorDer):
    """
    Controla la velocidad y dirección de los motores.

    Parámetros:
    velocidad_motor_izq (int): Velocidad del motor izquierdo (-1024 a 1024).
    velocidad_motor_der (int): Velocidad del motor derecho (-1024 a 1024).

    Nota:
    - Valores negativos indican movimiento en reversa.
    - Los valores se limitan al rango permitido por `configuracion.resolucionPWM`.
    """

    if velocidadMotorDer >= configuracion.resolucionPWM:
        velocidadMotorDer = configuracion.resolucionPWM
    elif velocidadMotorDer <= -configuracion.resolucionPWM:
        velocidadMotorDer = -configuracion.resolucionPWM

    if velocidadMotorIzq >= configuracion.resolucionPWM:
        velocidadMotorIzq = configuracion.resolucionPWM
    elif velocidadMotorIzq <= -configuracion.resolucionPWM:
        velocidadMotorIzq = -configuracion.resolucionPWM

    if velocidadMotorDer > 0:
        run_motor(0, velocidadMotorDer, 0)
    elif velocidadMotorDer < 0:
        run_motor(0, -velocidadMotorDer, 1)
    else:
        run_motor(0, 0, 0)

    if velocidadMotorIzq > 0:
        run_motor(1, velocidadMotorIzq, 0)
    elif velocidadMotorIzq < 0:
        run_motor(1, -velocidadMotorIzq, 1)
    else:
        run_motor(1, 0, 0)


def run_motor(motor, vel, direccion):
    """
    Controla un motor individual.

    Parámetros:
    motor (int): Identificador del motor (0: derecho, 1: izquierdo).
    velocidad (int): Velocidad del motor (0 a 1024).
    direccion (int): Dirección del motor (0: adelante, 1: reversa).
    """
    in1 = pigpio.LOW
    in2 = pigpio.HIGH

    if vel == 0:
        # Apagar motor
        pi.write(configuracion.AIN1, 0)
        pi.write(configuracion.AIN2, 0)
        pi.write(configuracion.BIN1, 0)
        pi.write(configuracion.BIN2, 0)
        pi.set_PWM_dutycycle(configuracion.PWMA, 0)
        pi.set_PWM_dutycycle(configuracion.PWMB, 0)
    else:
        # Ajustar dirección
        if direccion == 1:
            in1, in2 = pigpio.HIGH, pigpio.LOW

        # Motor derecho
        if motor == 0:
            pi.write(configuracion.AIN1, in1)
            pi.write(configuracion.AIN2, in2)
            pi.set_PWM_dutycycle(configuracion.PWMA, vel * (255 / configuracion.resolucionPWM))
        # Motor izquierdo
        elif motor == 1:
            pi.write(configuracion.BIN1, in2)
            pi.write(configuracion.BIN2, in1)
            pi.set_PWM_dutycycle(configuracion.PWMB, vel * (255 / configuracion.resolucionPWM))
