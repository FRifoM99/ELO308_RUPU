# coding=utf-8
import configuracion
import ctypes

#   variables globales  #

#FALTA IMPLEMENTAR#
global control
control = 0.0

#flags para debug
flag_debug = False   #activa los print
flag_debug_udp = False
flag_logger = False     #activa que escriba el archivo logger
flag_ubidots = False    #activa la suscripcion y publicacion en ubidots
flag_udp = True        #activa comunicacion upd
flag_calibrar = True   #activa la rutina de calibracion de los sensores IR
flag_peloton = True     #activa la funcionalidad multiagente
flag_robot = "L"        #Lider por defecto
flag_control = False   # activa switche curvatura
flag_saturacion_predecesor = True  ##activa saturador para PID distancia

#para comunicacion UDP
global data
data = bytearray()

#define los estados de las variables de transicion para el motor de estados
global parar, calibrar  
parar="si"
calibrar=0

#almacena valores maximos y minimos para calibracion de sensores IR
global maximo, minimo
maximo = [0]*16    
minimo = [32000]*16

#almacena timers
global t_actual     #tiempo transcurrido desde la ultima actualizacion de velocidades
global t_svel       #ultima actualizacion de velocidades
global t_controlador    #ultima actualizacion de controlador
global t_arco       #ultima actualizacion de control por curvatura
global t_com_predecesor #ultima actualizacion comunicacion predecesor
global t_control
global t_control_f
t_control_f = 0
t_actual = 0.0
t_svel = 0.0
t_controlador = 0.0
t_arco = 0.0
t_com_predecesor = 0.0

#Variables controlador PID para la posicion sobre la linea
global Input_theta, Output_theta, Kp_theta, Ki_theta, Kd_theta
Input_theta = 0     #entrada PID angulo, se busca que sea 0
Output_theta= 0     #salida PID angulo
Kp_theta = 1300 # 2000
Ki_theta = 700 # 4500
Kd_theta = 15 # 60

#Variables controlador PID para la velocidad
global Input_vel, Output_vel, sp_vel, vel_crucero, Kp_vel,Ki_vel, Kd_vel
Input_vel = 0.0       #promedio de velocidades actuales R y L
Output_vel= 0.0
vel_crucero = 15.0
sp_vel = 0.0
Kp_vel = 20.3 #5.75351825345478 #20.3 #100;//49.9757241214599;//130;
Ki_vel = 145.3 #0.100712270288173 #145.3 #282.271150682254;//130;
Kd_vel = 0 #0 #0.197722771627088;//0;

global PID_theta, error_ant_theta, integral_theta, PID_vel, error_ant_vel, integral_vel, PID_d, error_ant_d, integral_d
PID_theta="MANUAL"
error_ant_theta=(ctypes.c_double * 1)(0.0)
integral_theta=(ctypes.c_double * 1)(0.0)
PID_vel = "MANUAL"
error_ant_vel=(ctypes.c_double * 1)(0.0)
integral_vel=(ctypes.c_double * 1)(0.0)
PID_d="MANUAL"
error_ant_d = (ctypes.c_double * 1)(0.0)  # Inicializado a 0.0 como puntero
integral_d = (ctypes.c_double * 1)(0.0) 

#Variables controlador PID para la distancia
global Input_d, Output_d, error_d, alpha_fuzzy, delta, Kp_d, Ki_d, Kd_d, distFiltro
Input_d = 0         #entrada del PID de distancia, es la distancia que existe hacia delante
Output_d = 0
error_d = 0
#alpha_fuzzy=1
delta = 0.1
Kp_d = 4 #100 #1.5;//8.0013
Ki_d = 3 #11;//5.6025
Kd_d = 0 #0.1;//1.0077
distFiltro = configuracion.d_ref
alphaD = 1.0
varianzaD = 10

#variables para detectar curva
global recta, curvatura, curvatura_predecesor
recta = 0.0
curvatura = 0.0
curvatura_predecesor = 0.0

global velocidad_calibracion
velocidad_calibracion = 200

