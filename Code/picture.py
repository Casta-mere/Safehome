import socket
import numpy as np
import cv2
import time
import threading

class pic:
    def __init__(self,ip,host):
        self.ip=ip
        self.host=host
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind((ip,host))
        self.s.listen(1)
        self.frame=None

    def receive(self):
        self.conn,self.addr=self.s.accept()

        while True:
            try:
                data=b''
                length_bytes=self.conn.recv(4)
                length=int.from_bytes(length_bytes,'big')

                while len(data)<length:
                    data+=self.conn.recv(1024)
                    if(length>3000000):
                        print('tcp error! : data too long')
                        break
                try:
                    array=np.frombuffer(data,dtype=np.uint8)
                    frame=cv2.imdecode(array,cv2.IMREAD_COLOR)
                    yield frame
                except:
                    pass
            except:
                print(f"{self.ip}:{self.host} waiting for reconnect!\n")
                time.sleep(1)
                self.conn,self.addr=self.s.accept()
            
    def gen_frames(self):
        for frame in self.receive():
            try:
                encoded,buffer=cv2.imencode('.jpg',frame)
                data=buffer.tobytes()
                temp=(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + data + b'\r\n')
                if(self.frame!=temp):
                    self.frame=temp
            except:
                pass
                
    def get(self):
        while True:
            yield self.frame
            
def run(p):
    thread=[]
    t=threading.Thread(target=p.gen_frames)
    thread.append(t)
    t.start()

if __name__=='__main__':
    run('172.26.41.120',8081)
    print("ok")