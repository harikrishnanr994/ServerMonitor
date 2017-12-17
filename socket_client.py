import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = input("Server port? ")
sock.connect(('localhost',port))
while True:
    data = raw_input("message: ")
    sock.send(data)
    print "response: ", sock.recv(1024)
