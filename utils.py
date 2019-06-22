from datetime import datetime, timedelta

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

def timerHasExpired(t1, t2):

    #Tempo de expiração do timer em 1s
    t3 = timedelta(seconds = 1)

    #Caso tenha se passado 1 segundo, ele retorna falso
    if((t2 + t3) > t1):
        return True
    else:
        return False

def sendPKT(socket, msg, IP, port):


    file_handle = open(args[1], "rb")
    last = file_handle.read(1000)
    segNumber = randint(0,1000)
    
    while True:
        new = file_handle.read(1000)
        if not new: 															#if EOF
            sockd.sendto(("0 " + str(segNumber)+" ").encode() + last,addr)
            break
        sockd.sendto(("1 "+ str(segNumber)+" ").encode() + last,addr)
        segNumber+=1000
        last = new
    
    file_handle.close()

    listSegment = list()
    #Criamos um timer para a resposta do cliente
    
    #Pegamos o tempo atual
    t1 = datetime.now()
    sendPKT()

    while hasPKT():

        t2 = datetime.now()
        if(getACK(socket, msg, IP, port)):
            sendNextPKT()
            resetTimer()
        else:
            if(timerHasExpired(t1, t2)):
                t1 = datetime.now()
                resendPKT()
            else:
                waitACK()