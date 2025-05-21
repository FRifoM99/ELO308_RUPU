# coding=utf-8
from cmath import pi
import configuracion
import actuadores
import gl
import VL53L0X

# import Adafruit_ADS1x15
import smbus
# import Encoder
from gpiozero import PWMOutputDevice, DigitalOutputDevice
import time
import numpy as np

import spidev
from gpiozero import PWMOutputDevice, DigitalOutputDevice
import time

i2c = smbus.SMBus(configuracion.channel)
# adc = Adafruit_ADS1x15.ADS1015(busnum = 1)
tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
# adc.start_adc(0, gain=configuracion.GAIN, data_rate=configuracion.sps)
v_r = [0.0]*5
v_l = [0.0]*5
s_r = [0.0]*5
s_l = [0.0]*5
a_s = 0.0
b_s = 0.0
c_s = 0.0
a_sl = 0.0
a_sr = 0.0
b_sl = 0.0
b_sr = 0.0
c_sl = 0.0
c_sr = 0.0
a_curvatura = 0.0
b_curvatura = 0.0
c_curvatura = 0.0


# Pin setup using BOARD mode (Physical Pins)
CS1_PIN = DigitalOutputDevice(29)  # Physical Pin 29 (for MCP3208 #1, channels 0-7)
CS2_PIN = DigitalOutputDevice(22)  # Physical Pin 7 (for MCP3208 #2, channels 8-15)

# Initialize GPIO
# GPIO.setmode(GPIO.BOARD)  # Use BOARD mode
# GPIO.setwarnings(False)   # Suppress GPIO warnings
# GPIO.setup(CS1_PIN, GPIO.OUT)
# GPIO.setup(CS2_PIN, GPIO.OUT)

# Set CS pins to high (inactive) initially
CS1_PIN.on()
CS2_PIN.on()

# Initialize SPI on bus 1



spi = spidev.SpiDev()
spi.open(1, 0)  # Use SPI1, device 0
spi.max_speed_hz = 1000000
spi.mode = 0b00  # Set SPI mode to 0

# Function to read ADC value from MCP3208 on a given channel and CS pin
def read_adc(channel, cs_pin):
    if channel < 0 or channel > 7:
        raise ValueError("Channel must be between 0 and 7")

    cs_pin.off()

    adc = spi.xfer([6 | (channel & 4) >> 2, (channel & 3) << 6, 0])
    data = ((adc[1] & 15) << 8) + adc[2]

    cs_pin.on()

    # return value
    return data



def calibrarSensores():		#calibrar sensores IR
	if(gl.flag_debug):
		print("calibrando")

	vcal = gl.velocidad_calibracion #velocidad del motor para la calibracion
	gl.maximo = [0]*16 
	gl.minimo = [32000]*16
	
	if(gl.flag_debug):
		print("Obteniendo maximos y minimos..")
		
	while(abs(configuracion.radioRueda*pi*(configuracion.encoderD.steps- configuracion.encoderL.steps)*configuracion.N/(configuracion.CPR*configuracion.l))<4*pi):
		actuadores.motor(-vcal,vcal)
		if(gl.flag_debug):
			print(abs(configuracion.radioRueda*pi*(configuracion.encoderD.steps- configuracion.encoderL.steps)*configuracion.N/(configuracion.CPR*configuracion.l)))

		for s in range(16):
			
			if s<8:
				valor = read_adc(s, CS1_PIN)
			else:
				valor = read_adc(s - 8, CS2_PIN)
			gl.maximo[s] = max(valor, gl.maximo[s])
			gl.minimo[s] = min(valor, gl.minimo[s])
			time.sleep(0.01)
			print("leido: " + str(gl.maximo[s]) + '-------------' + str(gl.minimo[s]))

	if(gl.flag_debug):	
		print("listo, ahora voy a volver a la linea")

	while(((1-2*configuracion.linea)*100*(read_adc(4, CS1_PIN) - gl.minimo[2]) / (gl.maximo[2]-gl.minimo[2]) + 100*configuracion.linea ) < 80 ):
		#print((1-2*configuracion.linea)*100*(adc.read_adc(0, gain=configuracion.GAIN, data_rate=configuracion.sps) - minimo[2]) / (maximo[2]-minimo[2]) + 100*configuracion.linea )
		actuadores.motor(vcal,-vcal)

	actuadores.motor(0,0)



def configuracionSensorD():		#habilitar y configurar sensor de distancia
	tof.open()
	tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.GOOD)
	# timing = tof.get_timing()
	# if timing < 20000:
	# 	timing = 20000


def distancia():				#mide la distancia 
	dist = (tof.get_distance()/10) - configuracion.offsetSensorD #en cm, se le resta el offset
	if (dist > configuracion.sat_d):	#se satura en sat_d
		dist=configuracion.sat_d
	if(abs(dist - configuracion.d_ref)<= 3*gl.varianzaD):
		gl.distFiltro = gl.distFiltro*(1 - gl.alphaD) + dist*gl.alphaD
	#falta quitarle que entrege un valor muy distinto al leido anteriormente
	return gl.distFiltro



	
def velocidades():	#calcula velocidades, y la entrada del controlador PID de velocidad
	gl.t_actual = time.time() - gl.t_svel	#tiempo transcurrido desde ultima actualizacion de calculo de velocidad en s
	if(gl.t_actual >= 0.01):	#cada 10 ms
		v_r[1]=v_r[0]
		v_r[2]=v_r[1]
		v_r[3]=v_r[2]
		v_r[4]=v_r[3]
		v_l[1]=v_l[0]
		v_l[2]=v_l[1]
		v_l[3]=v_l[2]
		v_l[4]=v_l[3]
		v_r[0]=(2*pi*configuracion.radioRueda*configuracion.encoderD.steps*configuracion.N)/(gl.t_actual*configuracion.CPR); # ENCODERS:28CPR---CAJA_REDUCTORA:100:1  [cm/s]
		v_l[0]=(2*pi*configuracion.radioRueda*configuracion.encoderL.steps*configuracion.N)/(gl.t_actual*configuracion.CPR); # ENCODERS:28CPR---CAJA_REDUCTORA:100:1  [cm/s]
		configuracion.encoderD.steps = 0
		configuracion.encoderL.steps = 0
		gl.t_svel = time.time()
	#curva=2.3333*abs(((0.9*(v_r[1]+v_r[2]+v_r[3]+v_r[4])/4) + 0.1*v_r[0])-((0.9*(v_l[1]+v_l[2]+v_l[3]+v_l[4])/4) + 0.1*v_l[0]))
	v_r[0]=(0.2*(v_r[1]+v_r[2]+v_r[3]+v_r[4])/4) + 0.8*v_r[0]	#filtra velocidades que se escapen
	v_l[0]=(0.2*(v_l[1]+v_l[2]+v_l[3]+v_l[4])/4) + 0.8*v_l[0]
	gl.Input_vel=0.5*(v_r[0]+v_l[0]) # [cm/s]	#promedio de velocidades actuales R y L
	#ang_vel=0.5*(v_r[0]-v_l[0])/configuracion.l
	#gl.t_actual = time.time() - gl.t_arco
	#s_l+=abs(v_l[0]*configuracion.t_actual)
	#s_r+=abs(v_r[0]*configuracion.t_actual)
	#gl.t_arco= time.time()
	#s=0.5*(s_r+s_l)
	#if(s<10 & configuracion.Input_vel<0.1):
	#	#radio_curva=0
	#	s_l=0
	#	s_r=0
	#elif(s>=10):
		#radio_curva=abs((0.5*(s_r-s_l))/(configuracion.l*s))
	#	s_l=0
	#	s_r=0

def obtenerPosicion (direccion):	#obtienela longitud de arco que existe entre la linea y el centro de los sensores, respecto al eje de giro
	
	sensorNormalizado = [0]*16
	inte =  [0]*16
	sum1 = 0
	area = 0

	t_inicio = 0
	t_final = 0

	if (direccion == 1):	#direccion 0:hacia atras 1:hacia delante
		for s in range(8):	#mido los sensores IR de delante
			# t_inicio = time.time()
			sensorNormalizado[s] = ((1-2*configuracion.linea)*100*(read_adc(s, CS1_PIN)-gl.minimo[s])/(gl.maximo[s] -gl.minimo[s]))+100*configuracion.linea		#normaliza entre 0 a 100
			# t_final = time.time() - t_inicio
			# configuracion.count[0] = t_final
			# configuracion.count[1] = s
			# print(configuracion.count)
			if (sensorNormalizado[s]<30):
				sensorNormalizado[s]=0
	else:
		for s in range(8):	#mido los sensores IR de atras
			# valor_adc = adc.read_adc(0, gain=configuracion.GAIN, data_rate=configuracion.sps)
			# valor_adc = adc.read_adc(0, gain=configuracion.GAIN, data_rate=configuracion.sps)
			sensorNormalizado[s] = ((1-2*configuracion.linea)*100*(read_adc(s, CS2_PIN)-gl.minimo[s+8])/(gl.maximo[s+8] -gl.minimo[s+8]))+100*configuracion.linea
			if (sensorNormalizado[s]<30):
				sensorNormalizado[s]=0.

	# sens_adc = np.round(sensorNormalizado, 2)
	# print("-------------------------------------------------------------------------")		
	# print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} |'.format(*sens_adc))

	for s in range(8):
		inte[s]=8*sensorNormalizado[s]-0.04*sensorNormalizado[s]*sensorNormalizado[s]  	#cambia el rango de 200 a 400 linealizando el comportamiento del sensor 
	
	sum1=-28*inte[0] - 20*inte[1] - 12*inte[2] - 4*inte[3] + 4*inte[4] + 12*inte[5] + 20*inte[6] + 28*inte[7]	#pondera las posiciones del sensor
	area=inte[0]+inte[1]+inte[2]+inte[3]+inte[4]+inte[5]+inte[6]+inte[7]
	if(area==0):	#ya no esta sobre la linea
		gl.parar = "si"
		return 0
	else:
		gl.parar = gl.parar
		# print(sum1/area)
		return sum1/area #centroide, mientras mas cercano a 0 mas centrado en la linea

def curvaturaPista():
	global a_sl, a_sr, a_s, a_curvatura 
	global b_sl, b_sr, b_s, b_curvatura 
	global c_sl, c_sr, c_s, c_curvatura 
	gl.t_actual = time.time() - gl.t_arco
	if(gl.t_actual>=0.02):	#han transcurrido 20 ms
		a_sl += v_l[0]*gl.t_actual
		a_sr += v_r[0]*gl.t_actual
		b_sl += v_l[0]*gl.t_actual
		b_sr += v_r[0]*gl.t_actual
		c_sl += v_l[0]*gl.t_actual
		c_sr += v_r[0]*gl.t_actual
		gl.t_arco = time.time()
	a_s = (a_sr+a_sl)*0.5
	b_s = (b_sr+b_sl)*0.5
	c_s = (c_sr+c_sl)*0.5
	if(gl.Input_vel<0.1):
		a_curvatura = 0
		b_curvatura = 0
		c_curvatura = 0
		a_sl = 0
		a_sr = 0
		b_sl = 0
		b_sr = 0
		c_sl = 0
		c_sr = 0
	elif (a_s >= 3 and b_s>=10):
		b_curvatura = abs(((b_sr-b_sl)*0.5)/(configuracion.l*b_s))
		b_sl = 0
		b_sr = 0
	elif (a_s>=3 and a_s == b_s):
		b_sl=0
		b_sr=0
	elif (a_s>=6 and c_s>=10):
		c_curvatura = abs(((c_sr-c_sl)*0.5)/(configuracion.l*c_s))
		c_sl = 0
		c_sr = 0
	elif (a_s>=6 and a_s == c_s):
		c_sl=0
		c_sr=0
	elif (a_s>=10):
		a_curvatura = abs(((a_sr-a_sl)*0.5)/(configuracion.l*a_s))
		a_sl = 0
		a_sr = 0
	if(a_curvatura<0.01 and b_curvatura<0.01 and c_curvatura<0.01):
		gl.recta=1
	elif(a_curvatura>0.02 and b_curvatura>0.02 and c_curvatura>0.02):
		gl.recta=0
	if (gl.recta==1):
		if(a_curvatura>= b_curvatura and a_curvatura>= c_curvatura):
			gl.curvatura= a_curvatura
		elif(b_curvatura>= a_curvatura and b_curvatura>= c_curvatura):
			gl.curvatura= b_curvatura
		elif(c_curvatura>= a_curvatura and c_curvatura>= b_curvatura):
			gl.curvatura= c_curvatura
		else:
			gl.curvatura= a_curvatura
	else:
		if(a_curvatura< b_curvatura and a_curvatura< c_curvatura):
			gl.curvatura= a_curvatura
		elif(b_curvatura< a_curvatura and b_curvatura< c_curvatura):
			gl.curvatura= b_curvatura
		elif(c_curvatura< a_curvatura and c_curvatura< b_curvatura):
			gl.curvatura= c_curvatura
		else:
			gl.curvatura= a_curvatura


