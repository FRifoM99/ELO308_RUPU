
#FUNCIONANDO OK
from time import sleep
import sys
import os
import RPi.GPIO as GPIO
import ADS1x15
import time


GPIO.setmode(GPIO.BOARD)


#Definiciones
SIGNAL=29
S0=31
S1=33
S2=35
S3=37
channel = 1
address= 0x48
GAIN = 2/3
sps = 3300

ADS = ADS1x15.ADS1115(1, 0x48)

print(os.path.basename(__file__))
print("ADS1X15_LIB_VERSION: {}".format(ADS1x15.__version__))

ADS.setGain(ADS.PGA_6_144V)
ADS.setDataRate(ADS.DR_ADS111X_860)
# ADS.setMode(ADS.MODE_CONTINUOUS)
# ADS.requestADC(0)     

# ADS.setComparatorThresholdLow(0X8000)    # 1.5V
# ADS.setComparatorThresholdHigh(0X7FFF)

GPIO.setup(S0, GPIO.OUT)
GPIO.setup(S1, GPIO.OUT)
GPIO.setup(S2, GPIO.OUT)
GPIO.setup(S3, GPIO.OUT)


def main(args=None):
	values = [0]*16
	maximo = [0]*16
	minimo = [32000]*16
	print("calibrando!")
	for i in range (50):
		for s in range(16):
			GPIO.output(S0, s&0x01) # 0001
			GPIO.output(S1, s&0x02) # 0010
			GPIO.output(S2, s&0x04) # 0100
			GPIO.output(S3, s&0x08) # 1000
			valor = ADS.readADC(0)
			maximo[s] = valor if (valor > maximo[s]) else (maximo[s])
			minimo[s] = valor if (valor < minimo[s]) else (minimo[s])
			sleep(0.01)
	print(maximo)
	print(minimo)
	while True:
		t_inicio = time.time()
		for s in range(16):
			GPIO.output(S0, s&0x01) # 0001
			GPIO.output(S1, s&0x02) # 0010
			GPIO.output(S2, s&0x04) # 0100
			GPIO.output(S3, s&0x08) # 1000
			# values[s] = adc.read_adc(0, gain=GAIN, data_rate = 860)
			values[s] = round(((1-2*1)*100*(ADS.readADC(0)-minimo[s])/(maximo[s] - minimo[s])) + 100*1, 2)
			rango = maximo[s] - minimo[0]
			# th_h = maximo[s] - rango*0.5
			# th_l = minimo[s] + rango*0.5
			# values[s] = 0 if (values[s] >= th_h) else 1
			# sleep(0.01)
		t_final = time.time() - t_inicio
		print(t_final)
		print("-------------------------------------------------------------------------")		
		print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} |'.format(*values))
		print("|                                                                       |")
		print("|                                                                       |")
		print('| {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} | {13:>6} | {14:>6} | {15:>6} |'.format(*values))
		print("-------------------------------------------------------------------------")
		# sleep(0.02)

if __name__ == "__main__":
    main()
