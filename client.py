def showOptions():
	print("Digite : \"GET [ARQUIVO]\" para baixar o [ARQUIVO]\n")
	print("Digite \"LST\" para listar os arquivos no Dominio\n")
	print("Digite \"END\" para encerrar a comunicação\n")


from socket import *
UDP_IP = "127.0.0.1"
UDP_PORT = 12016

sock = socket(AF_INET, SOCK_STREAM) #socket de comunicação servidor cliente
sock.connect((UDP_IP,UDP_PORT))
message = input("QUAL Servidor você deseja acessar?\n")
message = "GET " + message
sock.send(message.encode())
answer = sock.recv(1024).decode().split()
#print(answer)
sock2 = socket(AF_INET, SOCK_STREAM)	#criando o socket de comunicação cliente servidor
sock2.connect((answer[0], int(answer[1])))
while True:
	showOptions()
	op = input()
	sock2.send(op.encode())
	if(op == "END"):
		break
	
sock2.close()
sock.close()

