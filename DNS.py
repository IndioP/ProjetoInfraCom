from socket import *
#IP e Porta do DNS
UDP_IP = "127.0.0.1"
UDP_PORT = 12018

sock = socket(AF_INET, SOCK_DGRAM) #criando o socket
sock.bind(('',UDP_PORT))
#sock.listen(1)
domains = dict()	#criando o dicionario, para armazenar os dominios

#padrão da mensagem com o servidor DNS
#[OP] [DOMAIN]
# - SET para definir o endereço de um dominio
# - GET para invocar o endereço de um dominio
# - END para encerrar o servidor

print("DNS is ON")
while True:
	message, addr = sock.recvfrom(1024)
	
	args = message.decode().split()
	
	print("arg: ", args)

	#print("received Option: ",args[0])	

	if(args[0] == "SET"):
		
		#Adiciona a porta como identificador e o end. IP de destino
		domains[args[2]] = addr[0] + " " + args[1]

		sock.sendto("ACK".encode(), addr)

		print("Domínios salvos: \n", domains)

	elif(args[0] == "GET"):
		message = domains[args[1]]
		sock.sendto(message.encode(), addr)

	elif(args[0] == "END"):
		break


print("Farewell")
sock.close()
