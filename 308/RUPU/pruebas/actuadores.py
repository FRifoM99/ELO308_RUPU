# coding=utf-8
#  Función de motor  
from time import sleep
from gpiozero import PWMOutputDevice, DigitalOutputDevice
import configuracion

from numpy import interp

global pwma
global pwmb
pwma = PWMOutputDevice(configuracion.PWMA, frequency=configuracion.freqPWM, initial_value = 0)	#se crea la instancia PWM con frecuencia de 500 Hz
pwmb = PWMOutputDevice(configuracion.PWMB, frequency=configuracion.freqPWM, initial_value = 0)

# pwma.value = 0	#se inicia el PWM con dutycicle de 0
# pwmb.value = 0



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
		
		
		
def runMotor(motor, vel, direccion): #motor 0: derecha
	in1 = False
	in2 = True
	
	if(vel == 0):
		configuracion.AIN1.off()
		configuracion.AIN2.off()
		configuracion.BIN1.off()
		configuracion.BIN2.off()
		pwma.value(0)
		pwmb.value(0)
		
	else:
		if(direccion == 1):	#direccion inversa
			in1 = True
			in2 = False

		if (motor == 0):	#motor derecho
			configuracion.AIN1.value = in1
			configuracion.AIN2.value = in2
			vel = vel /configuracion.resolucionPWM		#se realiza el mapeo de 0-1024 (resolucionPWM) a 0-100
			pwma.ChangeDutyCycle(vel)

		elif (motor == 1):	#motor izquierdo
			configuracion.BIN1.value = in2
			configuracion.BIN2.value = in1
			vel = vel /configuracion.resolucionPWM		#se realiza el mapeo de 0-1024 (resolucionPWM) a 0-100
			pwmb.ChangeDutyCycle(vel)
