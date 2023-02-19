import cv2
import threading

# get video from camera real-time and dispaly
def get_video():
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,360)
    cv2.namedWindow("MyCam", 0)
    cv2.resizeWindow("MyCam", 640, 360)
    cv2.setWindowProperty("MyCam", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while True:
        ret, frame = cap.read()
        cv2.imshow('MyCam', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

class VideoPlayer:
    def __init__(self, camera_index, window_name):
        # 创建一个VideoCapture对象，参数可以是设备索引或视频文件名
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(3,640)
        self.cap.set(4,360)
        cv2.namedWindow(window_name, 0)
        cv2.resizeWindow(window_name, 640, 360)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        # 创建一个窗口名，用于显示图像
        self.window_name = window_name

    def read_camera(self):
        # 从摄像头读取一帧图像
        ret, frame = self.cap.read()
        # 如果成功读取，则返回True和图像数据，否则返回False和None
        return ret, frame

    def play_video(self):
        # 循环读取和播放视频
        while True:
            # 调用read_camera函数获取图像数据
            ret, frame = self.read_camera()
            # 如果成功读取，则继续播放
            if ret:
                # 显示图像数据到对应的窗口中
                cv2.imshow(self.window_name, frame)
                # 等待用户按键
                key = cv2.waitKey(1)
                # 如果用户按下q键，则退出循环
                if key == ord('q'):
                    break

# 定义一个函数，用于创建一个VideoPlayer对象并调用play_video函数
def play_camera(camera_index, window_name):
    player = VideoPlayer(camera_index, window_name)
    player.play_video()

# 定义两个摄像头的索引和窗口名，可以根据需要修改或增加更多的摄像头
cameras = [(0, 'camera 0'), (1, 'camera 1')]

# 创建一个空列表，用于存储线程对象
threads = []

# 遍历每个摄像头的信息，创建一个线程对象并添加到列表中
for camera_index, window_name in cameras:
    thread = threading.Thread(target=play_camera, args=(camera_index, window_name))
    threads.append(thread)

# 启动每个线程对象，开始播放视频
for thread in threads:
    thread.start()

# 等待每个线程对象结束，释放资源并关闭窗口
for thread in threads:
    thread.join()
cv2.destroyAllWindows()
# if __name__ == '__main__':
#     print()
#     get_video()
