# coding=utf-8
import threading
# import paho.mqtt.client as mqttClient
import socket
import json
import time
import gl
import configuracion
import os


# """
#     Implementacion de MQTT (Ubidots)
# """
# #configuracion para ubidots
# global mqtt_client
# connected = False
# BROKER_ENDPOINT = "industrial.api.ubidots.com"
# PORT = 1883
# TOPIC  = "/v1.6/devices/"
# MQTT_USERNAME = 'BBFF-yMNR3Otjl6H8tka4RmaEcCSZeXwt0J'
# MQTT_PASSWORD = ''
# DEVICE_LABEL = "raspberry/"
# VARIABLE_LABEL = "prueba"
# TOPIC_SUSCRITO = "/v1.6/devices/controlador/+/lv"


# # The callback for when a message is received from the server.
# def on_message(client, userdata, msg):
#     if(gl.flag_debug):
#         print("sisub: msg received with topic: {} and payload: {}".format(msg.topic, str(msg.payload)))
#     variable = msg.topic.split('/')[4]  
#     valor = msg.payload.decode("utf-8") 
#     if (variable == "distancia_kp"): gl.Kp_d = float(valor)
#     elif (variable == "distancia_ki"): gl.Ki_d = float(valor)
#     elif (variable == "distancia_kd"): gl.Kd_d = float(valor)

#     elif (variable == "theta_kp"): gl.Kp_theta = float(valor)
#     elif (variable == "theta_ki"): gl.Ki_theta = float(valor)
#     elif (variable == "theta_kd"): gl.Kd_theta = float(valor)

#     elif (variable == "velocidad_kp"): gl.Kp_vel = float(valor)
#     elif (variable == "velocidad_ki"): gl.Ki_vel = float(valor)
#     elif (variable == "velocidad_kd"): gl.Kd_vel = float(valor)

#     elif (variable == "sp_vel"): gl.sp_vel = float(valor)
#     elif (variable == "vel_crucero"): gl.vel_crucero = float(valor)
#     elif (variable == "delta"): gl.delta = float(valor)
#     elif (variable == "d_ref"): configuracion.d_ref = float(valor)
#     elif (variable == "calibrar"): gl.calibrar = float(valor)
#     elif (variable == "parar"): gl.parar = str(valor)



    
# def connect(mqtt_client, mqtt_username, mqtt_password, broker_endpoint, port):
#     global connected

#     if not connected:
#         mqtt_client.username_pw_set(mqtt_username, password=mqtt_password)
#         mqtt_client.on_connect = on_connect
#         mqtt_client.on_publish = on_publish
#         mqtt_client.on_message = on_message
#         mqtt_client.connect(broker_endpoint, port=port)
#         mqtt_client.loop_forever()

#         attempts = 0

#         while not connected and attempts < 5:  # Wait for connection
#             if(gl.flag_debug):
#                 print(connected)
#                 print("Attempting to connect...")
#             time.sleep(1)
#             attempts += 1

#     if not connected:
#         if(gl.flag_debug):
#             print("[ERROR] Could not connect to broker")
#         return False

#     return True



"""
    Implementacion de UDP
"""

gw = os.popen("ip -4 route show default").read().split()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((gw[2], 0))
IPAddr = s.getsockname()[0]

print(IPAddr)
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
            # elif(message[1] == 'sp_vel'):
            #     gl.sp_vel = int(message[2])
            # if(message[1] == 'cv_ref'):
            # if(message[1] == 'cv_ref'):



         

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







