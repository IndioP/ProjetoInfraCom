from socket import *
UDP_IP = "127.0.0.1"
UDP_PORT = 12015

message = "SET ad"

sock = socket(AF_INET, SOCK_STREAM)
sock.connect((UDP_IP,UDP_PORT))
sock.send(message.encode())
sock.close()
