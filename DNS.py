from socket import *
#IP e Porta do DNS
UDP_IP = "127.0.0.1"
UDP_PORT = 12019

sock = socket(AF_INET, SOCK_STREAM) #criando o socket
sock.bind((UDP_IP,UDP_PORT))
sock.listen(1)
domains = dict()	#criando o dicionario, para armazenar os dominios

#padrão da mensagem com o servidor DNS
#[OP] [DOMAIN]
# - SET para definir o endereço de um dominio
# - GET para invocar o endereço de um dominio
# - END para encerrar o servidor

print("DNS is ON")
while True:
	connectionSocket, addr = sock.accept()
	args = connectionSocket.recv(1024).decode().split()
	print("received Option: ",args[0])	
	if(args[0] == "SET"):
		domains[args[1]] = addr
		connectionSocket.send((domains[args[1]][0]+" "+str(domains[args[1]][1])).encode())
	elif(args[0] == "GET"):
		connectionSocket.send((domains[args[1]][0]+" "+str(domains[args[1]][1])).encode())
	elif(args[0] == "END"):
		break;
	connectionSocket.close()
print("Farewell")
connectionSocket.close()
sock.close()

