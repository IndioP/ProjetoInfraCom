from threading import Timer

#TODO: Implementar timer para o ACK também
def getACK(socket, msg, IP, port):

        messageFromDNS, address = socket.recvfrom(1024)	
        if(messageFromDNS.decode() == "ACK"):
            print("ACK Received")
            return True
        else:
            return False

def getACKSegment(socket, msg, IP, port, listSegment):
    
        messageFromDNS, address = socket.recvfrom(1024)
        ack = messageFromDNS.decode().split()
        if("ACK" in ack):
            print("Segment ACK Received, Segment: ", ack[1])
            return True
        else:
            return False


def sendPKTAgain(socket, msg, IP, port):
    
    #O pacote vai ser enviado para o cliente e vai esperar um tempo para receber um ack

    #Envia o primeiro segmento
    sock.send(message.encode(), (IP, port))

def sendPKT(socket, msg, IP, port):

    listSegment = list()
    #Criamos um timer para a resposta do cliente
    timer = Timer(1.0, sendPKTAgain(socket, msg, IP, port))
    
    while hasPKT():
        if(getACK(socket, msg, IP, port)):
            sendNextPKT()
            resetTimer()
        else:
            if(timer.hasExpired()):
                resendPKT()
            else:
                waitACK()