from socket import *
#IP e Porta do DNS
UDP_IP = "172.20.4.175"
UDP_PORT = 12020

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

		#precisamos saber se o domínio está registrado, caso contrário retorna 404
		if (args[1] in domains): 
			message = domains[args[1]]
		else:
			message = "404"
		sock.sendto(message.encode(), addr)

	elif(args[0] == "END"):
		break


print("Farewell")
sock.close()
