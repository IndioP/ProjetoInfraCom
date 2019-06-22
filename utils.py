from datetime import datetime, timedelta
from random import *
class UDPReliable:
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

        listSegment = list()
        pkt = []

        if(msglen > 1000):
            createPKT(listSegment, msglen, msg, pkt)
        else:
            listSegment.append(segNumber)

        #O Segmento atual a ser enviado
        segmentoAtual = listSegment[0] 

        #Pegamos o tempo atual
        t1 = datetime.now()

        #socket.sendto(("0 " + str(segNumber)+" ").encode(),addr)

        while hasPKT(listSegment):

            t2 = datetime.now()
        
            if(getACKSegment(socket, msg, listSegment)):
                #Remove o segmento da lista de envio
                #sendNextPKT()
                #Como demos um pop, pegamos sempre o primeiro valor
                segmentoAtual = listSegment[0]

                #resetamos o timer
                t1 = datetime.now()

            else:
                if(timerHasExpired(t1, t2)):
                    t1 = datetime.now()
                    #resendPKT()
                    socket.sendto(("0 " + str(segNumber)+" ").encode(),addr)
                """else:
                    waitACK()"""