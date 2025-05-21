# coding=utf-8
#   presenta todas las configuraciones estables de pines    #
import pigpio
from rotary_encoder import Encoder

pi = pigpio.pi()

global PWMA, AIN2, AIN1, BIN1, BIN2, PWMB   #definicion pines motor
global encoder1D, encoder2D, encoder1L, encoder2L   #definicion pines encoder
global resolucionPWM
global N        # Modulo de reduccion
global CPR      # Cuentas por revolucion
global l        # Distancia en cm entre las ruedas
global linea    # 0 = linea negra; 1 = linea blanca
global radioRueda   # Radio de la rueda en cm
global d1       # Distancia entre el eje de giro y el centro del sensor IR de delante
global d2       # Distancia entre el eje de giro y el centro del sensor IR de atras
PWMA = 18
AIN2 = 24
AIN1 = 23
BIN1 = 22
BIN2 = 27
PWMB = 17

encoder1D=10
encoder2D=9
encoder1L=8
encoder2L=11

global freqPWM  # Frecuencia pwm
freqPWM=500 
resolucionPWM = 1023    # Valor maximo que genera el controlador

N = 0.01 
CPR = 7
l = 5.6 
linea = 1 
radioRueda = 2
d1=52
d2=32


global SIGNAL, S0, S1, S2, S3   # Definicion de pines del multiplexor
global channel, address         # Constantes para I2C
global GAIN, offsetSensorD      # Constantes sensores I2C
SIGNAL=29
S0=31 
S1=33
S2=35
S3=37
channel = 1
address= 0x48
GAIN = 2/3
offsetSensorD=4.0
sps = 860

count = [0]*5

#   configuracion GPIO
pi.set_mode(PWMA, pigpio.OUTPUT)
pi.set_mode(PWMB, pigpio.OUTPUT)
pi.set_PWM_frequency(PWMA, freqPWM)
pi.set_PWM_frequency(PWMB, freqPWM)

pi.set_mode(AIN1, pigpio.OUTPUT)
pi.set_mode(AIN2, pigpio.OUTPUT)
pi.set_mode(BIN1, pigpio.OUTPUT)
pi.set_mode(BIN2, pigpio.OUTPUT)

CS1_PIN = 5
CS2_PIN = 25
pi.set_mode(CS1_PIN, pigpio.OUTPUT)
pi.set_mode(CS2_PIN, pigpio.OUTPUT)
pi.write(CS1_PIN, 1)
pi.write(CS2_PIN, 1)


#   Contruccion de encoder
posL = 0
posR = 0
def callbackL(way):
    global posL
    posL += way
def callbackR(way):
    global posR
    posR += way

EncoderL = Encoder(pi, encoder1D, encoder2D, callbackL)
EncoderR = Encoder(pi, encoder1L, encoder2L, callbackR)

#   Constantes de referencia
global theta_ref, vel_ref, sat_theta, sat_vel, sat_d
theta_ref = 0         
vel_ref = 5            
d_ref = 10				
sat_theta=1023
sat_vel=1023
sat_d=1023

# declaracion de ip
global monitor, lider, seguidor1, seguidor2, seguidor3, bufferSize
monitor = ("10.42.0.169", 1234)   #ip y puerto pc windows
#lider = ("192.168.100.18", 1111)    #ip y puerto de la raspberry
seguidor1 = ("10.42.0.4", 1111)   #ip y puerto del robot sucesor 
seguidor2 = ("192.168.100.22", 1111)   #ip y puerto del robot sucesor 
seguidor3 = ("192.168.100.18", 1111)   #ip y puerto del robot sucesor 
lider = ("192.168.100.23", 1111)  
seguidor4 = ("192.168.100.26", 1111)  	#PRUEBA CON ESP <-----------------
bufferSize = 1024
