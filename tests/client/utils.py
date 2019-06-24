from datetime import datetime, timedelta
from random import *

#TODO: Implementar timer para o ACK também
def getACK(socket, msg):

        messageFromDNS, address = socket.recvfrom(1024)	
        if(messageFromDNS.decode() == "ACK"):
            print("ACK Received")
            return True
        else:
            return False

def getACKSegment(socket, msg, IP, listSegment):
    
        messageFromDNS, address = socket.recvfrom(1024)
        ack = messageFromDNS.decode().split()
        if("ACK" in ack):
            print("Segment ACK Received, Segment: ", ack[1])
            listSegment.remove(int(ack[1]))
            return True
        else:
            return False

def timerHasExpired(t1, t2):

    #Tempo de expiração do timer em 1s
    t3 = timedelta(seconds = 1)

    #Caso tenha se passado 1 segundo, ele retorna falso
    if((t2 + t3) > t1):
        return True
    else:
        return False

#String length in bytes
def utf8len(s):
    return len(s.encode('utf-8'))

def hasPKT(listSegment):
    
    if not listSegment:
        return False
    return True

def sendPKT(socket, msg, addr):

    msglen = utf8len(msg)

    #gera o primeiro segment number
    segNumber = randint(0,1000)

    file_handle = open("test.txt", "rb")

    #Lê os primeiros 1000 bytes
    last = file_handle.read(1000)

    #Gera o número de segmento
    segNumber = randint(0,1000)

    listSegment = list()
    pkt = []

    listSegment.append(segNumber)

    #O Segmento atual a ser enviado
    segmentoAtual = listSegment[0] 

    #Pegamos o tempo atual
    t1 = datetime.now()

    #socket.sendto(("0 " + str(segNumber)+" ").encode(),addr)

    #Lemos os próximos 1000 bytes para verificar se vai haver fragmentação ou não
    new = file_handle.read(1000)

    if not new:
        fragflag = "0 "
    else:
        fragflag = "1 "

    #Envia a primeira mensagem do arquivo para o cliente
    socket.sendto((fragflag + str(segNumber) + " ").encode() + last, addr)

    while hasPKT(listSegment):

        t2 = datetime.now()
    
        print("Ainda há segmentos, num: ", segNumber)

        if(getACKSegment(socket, msg, listSegment)):
            #Remove o segmento da lista de envio
            #sendNextPKT()

            last = new    

            #Lemos mais 1000 bytes e criamos mais um segmento
            new = file_handle.read(1000)
            
            #Incrementamos o número de segmento em 1000
            segNumber += 1000    

            listSegment.append(segNumber)
            
            if not new:
                fragflag = "0 "
            else:
                fragflag = "1 "
                
            segmentoAtual = listSegment[0]

            socket.sendto((fragflag + str(segNumber) + " ").encode() + last, addr)

            #resetamos o timer
            t1 = datetime.now()

        else:
            if(timerHasExpired(t1, t2)):
                t1 = datetime.now()
                socket.sendto((fragflag + str(segNumber) + " ").encode() + last, addr)

            """else:
                waitACK()"""