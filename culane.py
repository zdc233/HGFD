import shutil

import requests
import json
import os
import cv2
import re
import numpy as np
from PIL import Image
# 配置 ComfyUI 服务器的地址
COMFYUI_API_URL = "http://localhost:8188"

# 加载 JSON 文件
def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# 上传图片并获取文件路径
def upload_image(image_path):
    files = {'image' : open(image_path, 'rb')} 
    response = requests.post(f"{COMFYUI_API_URL}/upload/image", files=files)
    if response.status_code == 200:
        return response.json()['name']
    else:
        raise Exception(f"Failed to upload image: {response.text}")

# 发送请求到 ComfyUI 生成图片
def generate_image(json_data, seed, original_image_filename, canny_image_filename, positive_prompt, negative_prompt):

    # 构建新的 JSON 对象
    data = {
        "client_id": "1",
        "prompt": json_data 
    }
    
    # 发送请求
    response = requests.post(f"{COMFYUI_API_URL}/prompt", json=data)
    if response.status_code == 200:
        result = response.json()
        print(f"{original_image_filename} submit!")
    else:
        raise Exception(f"Failed to generate image: {response.text}")

# 下载生成的图片
def download_image(image_url, output_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded successfully: {output_path}")
    else:
        raise Exception(f"Failed to download image: {response.text}")

class CannyDetector:
    def __call__(self, img, annotator_file, low_threshold, high_threshold):
        # 对图像进行Canny边缘检测
        canny_edges = cv2.Canny(img, low_threshold, high_threshold)

        # 从标注文件中读取多边形数据
        polygons = self.read_polygons_from_file(annotator_file)

        # 创建一个与图像大小相同的掩膜
        mask = np.zeros_like(canny_edges)

        # 填充多边形区域为白色（255），表示车道线所在的区域
        for polygon in polygons:
            points = np.array(polygon, dtype=np.int32)
            cv2.fillPoly(mask, [points], color=255)  # 填充多边形内部
 
        # 使用颜色信息进一步提取车道线
        color_mask = self.get_color_mask(img)
        color_masked_edges = cv2.bitwise_and(mask, color_mask)

        # 将掩膜应用到Canny边缘图上
        combine_image = cv2.bitwise_or(canny_edges, color_masked_edges)
 
        return combine_image

    @staticmethod
    def read_polygons_from_file(file_path):
        """
        从文件中读取多边形数据
        :param file_path: 文件路径
        :return: 多边形数据列表，每个元素是一个多边形的顶点列表
        """
        polygons = []
        with open(file_path, 'r') as file:
            for line in file:
                # 将每行数据分割成坐标点
                points = line.strip().split()
                # 将坐标点转换为浮点数，并成对组合成(x, y)格式
                polygon = [(float(points[i]), float(points[i + 1])) for i in range(0, len(points), 2)]
                polygons.append(polygon)
        return polygons

    @staticmethod
    def get_color_mask(img):
        """
        创建颜色掩膜，提取白色和黄色的车道线
        :param img: 输入图像（彩色）
        :return: 颜色掩膜
        """
        # 转换到HSV颜色空间
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # 定义白色和黄色的HSV范围
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 255, 255])
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])

        # 创建白色和黄色的掩膜
        white_mask = cv2.inRange(hsv, lower_white, upper_white)
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # 合并白色和黄色掩膜
        color_mask = cv2.bitwise_or(white_mask, yellow_mask)
        return color_mask

# 主函数
def main(label, seed, json_file_path, original_image_filename, canny_image_filename, positive_prompt, negative_prompt,output_image_name):
    # 加载 JSON 文件
    json_data = load_json_file(json_file_path)

    # 更新 JSON 数据中的图片路径
    if json_file_path == json_file_path_canny_p2p:
        json_data['12']['inputs']['image'] = original_image_filename  # 原图路径
        json_data['38']['inputs']['image'] = canny_image_filename  # Canny 图路径
        json_data['6']['inputs']['text'] = positive_prompt  # 正向提示词
        json_data['7']['inputs']['text'] = negative_prompt  # 反向提示词
        json_data['3']['inputs']['seed'] = seed # 种子
        json_data['37']['inputs']['filename_prefix'] = output_image_name
    elif json_file_path == json_file_path_canny:
        json_data['12']['inputs']['image'] = canny_image_filename  # Canny 图路径
        json_data['6']['inputs']['text'] = positive_prompt  # 正向提示词
        json_data['7']['inputs']['text'] = negative_prompt  # 反向提示词
        json_data['3']['inputs']['seed'] = seed  # 种子
        json_data['37']['inputs']['filename_prefix'] = output_image_name
    else:
        raise Exception(f"Canny file format not supported: {json_file_path}")
    # 生成图片
    generate_image(json_data, seed, original_image_filename, canny_image_filename, positive_prompt, negative_prompt)


# 示例调用
if __name__ == "__main__":
    json_file_path_canny_p2p = "v11_canny_p2p.json"  # 你的 JSON 文件路径
    json_file_path_canny = "v11_canny.json"
    low_threshold = 100
    high_threshold = 200 
    
    # 定义图片和标注文件的根目录
    image_root = "./datasets/CULane_6x5k/normal"
    canny_root = "./datasets/CULane_6x5k/canny"
    annotator_root = "./datasets/CULane_6x5k/annotator"
    labels = ['snow','rain','fog','night','dusk'] 
    # labels = ['night']

    # 获取图片路径列表
    image_list = []
    canny_list = []
    annotator_file_list = []

    # 遍历图片根目录
    for root, dirs, files in os.walk(image_root):
        for file in files:
            if file.endswith(".jpg"):
                # 获取图片的完整路径
                image_path = os.path.join(root, file)
                # 生成对应的标注文件路径
                annotator_file = file.replace(".jpg", ".lines.txt")
                annotator_path = os.path.join(annotator_root, annotator_file)
                # canny_path
                canny_file = file.replace(".jpg", "_canny.png")
                canny_path = os.path.join(canny_root, canny_file)
                # 检查标注文件是否存在
                if os.path.exists(annotator_path):
                    image_list.append(image_path)
                    canny_list.append(canny_path)
                    annotator_file_list.append(annotator_path)

    image_list = sorted(image_list, key=lambda x: int(re.search(r'normal_(\d+)\.jpg', x).group(1)))
    canny_list = sorted(canny_list, key=lambda x: int(re.search(r'normal_(\d+)_canny\.png', x).group(1)))
    annotator_file_list = sorted(annotator_file_list,key=lambda x: int(re.search(r'normal_(\d+)\.lines\.txt', x).group(1)))

    # 测试用
    # image_list = image_list[:3]
    # canny_list = canny_list[:3]
    # annotator_file_list = annotator_file_list[:3]
    
    apply_canny = CannyDetector()
    
    for input_image_path, canny_image_path, annotator_file_path in zip(image_list, canny_list, annotator_file_list):
        input_image = cv2.imread(input_image_path)
        
        if input_image is None:
            print(f"Failed to load image: {input_image_path}")
            continue
            
        detected_map = apply_canny(input_image, annotator_file_path, low_threshold, high_threshold)
        cv2.imwrite(canny_image_path, detected_map)
        
        # 上传图片
        original_image_filename = upload_image(input_image_path)
        canny_image_filename = upload_image(canny_image_path)

        for label in labels:
            if label == 'night':
                seed = "190435371239247"
                positive_prompt = "change the sky to night, but not change the lane. detailed, 4k"  # 正向提示词
                negative_prompt = "Low-quality, blurry, distorted, unrealistic proportions, dull colors, out of focus, messy background, duplicate characters."  # 反向提示词
                json_file_path = json_file_path_canny_p2p
            elif label == 'dusk':
                seed = "190435371239249"
                positive_prompt = "change the sky to dusk, random add less sunset, but not change the lane. detailed, 4k"  # 正向提示词
                negative_prompt = "Low-quality, blurry, distorted, unrealistic proportions, dull colors, out of focus, messy background, duplicate characters."  # 反向提示词
                json_file_path = json_file_path_canny_p2p
            elif label == 'snow':
                seed = "5"
                positive_prompt = "falling snow, daytime"  # 正向提示词
                negative_prompt = "unrealistic proportions"  # 反向提示词
                json_file_path = json_file_path_canny
            elif label == 'rain':
                seed = "9"
                positive_prompt = "falling rain, daytime"  # 正向提示词
                negative_prompt = "Low-quality, distorted, unrealistic proportions, dull colors, out of focus, messy background, duplicate characters, foggy."  # 反向提示词
                json_file_path = json_file_path_canny
            elif label == 'fog':
                seed = "30"
                positive_prompt = "mist, daytime"  # 正向提示词
                negative_prompt = "Low-quality, blurry, distorted, unrealistic proportions, dull colors, out of focus, messy background, duplicate characters."  # 反向提示词
                json_file_path = json_file_path_canny
            else:
                raise ValueError(f"Unknown label: {label}")
            target_path = f"./datasets/CULane_6x5k/{label}"
            # 检查路径是否存在
            if not os.path.exists(target_path):
                os.makedirs(target_path)

            output_image_name = f"{label}_{original_image_filename[7:-4]}.jpg"

            main(label, seed, json_file_path, original_image_filename, canny_image_filename, positive_prompt, negative_prompt, output_image_name)

    
    
