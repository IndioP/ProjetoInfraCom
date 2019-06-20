def getACK(socket, msg, IP, port):
    while True:
        messageFromDNS, address = socket.recvfrom(1024)	
        if(messageFromDNS.decode() == "ACK"):
            print("ACK Received")
            return True
        else:
            sock.send(messageToDNS.encode(), (IP, port))
