import socket
import cv2
import numpy

class VideoServer:
    def __init__(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.client.bind(("localhost", 8081))
            self.client.listen(1)
        except Exception as e:
            print(e)
            exit(0)

    def recv(self,sock,count):
        buf=b''
        while count:
            newbuf=sock.recv(count)
            if not newbuf: return None
            buf+=newbuf
            count-=len(newbuf)
        return buf

    def recv_Show(self):
        c_sock,c_addr=self.client.accept()
        while True:
            length=self.recv(c_sock,16)
            if(len(length)==16):
                stringData=self.recv(c_sock,int(length))
                data=numpy.fromstring(stringData,dtype='uint8')
                decimg=cv2.imdecode(data,1)
                cv2.imshow('SERVER',decimg)
                if cv2.waitKey(10)==27:
                    break

        cv2.destroyAllWindows()

if __name__ == '__main__':
    server=VideoServer()
    server.recv_Show()