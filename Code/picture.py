import socket
import numpy as np
import cv2
import time
import threading

class pic:
    def __init__(self,ip,host):
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind((ip,host))
        self.s.listen(1)
        self.frame=None
        self.conn,self.addr=self.s.accept()

    def receive(self):
        while True:
            t=time.time()
            data=b''
            length_bytes=self.conn.recv(4)
            length=int.from_bytes(length_bytes,'big')
            #print(length)
            while len(data)<length:
                data+=self.conn.recv(1024)
                if(length>3000000):
                    print(len(data),length)
                    break
            #print(f'len data={len(data)}')
            try:        
                array=np.frombuffer(data,dtype=np.uint8)
                frame=cv2.imdecode(array,cv2.IMREAD_COLOR)
                yield frame
            except:
                pass
                
    def gen_frames(self):
        for frame in self.receive():
            try:
                encoded,buffer=cv2.imencode('.jpg',frame)
                data=buffer.tobytes()
                temp=(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + data + b'\r\n')
                if(self.frame!=temp):
                    self.frame=temp
                    #print('new frame!')
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