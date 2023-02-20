# 这是接收端的代码，需要运行在服务器上，并使用flask框架提供网页服务
from flask import Flask, render_template, Response
import picture as pc

# 创建一个Flask对象，用于处理网页请求和响应
app = Flask(__name__)


# p1=pc.pic('172.26.41.120',8081)
# p2=pc.pic('172.26.41.120',8082)
# s=pc.state('172.26.41.120',8083)
p1=pc.pic('localhost',8081)
p2=pc.pic('localhost',8082)
s=pc.state('localhost',8083)

pc.run(p1)
pc.run(p2)
pc.run_2(s)

@app.route('/')
def index():
    # 处理根路径的请求，返回index.html模板页面 
    data=s.get()
    t=data['temperature']
    p=int(int(t)/40*100)
    return render_template('index.html',temperature=t,percentage=p)

@app.route('/surveillance')
def surveillance():
    return render_template('camera.html')

@app.route('/camera1')
def camera1():
    return render_template('camera1.html')

@app.route('/camera2')
def camera2():
    return render_template('camera2.html')

@app.route('/statistics')
def statistics():
    return render_template('profile.html')

@app.route('/video_feed_1')
def video_feed_1():
    # 处理视频流路径的请求，返回
    return Response(p1.get(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_2')
def video_feed_2():
    # 处理视频流路径的请求，返回
    return Response(p2.get(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_null')
def video_feed_null():
    # 处理视频流路径的请求，返回
    return Response(pc.error_fig(), mimetype='multipart/x-mixed-replace; boundary=frame')

def server_run():
    app.run(host='0.0.0.0', port=80)

def local_run():
    app.run(host='0.0.0.0', port=5000,debug=True,use_reloader=False)    
    
if __name__ == '__main__':
    local_run()