# coding=utf-8
import actuadores
import configuracion
import sensores
import conexion
import main
import time
import gl
import logging	#para crear el archivo que almacena los datos 
import threading    #hilos
import ctypes

# Cargar la biblioteca compartida
pid_lib = ctypes.CDLL("./libpid_control.so")  # Usa ".dll" en Windows

# Configurar los tipos de argumentos y retorno para calculoPID
pid_lib.calculoPID.argtypes = [ctypes.c_double, ctypes.c_double,
                               ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double),
                               ctypes.c_double, ctypes.c_double, ctypes.c_double,
                               ctypes.c_double, ctypes.c_char_p, ctypes.c_double,
                               ctypes.c_char_p, ctypes.c_double, ctypes.c_int]
pid_lib.calculoPID.restype = ctypes.c_double

# Configurar los tipos de argumentos y retorno para calculoPIDd
pid_lib.calculoPIDd.argtypes = [ctypes.c_double, ctypes.c_double,
                                ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double),
                                ctypes.c_double, ctypes.c_double, ctypes.c_double,
                                ctypes.c_double, ctypes.c_char_p, ctypes.c_double,
                                ctypes.c_char_p, ctypes.c_double, ctypes.c_int]
pid_lib.calculoPIDd.restype = ctypes.c_double

t_inicio = 0
t_final = 0
flag_sensado = 0
pi = configuracion.pi

def ciclo_de_inicio():
	# print('inicio')
	if (gl.flag_udp):
		conexion.udp_recep() 
	gl.PID_theta = b"MANUAL"
	gl.PID_vel = b"MANUAL"
	gl.PID_d = b"MANUAL"
	gl.error_ant_d=(ctypes.c_double * 1)(0.0)  # Inicializado a 0.0 como puntero 
	gl.integral_d=(ctypes.c_double * 1)(0.0) 
	gl.error_ant_vel=(ctypes.c_double * 1)(0.0)
	gl.integral_vel=(ctypes.c_double * 1)(0.0)
	gl.error_ant_theta=(ctypes.c_double * 1)(0.0)
	gl.integral_theta=(ctypes.c_double * 1)(0.0)
	gl.Output_d=0.0
	gl.Output_vel=0.0
	gl.Output_theta=0.0
	#configuracion.d_ref = sensores.distancia()
	#gl.sp_vel = 0.0
	gl.Input_vel=0.0
	#configuracion.vel_ref=0.0
	actuadores.motor(0,0)
	configuracion.posR = 0
	configuracion.PosL = 0
	sensores.obtenerPosicion(1)
	gl.t_controlador=time.time()
	if (gl.flag_udp):
		conexion.udp_transm()
		if(gl.flag_debug_udp):
			print("se intenta mandar informacion udp")

def ciclo_de_calibracion():
	if(gl.flag_calibrar):
		sensores.calibrarSensores ()
	gl.calibrar = 0
	gl.parar = "si"
	
def ciclo_de_control():
	
  
	global flag_sensado
	if (flag_sensado == 0):
		print(*configuracion.count, sep=", ")
		# print(gl.Input_theta)
		t_inicio = 0
		t_final = 0
		
		if (gl.flag_udp):
			conexion.udp_recep()

		t_inicio = time.time()
# MEDICION DISTANCIA
		gl.Input_d = sensores.distancia()
		flag_sensado = 1
		# print('distancia == ' + str(gl.Input_d))

		t_final = time.time() - t_inicio
		configuracion.count[0] = t_final


		if (gl.flag_robot != "L"):
			gl.error_d = gl.Input_d - configuracion.d_ref
		else:
			gl.error_d = 0

# MEDICION VELOCIDAD
		t_inicio = time.time()
		sensores.velocidades()	
		t_final = time.time() - t_inicio
		configuracion.count[1] = t_final


		# t_inicio = time.time()
		# sensores.curvaturaPista()
		# t_final = time.time() - t_inicio	
		# configuracion.count[2] = t_final
		# gl.control = ((gl.curvatura_predecesor <= 0.01) and (gl.curvatura <= 0.01))
			
		# if (gl.flag_sensado):
		gl.control = 1
			
# MEDICION POSICION
		t_inicio = time.time()
		if (gl.Output_vel<0):		#calcula entrada de PID angulo linea			
			gl.Input_theta=-1*sensores.obtenerPosicion(0)/configuracion.d2		#recorrido inverso
		else:
			gl.Input_theta= sensores.obtenerPosicion(1)/configuracion.d1		#recorrido hacia delante
		t_final = time.time() - t_inicio
		configuracion.count[3] = t_final
	

		gl.PID_vel=b"AUTO"
		gl.PID_theta=b"AUTO"
		gl.PID_d=b"AUTO"
				
		if((abs(gl.error_d) >= gl.delta + 1) or (gl.flag_robot == "L")):
			gl.PID_theta=b"AUTO"
			gl.PID_vel=b"AUTO"
			if (gl.control):
				gl.PID_d=b"AUTO"
			else:
				gl.PID_d=b"MANUAL"
				gl.Output_vel = gl.vel_crucero
				gl.error_ant_d = (ctypes.c_double * 1)(0.0) 
				gl.integral_d = [gl.vel_crucero / gl.Ki_d - gl.error_d * 0.04]
			if (gl.flag_robot == "L"):
				gl.PID_d = b"MANUAL"
				gl.Output_d = 0
				gl.error_ant_d = (ctypes.c_double * 1)(0.0) 
				gl.integral_d = (ctypes.c_double * 1)(0.0) 
				gl.error_d = 0

		if ((abs(gl.Input_vel) <= 6) and (abs(gl.Input_theta) <= 0.015) and (abs(gl.error_d)<gl.delta) and ((gl.sp_vel == 0) or gl.flag_robot != "L")):
			gl.PID_d=b"MANUAL"
			gl.PID_vel=b"MANUAL"
			gl.PID_theta=b"MANUAL"
			gl.Output_d = 0
			gl.Output_vel = 0
			gl.Output_theta = 0
			gl.error_ant_d=(ctypes.c_double * 1)(0.0) 
			gl.integral_d=(ctypes.c_double * 1)(0.0) 
			gl.error_ant_vel=(ctypes.c_double * 1)(0.0)
			gl.integral_vel=(ctypes.c_double * 1)(0.0)
			gl.error_ant_theta=(ctypes.c_double * 1)(0.0)
			gl.integral_theta=(ctypes.c_double * 1)(0.0)
			
		if (gl.flag_udp):
			conexion.udp_transm()


	# if time.time() - gl.t_controlador < 0.04:
	# 	while time.time() - gl.t_controlador < 0.04:
	# 		time.sleep(0.0002)  #

	else:
		gl.t_actual = time.time() - gl.t_controlador
		time.sleep(0.00001)
		

		if (gl.t_actual >= 0.04):							#se activa cada 40 ms
			# print('tiempo final ==' + str(gl.t_actual))
			# gl.t_control = time.time()
			t_inicio = time.time()
			pi.write(26, 1)
			# print('control' + '-----------' + str(gl.t_actual))
			# gl.error_ant_d = (ctypes.c_double * 1)(gl.error_ant_d)
			# gl.integral_d = (ctypes.c_double * 1)(gl.integral_d)
			if(gl.flag_saturacion_predecesor):
				gl.Output_d=pid_lib.calculoPIDd(gl.Input_d, configuracion.d_ref, gl.error_ant_d, gl.integral_d, gl.Kp_d, gl.Ki_d, gl.Kd_d, configuracion.sat_d, gl.PID_d, gl.Output_d, b"INVERSO", gl.t_actual, gl.flag_debug)
			else:
				gl.Output_d=pid_lib.calculoPID(gl.Input_d, configuracion.d_ref, gl.error_ant_d, gl.integral_d, gl.Kp_d, gl.Ki_d, gl.Kd_d, configuracion.sat_d, gl.PID_d, gl.Output_d, b"INVERSO", gl.t_actual, gl.flag_debug)
			if (gl.flag_robot == "L"):
				configuracion.vel_ref=gl.sp_vel
			else:
				configuracion.vel_ref=gl.Output_d
			gl.Output_vel=pid_lib.calculoPID(gl.Input_vel, configuracion.vel_ref, gl.error_ant_vel, gl.integral_vel, gl.Kp_vel, gl.Ki_vel, gl.Kd_vel, configuracion.sat_vel, gl.PID_vel, gl.Output_vel, b"DIRECTO", gl.t_actual, gl.flag_debug)
			gl.Output_theta=pid_lib.calculoPID(gl.Input_theta, configuracion.theta_ref, gl.error_ant_theta, gl.integral_theta, gl.Kp_theta, gl.Ki_theta, gl.Kd_theta, configuracion.sat_theta, gl.PID_theta, gl.Output_theta, b"DIRECTO", gl.t_actual, gl.flag_debug)

			if(gl.flag_udp):
				conexion.udp_monitor()
			# gl.t_control_f = time.time() - gl.t_control
			t_final = time.time() - t_inicio
			configuracion.count[4] = t_final
			flag_sensado = 0
			pi.write(26, 0)
			gl.t_controlador=time.time()
			configuracion.count[2] = gl.t_actual

	actuadores.motor(gl.Output_vel - gl.Output_theta , gl.Output_vel + gl.Output_theta)
	

# def calculoPID (y, ref, error_ant, error_integral, kp, ki, kd, limite, MODO, out_manual, direccion):
	# if (MODO == "MANUAL"):
	# 	return out_manual
	
	# elif (MODO == "AUTO"):
	# 	if(direccion=="DIRECTO"):
	# 		error=ref-y
	# 	elif(direccion =="INVERSO"):
	# 		error=y-ref
	# 	error_integral[0] = error_integral[0] + error*gl.t_actual
	# 	if(error_integral[0] * ki > limite):
	# 		error_integral[0] = limite /ki
	# 	elif(ki*error_integral[0] < -limite):
	# 		error_integral[0] = -limite /ki
	# 	u=kp*error + error_integral[0]*ki + kd*(error-error_ant[0] )/(gl.t_actual)
	# 	if (gl.flag_debug):
	# 		print("u: " + str(u))
	# 	error_ant[0] = error

	# 	if(u>limite):
	# 		return limite
	# 	elif (u<-limite):
	# 		return -limite
	# 	else:
	# 		return u

# def calculoPIDd (y, ref, error_ant, error_integral, kp, ki, kd, limite, MODO, out_manual, direccion):
# 	# print("hola, estoy en modo: " + str(MODO) + " y mi control es " + str(gl.control))
# 	if (MODO == "MANUAL"):
# 		return out_manual
	
# 	elif (MODO == "AUTO"):
# 		if(direccion=="DIRECTO"):
# 			error=ref-y
# 		elif(direccion =="INVERSO"):
# 			error=y-ref
# 		error_integral[0] = error_integral[0] + error*gl.t_actual
# 		print("error integral antes de saturar: " + str(error_integral[0]))
# 		if(error_integral[0] * ki > limite):
# 			error_integral[0] = limite /ki
# 		elif(ki*error_integral[0] < -limite):
# 			error_integral[0] = -limite /ki
# 		u=kp*error + error_integral[0]*ki + kd*(error-error_ant[0] )/(gl.t_actual)
# 		if (gl.flag_debug):
# 			print("u: " + str(u))
# 		error_ant[0] = error

# 		if(u > (limite * 1.1 + 1)):
# 			return limite * 1.1 + 1
# 		elif (u < (limite * 0.9 - 1)):
# 			return limite * 0.9 - 1
# 		else:
# 			return u
