import socket

class VideoServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
        self.sock.bind(("localhost", 8081))
        self.sock.listen(1)
    
    def recv(self):
        while True:
            client,addr=self.sock.accept()
            self.img=self.handle_request(client)
            print(self.img)

    def handle_request(self,client):
        buf=client.recv(1024)
        return buf
    
        


if __name__ == '__main__':
    server=VideoServer()
    server.recv()