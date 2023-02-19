import socket

global image


class CaptureCam:

    def __init__(self):
        self.addr=("localhost",8082)
        self.image=b""

    def get(self):
        print("start")
        while True:
            self.server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect(self.addr)
            data=b'I want file'
            self.server.send(data)
            self.image=self.server.recv(999999)

      
    def get_image(self):
        return self.image

# c=CaptureCam()
# print(c.get_image())
# c.get()
