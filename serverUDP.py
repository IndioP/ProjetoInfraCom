from socket import *
import subprocess
import utils

UDP_IP = "127.0.0.1"
UDP_PORT = 12019

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


# while True:
# 	messageFromDNS, address = sock.recvfrom(1024)	
# 	if(messageFromDNS.decode() == "ACK"):
# 		print("ACK Received")
# 		break
# 	else:
# 		sock.send(messageToDNS.encode())


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

	sockd.sendto("ACK".encode(), addr)

	args = messageFromClient.decode().split()

	print("received Option: ",args[0])	
	
	if(args[0] == "END"):
		break

	if(args[0] == "LST"):
		print("Hello")
		#returned_value = subprocess.check_output(cmd)
		#connectionSocket.send(returned_value)
		#print('returned_value:',returned_value)

	connectionSocket.close()
print("Farewell")
connectionSocket.close()
sockd.close()




