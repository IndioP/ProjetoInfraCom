from socket import *
import utils

UDP_IP = "127.0.0.1"
UDP_PORT = 54210

def showOptions():
	print("Digite : \"GET ARQUIVO\" para baixar o arquivo\n")
	print("Digite \"LST\" para listar os arquivos no Dominio\n")
	print("Digite \"END\" para encerrar a comunicação\n")


def Main():

	isOk = True

	while True:

		#criando o socket de comunicação cliente servidor
		sock2 = socket(AF_INET, SOCK_DGRAM)	

		showOptions()
		op = input()
		
		if(not utils.send(sock2, op, UDP_IP, UDP_PORT)):
			print("Erro, servidor não recebeu mensagem")
			isOk = False
		else:
			print("Servidor recebeu mensagem")
			isOk = True

		op = op.split()

		if(op[0] == "END" and isOk):
			break

		if(op[0] == "LST" and isOk):
			
			resposta, addrServer = sock2.recvfrom(1024)
			print(resposta.decode())

		if(op[0] == "GET" and isOk):
			
			print("GET " + op[1])
			f = open("new_"+op[1], "wb")

			while True:
				resposta, addrServer = sock2.recvfrom(1024)

				#print("Receiving bytes: ", len(resposta))

				#resposta = resposta.decode()
				#print(resposta)
				#primeiros 24 bytes são de controle
				segmento = resposta[:23]
				
				#Os 1000 bytes restantes são os dados
				data = resposta[23:]

				#Pegamos o número do segmento enviado pelo servidor
				segmento = segmento.decode().split()

				print(segmento)

				#print(data)			

				f.write(data)

				#print("Segmento: ", segmento[1])

				fragflag = segmento[0]
				#seg = input("Digite o segmento de resposta: ")

				sock2.sendto(("ACK " + segmento[1]).encode(), (UDP_IP, UDP_PORT))

				if(fragflag == "0"):
					break
					

			f.close()



	sock2.close()

if __name__ == "__main__":
	Main()
