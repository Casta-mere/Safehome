import socket
s=socket.socket()
host="118.31.103.3"
port=8081
info="hello"
s.connect((host,port))
s.send(info.encode())
s.close()