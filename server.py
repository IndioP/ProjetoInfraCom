from socket import *
UDP_IP = "127.0.0.1"
UDP_PORT = 12016

message = "ad" #my domain


#setando meu dominio no DNS
sock = socket(AF_INET, SOCK_STREAM)
sock.connect((UDP_IP,UDP_PORT))
message2 = "SET " + message
sock.send(message2.encode())
answer = sock.recv(1024).decode().split()
sock.close()


sockd = socket(AF_INET, SOCK_STREAM) #criando o socket de comunicação cliente servidor
sockd.bind((answer[0], int(answer[1])))
sockd.listen(1)
print("Server is on")
while True:
	connectionSocket, addr = sockd.accept()
	args = connectionSocket.recv(1024).decode().split()
	print("received Option: ",args[0])	
	if(args[0] == "END"):
		break;
	connectionSocket.close()
print("Farewell")
connectionSocket.close()
sockd.close()



