import time
import cv2
import time
import os.path
import requests
import json
import base64
import datetime
from django.http import JsonResponse
from demo import nmg
import threading
import requests
from requests.auth import HTTPDigestAuth

session = None
login={
    "session": 0,
    "id": 2,
    "call": {
        "service": "rpc",
        "method": "login"
    },
    "params": {
        "userName": "admin",
        "password": "f16f6723ee0b58f33161066d93cd2e01",
        "random": "WKNQ3H",
        "ip": "127.0.0.1",
        "port": 80,
        "encryptType": 0
    }
}
hert ={"session":session,
"id":2,
"call":{"service":"rpc","method":"keepAlive"},
"params":{"timeout":50}
}
# move:云台动作指令
# 0：停止
# 1：向上
# 2：向下
# 3：向左
# 4：向右
# 5：变倍小
# 6：变倍大
# speed_h:水平速度等级，取值范围0~63
# speed_v:垂直速度等级，取值范围0~63
# speed_z:变倍速度等级，取值范围1~20
ptz={
    "move":0,
    "soeed_h":20,
    "speed_V":20,
    "speed_z":16
}



def Login():
    global session
    response = requests.post('http://192.168.5.116/SDK/UNIV_API/', json.dumps(login))
    req=response.json()
    print(req)
    if req['result']:
        session = req['params']['session']
        Hert()
def Hert():
    global session
    response = requests.post('http://192.168.5.116/SDK/UNIV_API/', json.dumps(hert))
    req=response.json()
    # print(req)
    # session = req['params']['session']

#截图
def Jpg():
    global session
    datatimes = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')  # 获取当前时间
    try:
        print('开始截图')
        Login()
        kjpg = {"session": session,
                "id": 2,
                "call": {"service": "snap", "method": "getSnapData"},
                "params": {"quality": 50}
                }
        response = requests.post('http://192.168.5.116/api/v1/jpgdata/', json.dumps(kjpg))
        req = response.json()
        if req['result']:
            img =req['params']['Data']
            imgdata = base64.b64decode(img)
            file = open(r"images/UpperComputer//"+datatimes+'.jpg', 'wb')
            file.write(imgdata)
            file.close()
            # 开启温度监测
            # nmg(r"./images/UpperComputer//"+datatimes+'.jpg',datatimes)
            S = threading.Thread(target=nmg,args=(r"./images/UpperComputer//"+datatimes+'.jpg',datatimes))
            S.start()
    except Exception as e:
        print('失败',e)

#海康威视截图
def hkwspg():
    try:
        datatimes = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')  # 获取当前时间
        # print('开始截图')
        url = f'http://192.168.5.116/ISAPI/Streaming/channels/1/picture'
        ptz_pre = requests.get(url, auth=HTTPDigestAuth('admin', 'sshw1234'), stream=True)
        with open(r"./images/UpperComputer//"+datatimes+'.jpg', 'wb') as f:
            f.write(ptz_pre.content)
        # print("抓取一张可见光图像")
        S = threading.Thread(target=nmg, args=(r"./images/UpperComputer//" + datatimes + '.jpg', datatimes,4))
        S.start()
        # url = "rtsp://admin:sshw1234@192.168.5.166/Streaming/Channels/1"
        # # rtsp://用户名:密码@ip地址/Streaming/Channels/1最后面的1是因为我选择1会显示出我要的内容，有的是1或者3或者4
        # cap = cv2.VideoCapture(url)
        # ret, frame = cap.read()
        # cv2.imshow("frame", frame)
        # print(frame)
        # # while ret:  # 不断的刷新 ret=True
        # #     ret, frame = cap.read()
        # #     cv2.imshow("frame", frame)
        # #     file = "E:/pic/{}.jpg".format(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))  # 以日期来命名文件并指定文件夹
        # #     if (os.path.isfile(file) == False and int(time.strftime("%S", time.localtime())) % 5 == 0):  # 每5s截图
        # #         cv2.imwrite(file, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])  # 无损输出图片 但是图片质量仍不是很高
        # #     if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q退出
        # #         break
        # cv2.destroyAllWindows()  # 全屏显示
        # cap.release()  # 关闭
    except Exception as e:
        print('失败',e)

while True:
    time.sleep(4)
    hkwspg()
# hkwspg()

