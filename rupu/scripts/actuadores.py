# coding=utf-8
 
from time import sleep
import configuracion
from numpy import interp
import pigpio

pi = configuracion.pi

# global pwma
# global pwmb
# pwma = GPIO.PWM(configuracion.PWMA, configuracion.freqPWM)	#se crea la instancia PWM con frecuencia de 500 Hz
# pwmb = GPIO.PWM(configuracion.PWMB, configuracion.freqPWM)

# pwma.start(0)	#se inicia el PWM con dutycicle de 0
# pwmb.start(0)



def motor (velocidadMotorIzq, velocidadMotorDer):

	#Función de motor motor(M1, M2).
	#Mueve los motores con velocidad M1 y M2 con un valor entero entre 0 y 1024
	#En caso de introducir un número negativo, el motor se mueve en sentido inverso.
	
	if (velocidadMotorDer >= configuracion.resolucionPWM):
		velocidadMotorDer=configuracion.resolucionPWM
	elif (velocidadMotorDer <= - configuracion.resolucionPWM):
		velocidadMotorDer=-configuracion.resolucionPWM
	if(velocidadMotorIzq >= configuracion.resolucionPWM):
		velocidadMotorIzq=configuracion.resolucionPWM
	elif (velocidadMotorIzq <= - configuracion.resolucionPWM):
		velocidadMotorIzq=-configuracion.resolucionPWM
		
	
	if(velocidadMotorDer>0):
		runMotor(0,velocidadMotorDer,0)
	elif (velocidadMotorDer<0):
		runMotor(0,-velocidadMotorDer,1)
	else:
		runMotor(0,0,0)
	
	if(velocidadMotorIzq>0):
		runMotor(1,velocidadMotorIzq,0)
	elif (velocidadMotorIzq<0):
		runMotor(1,-velocidadMotorIzq,1)
	
	else:
		runMotor(1,0,0)
		
		
		
def runMotor(motor, vel, direccion):
    """
    Controla un motor individual, con direccion 0 para adelante y 1 para reversa.
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