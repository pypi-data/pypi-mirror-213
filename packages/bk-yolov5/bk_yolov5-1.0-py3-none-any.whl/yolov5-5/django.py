from PIL import Image,ImageDraw
import torch
import cv2
import numpy as np
from models.experimental import attempt_load
from utils.general import non_max_suppression, scale_coords,check_img_size
from utils.datasets import letterbox
import datetime

def helmet_detection():
    # 获取请求中的文件
    image_file = 'E:/MachineLearning/databases/Underground_dressing/val/images/2019-11-18_114318.jpg'

    # 打开图像
    # image = Image.open(image_file)
    # image.show()
    image = cv2.imread(image_file)
    # 调整图像大小以适合模型
    input_size = (640, 640)
    img = letterbox(image, new_shape=input_size)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)
    img = np.ascontiguousarray(img)

    # 将图像转换为tensor
    img = torch.from_numpy(img).unsqueeze(0).to(device="cuda")
    # 加载模型
    model = attempt_load("runs/train/exp50/weights/last.pt", map_location="cuda")
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(640, s=stride)  # check img_size
    # 预测
    with torch.no_grad():
        # pred = model(img)
        pred = model(torch.zeros(1, 3, imgsz, imgsz).to("cuda").type_as(next(model.parameters())))  # run once

    # 后处理
    print('pred',pred)
    detections = non_max_suppression(pred, conf_thres=0.5, iou_thres=0.5)
    detections = detections[0]
    # 绘制检测结果
    if detections is not None:
        for x1, y1, x2, y2, conf, cls_conf, cls in detections:
            if int(cls) == 1:
                x1, y1, x2, y2 = scale_coords(img.shape[2:], (x1, y1, x2, y2), image.size).round()
                draw = ImageDraw.Draw(image)
                draw.rectangle((x1, y1, x2, y2), outline='red', width=3)
    # 返回图像
    # response = HttpResponse(content_type="image/jpeg")
    # image.save(response, "JPEG")

# helmet_detection()



def helmet():
    # 加载模型
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', path='runs/train/standard/weights/last.pt', source='local')
    # 定义标签的名称，这里只用到了一类安全帽
    class_names = [ 'helmet', 'workingClothes', 'no-helmet','no-workingClothes']
    # 加载待识别的图片
    img = Image.open('E:/MachineLearning/databases/Underground_dressing/standard/val/images/2019-11-18_114318.jpg')
    # 将图片转换为numpy数组并调整大小
    img = np.array(img)
    img = model.letterbox(img, new_shape=640)[0]

    # 使用模型进行预测
    results = model(img)
    # 获取预测结果中的安全帽
    pred = results.pred[0][results.pred[0][:, 5] == 0]

    # 如果有安全帽的预测框，则认为检测到了安全帽
    if pred.size(0) > 0:
        print('This image contains a helmet.')
    else:
        print('This image does not contain a helmet.')

# helmet()

WaterTimeOpen = (datetime.datetime.now() + datetime.timedelta(seconds=20)).strftime('%H:%M:%S')