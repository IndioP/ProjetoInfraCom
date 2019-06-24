from socket import *
#trocado por pathlib
import pathlib
import utils
from random import *

UDP_IP = "127.0.0.1"
UDP_PORT = 54210

def Main():
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
			sockd.sendto("ACK".encode(), addr)
			msg = args[1]
			utils.sendFile(sockd, msg, addr)
			print("Returned to main")
			sockd.setblocking(True)

	print("Farewell")
	sockd.close()


if __name__ == "__main__":
	Main()
