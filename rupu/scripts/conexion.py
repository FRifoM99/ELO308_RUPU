# coding=utf-8
import threading
import socket
import json
import time
import gl
import configuracion
import os

"""
    Implementacion de UDP
"""


import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15].encode('utf-8'))
    )[20:24])

try:
    IPAddr = get_ip_address('wlan0')
    print("Dirección IP en modo hotspot:", IPAddr)
except OSError:
    print("No se pudo obtener la dirección IP. Asegúrate de que la interfaz esté activa.")

# gw = os.popen("ip -4 route show default").read().split()
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect((gw[2], 0))
# IPAddr = s.getsockname()[0]

# print(IPAddr)


UDP_IP = IPAddr
UDP_PORT = 1111

socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
data = bytearray()

def udp_transm():   #Transmite informacion al robot sucesor
    global socket_udp
    gl.t_actual = time.time() - gl.t_com_predecesor
    if (gl.t_actual >= 0.1):    #0.1 segundo
        cadena = "V/" + gl.parar + "/" + str(gl.Input_vel) + "/" + str(configuracion.vel_ref) + "/" + str(gl.curvatura)
        msg = str.encode(cadena)
        if(gl.flag_robot == "L"): sucesor = configuracion.seguidor1
        elif (gl.flag_robot == "S1"): sucesor = configuracion.seguidor2
        elif (gl.flag_robot == "S2"): sucesor = configuracion.seguidor3
        else: sucesor = configuracion.seguidor1
        if(gl.flag_debug_udp):
            print("voy a enviar al sucesor" + str(sucesor) + " la cadena : " + cadena)
        socket_udp.sendto(msg, sucesor)
        gl.t_com_predecesor = time.time()

def setup_udp():
    global socket_udp, data, message
    if(gl.flag_robot == "L"): local = configuracion.lider
    elif (gl.flag_robot == "S1"): local = configuracion.seguidor1
    elif (gl.flag_robot == "S2"): local = configuracion.seguidor2
    elif (gl.flag_robot == "S3"): local = configuracion.seguidor3
    else: local = configuracion.lider

    if(gl.flag_debug_udp):
        print('abriendo servidor udp en {} port {}'.format(*local))
    socket_udp.bind((UDP_IP, UDP_PORT))

    while True:
        if(gl.flag_debug_udp):
            print('\nesperando a recibir mensajes')
        data, address = socket_udp.recvfrom(4096)

        if(gl.flag_debug_udp):
            print('received {} bytes from {}'.format(len(data), address))
            print(data)
        message = str(data.decode('utf-8'))
        message = message.split('/')

        if(message[0] == 'E'):
            if(message[1] == 'cv_ref'):
                gl.sp_vel = int(message[2])
            elif(message[1] == 'parar'):
                print('parar')
                gl.parar = message[2]
            elif(message[1] == 'calibrar'):
                gl.calibrar = message[2]
            elif(message[1] == 'co_p'):
                gl.Kp_theta = int(message[2])
            elif(message[1] == 'co_i'):
                gl.Ki_theta = int(message[2])
            elif(message[1] == 'co_d'):
                gl.Kd_theta = int(message[2])
            elif(message[1] == 'cv_p'):
                gl.Kp_vel = int(message[2])
            elif(message[1] == 'cv_i'):
                gl.Kp_vel = int(message[2])
            elif(message[1] == 'cv_d'):
                gl.Kp_vel = int(message[2])
            elif(message[1] == 'cd_p'):
                gl.Kp_d = int(message[2])
            elif(message[1] == 'cd_i'):
                gl.Kp_d = int(message[2])
            elif(message[1] == 'cd_d'):
                gl.Kp_d = int(message[2])



def udp_monitor():
    # print(gl.t_actual)
    cadena = gl.flag_robot + "," +  str(gl.t_actual)  + "," +  str(gl.Input_d)  + "," +  str(configuracion.d_ref)  + "," +  str(configuracion.vel_ref)  + "," +  str(gl.Input_vel)  + "," +  str(gl.Input_theta)  + "," +  str(gl.Output_d)  + "," +   str(gl.Output_vel)  + "," +  str(gl.Output_theta)  + "," +  str(gl.curvatura) + "," +  str(gl.vel_crucero)  + "," +  str(gl.curvatura_predecesor)  + "," +  str(gl.control)    
    cadena2 = gl.flag_robot + "," + str(gl.Input_vel)  + "," +  str(configuracion.vel_ref) + "," + str(gl.error_ant_vel[0]) + "," +  str(gl.Output_vel)  + "," + str(gl.Kp_vel) + "," + str(gl.Ki_vel) + "," + str(gl.Kd_vel)  + "," + str(gl.Input_theta)  + "," +  str(configuracion.theta_ref) + "," + str(gl.error_ant_theta[0]) + "," +  str(gl.Output_theta) + "," + str(gl.Kp_theta) + "," + str(gl.Ki_theta) + "," + str(gl.Kd_theta) + "," + str(gl.Input_d)  + "," +  str(configuracion.d_ref) + "," + str(gl.error_ant_d[0]) + "," +  str(gl.Output_d)  + "," + str(gl.Kp_d) + "," + str(gl.Ki_d) + "," + str(gl.Kd_d)
#    msg = str.encode(cadena2)
    msg = str.encode(cadena)
    if(gl.flag_debug_udp):
        print("voy a enviar al monitor la cadena : " + cadena)
    socket_udp.sendto(msg, configuracion.monitor)
 
def udp_recep():
    global data
    paquete_entrante = data.decode('UTF-8')
    len_data = len(data)
    if (len_data > 0):
        if(paquete_entrante[0] == "L"):
            lectura_estado(len_data)
        elif (paquete_entrante[0] == "V"):
            estado_predecesor(len_data)



def lectura_estado(len_data):   
    global data, socket_udp
    mensaje = data.decode('UTF-8')
    if(gl.flag_debug_udp):
        print("funcion enviar informacion a sucesor")
    if (mensaje == "L/estado_predecesor"):
        cadena = "V/" + gl.parar + "/" + str(gl.Input_vel) + "/" + str(configuracion.vel_ref) + "/" + str(gl.curvatura_predecesor)
    else:
        cadena = "incorrecto"
    for i in range (3):
        msg = str.encode(cadena)
        
        if(gl.flag_robot == "L"): sucesor = configuracion.seguidor1
        elif(gl.flag_robot == "S1"): sucesor = configuracion.seguidor2
        elif(gl.flag_robot == "S2"): sucesor = configuracion.seguidor3
        elif(gl.flag_robot == "S3"): sucesor = configuracion.seguidor4
        
        if(gl.flag_debug_udp):
            print("voy a enviar al sucesor " + str.i + " veces la cadena: " + cadena)
        
        socket_udp.sendto(msg, configuracion.monitor)

def estado_predecesor(len_data): 
    global data
    mensaje = data.decode('UTF-8')
    if(gl.flag_debug_udp):
        print("funcion obtener estado predecesor con mensaje: " + mensaje)
    valores = mensaje.split("/")
    if (len(valores) < 4):
        if(gl.flag_debug_udp):
            print("datos insuficientes")
    else:
        # gl.parar = valores[1]

        if(gl.flag_control):
            gl.vel_crucero = float(valores[2])

        if(gl.flag_saturacion_predecesor):
            configuracion.sat_d = float(valores[3])

            if (float(valores[3]) >= 0):
                configuracion.sat_d = 1 * float(valores[3]) + 1
            else:
                configuracion.sat_d = -1 * float(valores[3]) + 1

        if(gl.flag_control):
            gl.vel_crucero = float(valores[2])
        
        gl.curvatura_predecesor = float(valores[4])







