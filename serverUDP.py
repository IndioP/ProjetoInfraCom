from socket import *
import subprocess
import utils

UDP_IP = "127.0.0.1"
UDP_PORT = 12018

#Pode ser implementado depois
SERVER_NAME = "www.infracom.com"

#pode ser colocado depois para ser gerado randomicamente
UDP_PORT_SERVER = 54210

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

	if(args[0] == "LST"):
		sockd.sendto("ACK".encode(), addr)
		returned_value = subprocess.check_output("ls")
		sockd.sendto(returned_value,addr)
		print('returned_value:',returned_value.decode())

	#connectionSocket.close()
print("Farewell")
#connectionSocket.close()
sockd.close()




