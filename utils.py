from datetime import datetime, timedelta
from random import *

def getACKSegment(socket, msg, segment):
    
    socket.settimeout(1)
    try:
        message, address = socket.recvfrom(1024)
    except:
        return False
    
    ack = message.decode().split()
    if ("ACK" in ack) :
        segment.remove(int(ack[1]))
        print("Segment ACK Received, Segment: ", ack[1])
        return True
    else:
        return False

def getACK(socket):
    
    socket.settimeout(1)
    try:
        message, address = socket.recvfrom(1024)
    except:
        return False
    ack = message.decode().split()
    if ("ACK" in ack) :
        return True
    else:
        return False

#String length in bytes
def utf8len(s):
    return len(s.encode('utf-8'))

def send(socket, msg, IP, PORT):
    
    t1 = datetime.now()
    socket.sendto(msg.encode(), (IP, PORT))
    while True:
        t2 = datetime.now()
        if(getACK(socket)):
            return True
        else:
            socket.sendto(msg.encode(), (IP, PORT))
        if(timeout(t1,t2)):
            print("Mensagem não enviada")
            return False

def sendACK(socket, addr):

    socket.sendto("ACK".encode(), addr)
    print("ACK enviado")        
	
def timeout(t1, t2):
    t3 = timedelta(seconds = 10)

    if((t2 - t1) > t3):
        return True
    return False

def hasPKT(listSegment):
        
        if not listSegment:
            return False
        return True

def sendFile(socket, msg, addr):

    #gera o primeiro segment number
    segNumber = randint(0,1000)

    print("Opening file " + msg)

    try:
        file_handle = open(msg, "rb")
        socket.sendto("ACK".encode(), addr)
    except:
        socket.sendto("404".encode(), addr)
        return

    #Lê os primeiros 1000 bytes
    last = file_handle.read(1000)

    listSegment = list()

    #Gera o número de segmento
    segNumber = randint(0,1000)

    listSegment.append(segNumber)

    #print("Numero do primeiro segmento: ", segNumber)

    #Pegamos o tempo atual
    t1 = datetime.now()

    #Lemos os próximos 1000 bytes para verificar se vai haver fragmentação ou não
    new = file_handle.read(1000)
    
    fragflag = 0

    if not new:
        fragflag = "0 "
    else:
        fragflag = "1 "

    toSend = fragflag + str(segNumber)
    length = utf8len(toSend)
    leftBytes = ""

    #Preenchemos os 24 bytes de controle com espaços
    while(length < 23):
        leftBytes = leftBytes + " "
        length = length + 1

    #Envia a primeira mensagem do arquivo para o cliente
    socket.sendto((toSend + leftBytes).encode() + last, addr)

    while hasPKT(listSegment):

        t2 = datetime.now()

        if(getACKSegment(socket, msg, listSegment) and int(fragflag) > 0):

            last = new    

            #print("ACK de segmento obtido")

            #Lemos mais 1000 bytes e criamos mais um segmento
            new = file_handle.read(1000)
            
            #Incrementamos o número de segmento em 1000
            segNumber += 1000    
            
            listSegment.append(segNumber)

            #print("Segmento atual: ", segNumber)
            #print("Fragflag: ", fragflag)
            
            segmentoAtual = listSegment[0]

            if not new:
                fragflag = "0 "
            else:
                fragflag = "1 "

            toSend = fragflag + str(segNumber)

            length = utf8len(toSend)

            #Preenchemos os bytes de controle com espaços caso o número do segmento seja pequeno
            leftBytes = ""
            while(length < 23):
                leftBytes = leftBytes + " "
                length = length + 1

            size = (toSend + leftBytes).encode() + last

            #print("Enviando: ", toSend)

            socket.sendto((toSend + leftBytes).encode() + last, addr)

            #resetamos o timer
            t1 = datetime.now()
        
        else:
            print("Reenviando Pacote")
            socket.sendto((toSend + leftBytes).encode() + last, addr)

        if timeout(t1,t2):
            print("Conexão terminada, tempo de resposta muito alto")
            break