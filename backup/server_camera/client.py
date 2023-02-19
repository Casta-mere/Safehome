import socket
import cv2
import numpy

class CaptureCam:

    def __init__(self):
        self.server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect(('118.31.103.3', 8081))

        self.resolution = (1920,1080)
        self.img_fps =30
        self.img=''
        self.img_data='empty'

    def send(self):
        cam=cv2.VideoCapture(0)
        img_param=[int(cv2.IMWRITE_JPEG_QUALITY),self.img_fps]

        while True:
            ret,self.img=cam.read()
            self.img=cv2.resize(self.img,self.resolution)
            ret,img_encode=cv2.imencode('.jpg',self.img,img_param)
            img_code=numpy.array(img_encode)
            self.img_data=img_code.tobytes()
            try:
                self.server.send(str(len(self.img_data)).ljust(16).encode())
                self.server.send(self.img_data)
            except Exception as e:
                print(e)
                cam.release()
                self.server.close()
                exit(0)

if __name__ == '__main__':
    cam=CaptureCam()
    cam.send()