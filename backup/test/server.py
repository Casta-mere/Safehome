import socket

host="192.168.27.148"
port=8081
s=socket.socket()
s.bind((host,port))
s.listen(5)
while True:
    c,addr=s.accept()
    print('Got connection from',addr)
    c.send('Thank you for connecting'.encode())
    c.close()