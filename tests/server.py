from socket import *
#trocado por pathlib
import pathlib
import utils
from random import *

UDP_IP = "127.0.0.1"
UDP_PORT = 54210

#criando o socket de comunicação cliente servidor
sockd = socket(AF_INET, SOCK_DGRAM) 

sockd.bind(('', UDP_PORT))

print("Server is on")

while True:
	#connectionSocket, addr = sockd.accept()	
	messageFromClient, addr = sockd.recvfrom(1024)

	args = messageFromClient.decode().split()

	print("received Option: ",args[0])	

	if(args[0] == "GET"):
		msg = "Hello"
		utils.sendFile(sockd, msg, addr)

print("Farewell")
sockd.close()
