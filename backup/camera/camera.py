import cv2
import socket
import numpy
# get video from camera real-time and dispaly


def get_video():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1920)
    cap.set(4, 1080)
    cv2.namedWindow("MyCam", 0)
    cv2.resizeWindow("MyCam", 1920, 1080)
    cv2.setWindowProperty(
        "MyCam", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


class camera:
    def __init__(self, device_id, server):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((server[0], server[1]))

        self.cap = cv2.VideoCapture(device_id)
        self.cap.set(3, 1920)
        self.cap.set(4, 1080)
        self.img_fps = 30

    def send(self):
        for i in range(10000):
            data=f"{i}"
            self.server.send(data.encode())
            print(data)
        # while(True):
        #     self.server.send("1".encode())
            # print("1")
            # ret, image = self.cap.read()
            # image = cv2.resize(image, (1920, 1080))
            # image = cv2.imencode('.jpg', image)
            # data = image[1].tobytes()
            # try:
            #     self.server.send(data)
            # except Exception as e:
            #     print(e)
            #     self.cap.release()
            #     self.server.close()
            #     exit(0)
            # return image[1].tobytes()


if __name__ == '__main__':
    print(1)
    c = camera(0, ('localhost', 8081))
    c.send()
