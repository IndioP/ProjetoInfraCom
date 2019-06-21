from socket import *
import subprocess
import utils
from random import *

UDP_IP = "127.0.0.1"
UDP_PORT = 12019

#Pode ser implementado depois
SERVER_NAME = "www.infracom.com"

#pode ser colocado depois para ser gerado randomicamente
UDP_PORT_SERVER = 54219

#setando meu dominio no DNS
sock = socket()

#socket como UDP
sock = socket(AF_INET, SOCK_DGRAM)

sock.connect((UDP_IP, UDP_PORT))

messageToDNS = "SET " + str(UDP_PORT_SERVER) + " " + SERVER_NAME

#Seta o domínio no DNS com a porta previamente selecionada
print("Message: ", messageToDNS)

sock.send(messageToDNS.encode())

utils.getACK(sock, messageToDNS, UDP_IP, UDP_PORT)

#Fecha o socket de comunicação com o DNS
sock.close()
print("Socket closed")


#criando o socket de comunicação cliente servidor
sockd = socket(AF_INET, SOCK_DGRAM) 

sockd.bind(('', UDP_PORT_SERVER))

print("Server is on")

while True:
	#connectionSocket, addr = sockd.accept()
	
	messageFromClient, addr = sockd.recvfrom(1024)

	args = messageFromClient.decode().split()

	print("received Option: ",args[0])	
	
	if(args[0] == "END"):
		sockd.sendto("ACK".encode(), addr)
		break

	elif(args[0] == "LST"):
		sockd.sendto("ACK".encode(), addr)
		returned_value = subprocess.check_output("ls")
		sockd.sendto(returned_value,addr)
		print('returned_value:',returned_value.decode())

	elif(args[0] == "GET"):
		sockd.sendto("ACK".encode(), addr)
		file_handle = open(args[1],"rb")
		last = file_handle.read(1000)
		segNumber = randint(0,1000)
		while True:
			new = file_handle.read(1000)
			if not new: 															#if EOF
				sockd.sendto(("0 " + str(segNumber)+" ").encode() + last,addr)
				break
			sockd.sendto(("1 "+ str(segNumber)+" ").encode() + last,addr)
			segNumber+=1000
			last = new
		
		file_handle.close()

print("Farewell")
sockd.close()
