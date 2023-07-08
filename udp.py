import socket

UDP_PORT = 2390
UDP_IP = "192.168.43.255"

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 

sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message: %s" % data)