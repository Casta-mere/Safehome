import socket

class middle_server:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.bind(('localhost', 8081))
        self.client.listen(1)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect(("localhost", 8082))
    
    def transfer(self):
        c_sock,c_addr=self.client.accept()
        while True:
            self.server.send(c_sock.recv(4096))

if __name__ == '__main__':
    middle_server = middle_server()
    middle_server.transfer()