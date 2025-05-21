# coding=utf-8
#   presenta todas las configuraciones estables de pines    #
from gpiozero import PWMOutputDevice, DigitalOutputDevice, DigitalInputDevice, RotaryEncoder
# import Encoder

global PWMA, AIN2, AIN1, BIN1, BIN2, PWMB   #definicion pines motor
global encoder1D, encoder2D, encoder1L, encoder2L   #definicion pines encoder
global resolucionPWM
global N    #modulo de reduccion
global CPR  #cuentas por revolucion
global l    #distancia en cm entre las ruedas
global linea    # 0 = linea negra; 1 = linea blanca
global radioRueda   #radio de la rueda en cm
global d1   #distancia entre el eje de giro y el centro del sensor IR de delante
global d2   #distancia entre el eje de giro y el centro del sensor IR de atras

PWMA = 18
AIN2 = DigitalOutputDevice(24)
AIN1 = DigitalOutputDevice(23)
BIN1 = DigitalOutputDevice(22)
BIN2 = DigitalOutputDevice(27)
PWMB = 17
# encoder1D=DigitalInputDevice(10)
# encoder2D=DigitalInputDevice(9)
# encoder1L=DigitalInputDevice(11)
# encoder2L=DigitalInputDevice(8) 
resolucionPWM = 1023    #asi llamada resolucion, es el valor maximo que genera el controlador
N = 0.01 
CPR = 28 
l = 5.6 
linea = 1 
radioRueda = 2
d1=52
d2=32

global freqPWM  #frecuencia pwm
freqPWM=500 

global SIGNAL, S0, S1, S2, S3   #definicion de pines del multiplexor
global channel, address #constantes para I2C
global GAIN, offsetSensorD  #constantes sensores I2C
SIGNAL=5
S0=6 
S1=13
S2=19
S3=26
channel = 1
address= 0x48
GAIN = 2/3
offsetSensorD=4.0
sps = 860

count = [0]*5
#   configuracion GPIO

# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)
# GPIO.setup(PWMA, GPIO.OUT) 
# GPIO.setup(PWMB, GPIO.OUT) 
# GPIO.setup(AIN1, GPIO.OUT) 
# GPIO.setup(AIN2, GPIO.OUT) 
# GPIO.setup(BIN1, GPIO.OUT) 
# GPIO.setup(BIN2, GPIO.OUT) 
# GPIO.setup(encoder1D, GPIO.IN)
# GPIO.setup(encoder2D, GPIO.IN)
# GPIO.setup(encoder1L, GPIO.IN)
# GPIO.setup(encoder2L, GPIO.IN)
# GPIO.setup(S0, GPIO.OUT)
# GPIO.setup(S1, GPIO.OUT)
# GPIO.setup(S2, GPIO.OUT)
# GPIO.setup(S3, GPIO.OUT)

#   Contruccion de encoder
encoderD = RotaryEncoder(a=9, b=10, max_steps=0)
encoderL = RotaryEncoder(a=11, b=8, max_steps=0)

#constantes de referencia
global theta_ref, vel_ref, sat_theta, sat_vel, sat_d
theta_ref = 0         #quiero que este justo al centro
vel_ref = 5            #velocidad de referencia
d_ref = 10				#20 cm
sat_theta=1023
sat_vel=1023
sat_d=1023

#declaracion de ip
global monitor, lider, seguidor1, seguidor2, seguidor3, bufferSize
monitor = ("10.2.51.226", 1234)   #ip y puerto pc windows
#lider = ("192.168.100.18", 1111)    #ip y puerto de la raspberry
seguidor1 = ("192.168.100.20", 1111)   #ip y puerto del robot sucesor 
seguidor2 = ("192.168.100.22", 1111)   #ip y puerto del robot sucesor 
seguidor3 = ("192.168.100.18", 1111)   #ip y puerto del robot sucesor 
lider = ("192.168.100.23", 1111)  
seguidor4 = ("192.168.100.26", 1111)  	#PRUEBA CON ESP <-----------------
bufferSize = 1024
