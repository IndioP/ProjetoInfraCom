def showOptions():
	print("Digite : \"GET [ARQUIVO]\" para baixar o [ARQUIVO]\n")
	print("Digite \"LST\" para listar os arquivos no Dominio\n")
	print("Digite \"END\" para encerrar a comunicação\n")


from socket import *
import utils

def send(sock, msg):

	sock.sendto(msg.encode(),(UDP_IP, UDP_PORT))

UDP_IP = "127.0.0.1"
UDP_PORT = 54210

while True:

	#criando o socket de comunicação cliente servidor
	sock2 = socket(AF_INET, SOCK_DGRAM)	

	showOptions()
	op = input()
	sock2.sendto(op.encode(),(UDP_IP, UDP_PORT))

	op = op.split()

	if(op[0] == "END"):
		break

	if(op[0] == "LST"):
		
		resposta, addrServer = sock2.recvfrom(1024)
		print(resposta.decode())

	if(op[0] == "GET"):
		while True:
			resposta, addrServer = sock2.recvfrom(1024)
			resposta = resposta.decode()
			#print(resposta)
			
			segmento = resposta.split()

			print("Segmento: ", segmento[1])

			send(sock2, "ACK " + segmento[1])
			
			fragflag = segmento[0]
			if(fragflag == "0"):
				break

			"""
			aux = resposta.split()
			resposta = resposta[len(aux[0])+1+len(aux[1])+1:]
			print(resposta)
			if(aux[0] == "0"):
				break
			if(aux[0] == "1"):
				print("chegou 1")"""
			



sock2.close()
