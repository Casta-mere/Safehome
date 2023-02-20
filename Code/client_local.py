import cv2
import socket
import time
import threading



def send_data(cam_id, ip, host):
    camera = cv2.VideoCapture(cam_id)
    print(f"camera #{cam_id} ready!")

    # save video parameters
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = camera.get(cv2.CAP_PROP_FPS)
    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    size=(width, height)
    out = cv2.VideoWriter(f'video\camera_{cam_id}_1.mp4', fourcc, fps, size)
    t=time.time()
    flag_save=True
    while True:
        try:
            # initialize socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, host))
            flag = True
            while True:
                # read frame from camera, and resize it
                ret, frame = camera.read()

                # save video
                if(time.time()-t>15): 
                    out.release()
                    cv2.imwrite(f'picture\camera_{cam_id}.jpg', frame)
                    if flag_save:
                        out = cv2.VideoWriter(f'video\camera_{cam_id}_1.mp4', fourcc, fps, size)
                        flag_save=False
                    else:
                        out = cv2.VideoWriter(f'video\camera_{cam_id}_2.mp4', fourcc, fps, size)
                        flag_save=True
                    t=time.time()
                out.write(frame)

                # save picture

                #  server
                # frame = cv2.resize(frame, (0, 0),fx=0.4, fy=0.4)
                # encodepram=[int(cv2.IMWRITE_JPEG_QUALITY),40]

                # local
                frame = cv2.resize(frame, (0, 0), fx=0.8, fy=0.8)
                encodepram = [int(cv2.IMWRITE_JPEG_QUALITY), 80]

                # convert to bytes and get length
                encoded, buffer = cv2.imencode('.jpg', frame, encodepram)
                data = buffer.tobytes()
                length = len(data)
                # send length of data
                s.send(length.to_bytes(4, 'big'))
                # send data in 1024 bytes chunks each
                if(flag):
                    print(f"camera #{cam_id} connected! data length:", length)
                    flag = False
                for i in range(0, length, 1024):
                    s.send(data[i:i+1024])
                # time.sleep(0.1)
        except:
            print(f"camera #{cam_id} waiting")
            time.sleep(1)

def send_state(data,ip,host):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, host))
            flag=True
            while True:
                if(flag):
                    print(f"state transfer connected!")
                    flag=False
                s.send(data)
                time.sleep(1)
        except:
            print(f"state transfer waiting")
            time.sleep(1)

# two cameras, each has a thread
if __name__ == '__main__':
    thread = []
    # local
    info = [[0, 'localhost', 8081], [1, 'localhost', 8082], [b'{"temperature":22}','localhost', 8083]]
    
    # server
    # info=[[0,'118.31.103.3',8081],[1,'118.31.103.3',8082], [b'{"temperature":22}','118.31.103.3', 8083]]

    for i in range(2):
        thread.append(threading.Thread(target=send_data,args=(info[i][0], info[i][1], info[i][2])))
    thread.append(threading.Thread(target=send_state,args=(info[2][0],info[2][1], info[2][2])))

    for i in range(3):
        thread[i].start()

    thread[i].join()