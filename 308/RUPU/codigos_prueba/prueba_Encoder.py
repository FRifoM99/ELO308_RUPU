import Encoder
import RPi.GPIO as GPIO
import time
# from cmath import pi


import csv

# Define el archivo CSV y la lista de datos
nombre_archivo = 'datos.csv'
texto = open(nombre_archivo, 'w')
texto.write('velocidades'+'\n')
texto.close()
# Función para guardar los datos en el CSV




GPIO.setmode(GPIO.BOARD) 

encoder1D=19
encoder2D=21
encoder1L=23
encoder2L=24

GPIO.setup(encoder1D, GPIO.IN)
GPIO.setup(encoder2D, GPIO.IN)
GPIO.setup(encoder1L, GPIO.IN)
GPIO.setup(encoder2L, GPIO.IN)


encoderD = Encoder.Encoder(encoder1D,encoder2D)
encoderL = Encoder.Encoder(encoder2L,encoder1L)

t_svel = 0

for i in range(100000):
    t_actual = time.time() - t_svel
    if(t_actual >= 0.01):
        v_r=(2*3.14159*2*encoderD.read()*0.01)/(t_actual*28); # ENCODERS:28CPR---CAJA_REDUCTORA:100:1  [cm/s]
        v_l=(2*3.14159*2*encoderL.read()*0.01)/(t_actual*28); # ENCODERS:28CPR---CAJA_REDUCTORA:100:1  [cm/s]
        t_svel = time.time()
        encoderD.write(0)
        encoderL.write(0)
    Input_vel=0.5*(v_r+v_l)*3
    texto = open(nombre_archivo, 'a')
    texto.write(str(Input_vel)+'\n')

    print(str(i) + str(encoderD.read()) + '----' + str(encoderL.read()) + '----' + str(Input_vel)) 
texto.close()
