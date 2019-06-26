from socket import *
#trocado por pathlib
import pathlib
import utils
from random import *
import threading

UDP_IP = "127.0.0.1"
UDP_PORT = 12020

#Pode ser implementado depois
SERVER_NAME = "www.infracom.com"

#pode ser colocado depois para ser gerado randomicamente
UDP_PORT_SERVER = 54233

def worker(addr, message):
	print("chegou aqui")

	sockd = socket(AF_INET, SOCK_DGRAM)
	#connectionSocket, addr = sockd.accept()

	args = message.decode().split()

	print("received Option: ",args[0])	

	if(args[0] == "LST"):

		print("Thread " + str(id) + " recebeu a requisicao")
		
		sockd.sendto("ACK".encode(), addr)
		
		files = ""

		path = pathlib.Path('tests')

		#Verificamos cada arquivo dentro da pasta especificada
		for currentFile in path.iterdir():  
			files = files + str(currentFile) + "\n"
			#print(files)

		#utils.sendPKT(socket, files, addr)
		sockd.sendto(files.encode(),addr)

		#sockd.sendto(files.encode(),addr)
		print('Lista:',files)

	elif(args[0] == "GET"):
		
		sockd.sendto("ACK".encode(), addr)
		msg = "tests/"+ args[1]
		utils.sendFile(sockd, msg, addr)
		print("Returned to main")
		#sockd.setblocking(True)
		
	print("Thread returning to main")


def main():
	#setando meu dominio no DNS
	sock = socket()

	#socket como UDP
	sock = socket(AF_INET, SOCK_DGRAM)

	sock.connect((UDP_IP, UDP_PORT))

	messageToDNS = "SET " + str(UDP_PORT_SERVER) + " " + SERVER_NAME

	#Seta o domínio no DNS com a porta previamente selecionada
	print("Message: ", messageToDNS)

	if( not utils.send(sock, messageToDNS, UDP_IP, UDP_PORT)):
		print("DNS não encontrado")
		quit()


	#Fecha o socket de comunicação com o DNS
	sock.close()
	print("Socket closed")

	print("Server is on")
	#criando o socket de comunicação cliente servidor
	sockd = socket(AF_INET, SOCK_DGRAM) 

	sockd.bind(('', UDP_PORT_SERVER))

	while True:
	
		messageFromClient, addr = sockd.recvfrom(1024)
		args = messageFromClient.decode().split()
		print("Aqui")
		#if(args[0] == "END"):
		#	sockd.sendto("ACK".encode(), addr)
		#	break

		t = threading.Thread(target=worker, args=(addr, messageFromClient,))
		t.start()
		sockd.setblocking(1)
	

	print("Farewell")
	#sockd.close()	

if __name__ == "__main__":
	main()
