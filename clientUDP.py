def showOptions():
	print("Digite : \"GET [ARQUIVO]\" para baixar o [ARQUIVO]\n")
	print("Digite \"LST\" para listar os arquivos no Dominio\n")
	print("Digite \"END\" para encerrar a comunicação\n")


from socket import *
import utils
UDP_IP = "127.0.0.1"
UDP_PORT = 12019

sock = socket(AF_INET, SOCK_DGRAM) #socket de comunicação servidor cliente

message = input("QUAL Servidor você deseja acessar?\n")
message = "GET " + message

print(message)

sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
answer, servAddress = sock.recvfrom(2048)
serv = answer.decode().split()
print(answer.decode().split())
sock.close()

while True:
	#criando o socket de comunicação cliente servidor
	sock2 = socket(AF_INET, SOCK_DGRAM)	
	sock2.sendto("ACK".encode(), (serv[0], int(serv[1])))
	showOptions()
	op = input()
	sock2.sendto(op.encode(),(serv[0], int(serv[1])))
	utils.getACK(sock2,op,serv[0],int(serv[1]))
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
			aux = resposta.split()
			resposta = resposta[len(aux[0])+1+len(aux[1])+1:]
			print(resposta)
			if(aux[0] == "0"):
				break
			if(aux[0] == "1"):
				print("chegou 1")

	sock2.close()
