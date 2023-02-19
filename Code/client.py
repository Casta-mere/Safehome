import cv2
import socket
import time
import threading


def send_data(cam_id, ip, host):
    camera = cv2.VideoCapture(cam_id)
    print(f"camera {cam_id} ready!")
    while True:
        try:
            # initialize socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, host))
            flag = True
            while True:
                # read frame from camera, and resize it
                ret, frame = camera.read()

                #  server
                frame = cv2.resize(frame, (0, 0),fx=0.4, fy=0.4)
                encodepram=[int(cv2.IMWRITE_JPEG_QUALITY),40]

                # local
                # frame = cv2.resize(frame, (0, 0), fx=0.9, fy=0.9)
                # encodepram = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

                # convert to bytes and get length
                encoded, buffer = cv2.imencode('.jpg', frame, encodepram)
                data = buffer.tobytes()
                length = len(data)
                # send length of data
                s.send(length.to_bytes(4, 'big'))
                # send data in 1024 bytes chunks each
                if(flag):
                    print(f"camera #{cam_id}connected! data length:", length)
                    flag = False
                for i in range(0, length, 1024):
                    s.send(data[i:i+1024])
                time.sleep(0.1)
        except:
            print(f"camera #:{cam_id} waiting")
            time.sleep(1)


# two cameras, each has a thread
if __name__ == '__main__':
    thread = []
    info = [[0, 'localhost', 8081], [1, 'localhost', 8082]]
    # info=[[0,'118.31.103.3',8081],[1,'118.31.103.3',8082]]

    for i in range(2):
        thread.append(threading.Thread(target=send_data,
                      args=(info[i][0], info[i][1], info[i][2])))

    for i in range(2):
        thread[i].start()

    thread[i].join()
