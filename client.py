def showOptions():
	print("digite 1 para solicitar um Arquivo\n")
	print("Digite 2 para listar os arquivos disponiveis\n")
	print("Digite 3 para encerrar a conexão\n")

showOptions()

from socket import *
UDP_IP = "127.0.0.1"
UDP_PORT = 12014
message = "END"

sock = socket(AF_INET, SOCK_STREAM)
sock.connect((UDP_IP,UDP_PORT))
sock.send(message.encode())
answer = sock.recv(1024).decode()
print(answer)
sock.close()

