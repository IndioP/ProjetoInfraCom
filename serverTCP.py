from socket import *
import subprocess

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

message = "SET " + str(UDP_PORT_SERVER) + " " + SERVER_NAME

#Seta o domínio no DNS com a porta previamente selecionada
print("Message: ", message)

sock.send(message.encode())

#Fecha o socket de comunicação com o DNS
sock.close()
print("Socket closed")


#criando o socket de comunicação cliente servidor
sockd = socket(AF_INET, SOCK_STREAM) 

sockd.bind((UDP_IP, UDP_PORT_SERVER))

sockd.listen(1)

print("Server is on")

while True:
	connectionSocket, addr = sockd.accept()
	args = connectionSocket.recv(1024).decode().split()
	print("received Option: ",args[0])	
	if(args[0] == "END"):
		break
	if(args[0] == "LST"):
		returned_value = subprocess.check_output(cmd)
		connectionSocket.send(returned_value)
		#print('returned_value:',returned_value)
	connectionSocket.close()
print("Farewell")
connectionSocket.close()
sockd.close()




