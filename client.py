def showOptions():
	print("Digite : \"GET [ARQUIVO]\" para baixar o [ARQUIVO]\n")
	print("Digite \"LST\" para listar os arquivos no Dominio\n")
	print("Digite \"END\" para encerrar a comunicação\n")


from socket import *
import utils
UDP_IP = "127.0.0.1"
UDP_PORT = 12019

def main():
	sock = socket(AF_INET, SOCK_DGRAM) #socket de comunicação servidor cliente

	serv = ""

	message = input("QUAL Servidor você deseja acessar? - Digite Q para sair \n")

	option = True
	DNSok = False
	isOk = True

	while option:
		
		if(message == "Q"):
			quit()

		message = "GET " + message

		#print(message)

		sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
		answer, servAddress = sock.recvfrom(2048)


		#Verificamos se o domínio existe
		if(answer.decode() == "404"):
			print("Erro 404 - Endereço não encontrado, digite novamente ou digite 'Q' para sair")
			message = input()
		else:
			DNSok = True
			option = False
			serv = answer.decode().split()
			sock.close()



	while (True and DNSok):

		#criando o socket de comunicação cliente servidor
		sock2 = socket(AF_INET, SOCK_DGRAM)	

		print("Servidor Porta: ", serv[1])
		print("Servidor IP: ", serv[0])

		sock2.sendto("ACK".encode(), (serv[0], int(serv[1])))
		showOptions()
		op = input()
		
		
		if(not utils.send(sock2, op, serv[0], int(serv[1]))):
			print("Erro, servidor não recebeu mensagem")
			isOk = False
		else:
			print("Servidor recebeu mensagem")
			isOk = True
		
		op = op.split()

		if(op[0] == "END"):
			break
		
		if(op[0] == "LST" and isOk):
			resposta, addrServer = sock2.recvfrom(1024)
			print(resposta.decode())

		if(op[0] == "GET" and isOk):
				print("GET " + op[1])
				f = open("client/"+op[1], "wb")

				while True:
					sock2.setblocking(True)
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

					sock2.sendto(("ACK " + segmento[1]).encode(), addrServer)

					if(fragflag == "0"):
						break
						

				f.close()

		sock2.close()

if __name__ == "__main__":
	main()

