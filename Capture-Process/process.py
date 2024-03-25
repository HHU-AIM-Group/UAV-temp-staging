import os
from PIL import Image
import cv2
import numpy as np
from tqdm import tqdm
import time

# 实景图、分割图及标签的存储位置
scenepath = "SceneImage/"
segmentationpath = "SegmentationImage/"
annotationpath = "Annotation/"
# 图片的尺寸
WIDTH, HEIGHT, DEPTH = 1920, 1080, 3
# 偏移量
delta = 5
# 图片存储主路径
PREPATHNAME = "C:\\Users\\lenovo\\Desktop\\UAV\\tres\\process"

# 车辆及对应的颜色
models = {
    "SUV": [178, 221, 213],
    "Sedan": [160, 113, 101],
    "BoxTruck": [177, 106, 230],
    "Campervan": [130, 56, 55]
}

# 车辆模型标签信息
class Car:
    def __init__(self, name, xmin, ymin, xmax, ymax):
        # 是否分割
        if 0 <= xmin <= delta or 0 <= ymin <= delta \
                or HEIGHT - delta <= xmax <= HEIGHT or WIDTH - delta <= ymax <= WIDTH:
            self.truncated = 1
        else:
            self.truncated = 0
        self.name = name
        # 检测框坐标
        self.xmin = str(xmin)
        self.ymin = str(ymin)
        self.xmax = str(xmax)
        self.ymax = str(ymax)


# 图片信息
class Picture:
    def __init__(self, path, cars=[]):
        # 图片路径
        folder, filename = os.path.split(path)
        self.path = PREPATHNAME + path
        self.folder = folder
        self.filename = filename
        # 图片其他信息
        self.database = "Unknown"
        self.width = WIDTH
        self.height = HEIGHT
        self.depth = DEPTH
        # 图片中的车辆模型信息
        self.cars = cars

files = os.listdir(segmentationpath)
picture_nums = len(files)
print("当前数据集中共有" + str(picture_nums) + "张相片")

# for pictureid in range(1, picture_nums + 1):
def imageprocess(pictureid):
    # 加载图片
    image_path = segmentationpath + "Segmentation" + str(pictureid) + ".png"
    image = Image.open(image_path)
    image_np = np.array(image)
    # 处理图片中的车辆模型信息
    car_list = []
    for key, value in models.items():
        target_color = np.array(value)
        matches = np.all(image_np[:, :, :3] == target_color, axis=-1)
        contours, _ = cv2.findContours(matches.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        bounding_boxes = [cv2.boundingRect(contour) for contour in contours]
        bounding_boxescopy = []
        for bounding_box in bounding_boxes:
            tuplecopy = list(bounding_box)
            # 过于边缘的模型删掉
            if tuplecopy[2] <= delta or tuplecopy[3] <= delta:
                continue
            tuplecopy[2] = tuplecopy[0] + tuplecopy[2]
            tuplecopy[3] = tuplecopy[1] + tuplecopy[3]
            car_list.append(Car(key, tuplecopy[0], tuplecopy[1], tuplecopy[2], tuplecopy[3]))
            bounding_boxescopy.append(tuplecopy)
        # print(key, bounding_boxescopy)

    # for p in car_list:
    #     print(p.name, p.xmin, p.ymin, p.xmax, p.ymax)
    # 输出到标签中
    pathname = scenepath + "Scene" + str(pictureid) + ".png"
    picture = Picture(pathname, car_list)
    parts = picture.filename.split(".")
    xmlname = parts[0]
    xmlname = xmlname + ".xml"
    xmlpath = annotationpath + xmlname
    # print(xmlname)
    with open(xmlpath, 'w') as f:
        f.write("<annotation>\n")
        f.write("\t<folder>" + picture.folder + "</folder>\n")
        f.write("\t<filename>" + picture.filename + "</filename>\n")
        f.write("\t<path>" + picture.path + "</path>\n")
        f.write("\t<source>\n")
        f.write("\t\t<database>" + picture.database + "</database>\n")
        f.write("\t</source>\n")
        f.write("\t<size>\n")
        f.write("\t\t<width>" + str(picture.width) + "</width>\n")
        f.write("\t\t<height>" + str(picture.height) + "</height>\n")
        f.write("\t\t<depth>" + str(picture.depth) + "</depth>\n")
        f.write("\t</size>\n")
        f.write("\t<segmented>0</segmented>\n")
        for obj in picture.cars:
            f.write("\t<object>\n")
            f.write("\t\t<name>" + obj.name + "</name>\n")
            f.write("\t\t<pose>Unspecified</pose>\n")
            f.write("\t\t<truncated>" + str(obj.truncated) + "</truncated>\n")
            f.write("\t\t<difficult>0</difficult>\n")
            f.write("\t\t<bndbox>\n")
            f.write("\t\t\t<xmin>" + obj.xmin + "</xmin>\n")
            f.write("\t\t\t<ymin>" + obj.ymin + "</ymin>\n")
            f.write("\t\t\t<xmax>" + obj.xmax + "</xmax>\n")
            f.write("\t\t\t<ymax>" + obj.ymax + "</ymax>\n")
            f.write("\t\t</bndbox>\n")
            f.write("\t</object>\n")
        f.write("</annotation>\n")

num_list = range(picture_nums)
for num in tqdm(num_list, desc='Processing data', unit='data'):
    imageprocess(num + 1)
print("数据集处理完成!")