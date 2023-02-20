import socket
import numpy as np
import cv2
import time
import threading
import json

class pic:
    def __init__(self,ip,host):
        self.ip=ip
        self.host=host
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind((ip,host))
        self.s.listen(1)
        self.frame=error_fig()

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
                print(f"{self.ip}:{self.host} waiting for reconnect!\n",end="")
                self.frame=error_fig()
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


def error_fig():
        return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + open('404.jpg','rb').read() + b'\r\n'

class state:
    def __init__(self,ip,host):
        self.ip=ip
        self.host=host
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind((ip,host))
        self.s.listen(1)
        self.data=23
        self.json_data={'temperature':23}

    def receive(self):
        self.conn,self.addr=self.s.accept()

        while True:
            try:
                data=self.conn.recv(1024)
                if(self.data!=data.decode() and data!=b''):
                    self.data=data.decode()
                    self.json_data['temperature']=self.data.split(":")[1].split("}")[0]
            except:
                print(f"{self.ip}:{self.host} waiting for reconnect!\n",end="")
                time.sleep(1)
                self.conn,self.addr=self.s.accept()
        
    def get(self):
        return self.json_data

def run(p):
    thread=[]
    t=threading.Thread(target=p.gen_frames)
    thread.append(t)
    t.start()

def run_2(s):
    thread=[]
    t=threading.Thread(target=s.receive)
    thread.append(t)
    t.start()

if __name__=='__main__':
    run('172.26.41.120',8081)
    print("ok")