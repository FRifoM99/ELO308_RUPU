import socket
import os

gw = os.popen("ip -4 route show default").read().split()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((gw[2], 0))
IPAddr = s.getsockname()[0]

UDP_IP = IPAddr
UDP_PORT = 1111
print(IPAddr)
sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message: %s" % data)
    message = str(data.decode('utf-8'))
    message = message.split('/')
    print("received message: %s" % message[1])