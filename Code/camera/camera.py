import cv2
# get video from camera real-time and dispaly
def get_video():
    cap = cv2.VideoCapture(0)
    cap.set(3,1920)
    cap.set(4,1080)
    cv2.namedWindow("MyCam", 0)
    cv2.resizeWindow("MyCam", 1920, 1080)
    cv2.setWindowProperty("MyCam", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    print(1)
    get_video()
