import os
import random
import shutil

# 定义文件路径
test_file_path = "/home/zdc233/PycharmProjects/datasets/CULane/list/test_split/test0_normal.txt"
normal_dir = "./datasets/CULane100_2_500-999/normal"
annotator_dir = "./datasets/CULane100_2_500-999/annotator"
base_path = "/home/zdc233/PycharmProjects/datasets/CULane"

# 确保目标文件夹存在
os.makedirs(normal_dir, exist_ok=True)
os.makedirs(annotator_dir, exist_ok=True)

# 读取图片路径
with open(test_file_path, 'r') as file:
    image_paths = [line.strip() for line in file.readlines()]  # 使用strip()去除多余空格和换行符

# 系统抽样
# m = random.randint(0, 9)  # 随机生成一个0到9的数
m = 1
selected_images = []
for i in range(1,9000):  # 抽取1000张图片
    index = m + i * 2
    if index < len(image_paths):  # 确保索引在图片列表范围内
        selected_images.append(image_paths[index])



# 复制图片和标注文件
for idx, image_path in enumerate(selected_images):
    # 获取图片的完整路径
    full_image_path = os.path.join(base_path, image_path)
    # 获取标注文件的完整路径
    annotator_file = image_path.replace(".jpg", ".lines.txt")
    full_annotator_path = os.path.join(base_path, annotator_file)

    # 生成新的文件名
    new_image_name = f"normal_{idx}.jpg"
    new_annotator_name = f"normal_{idx}.lines.txt"

    # 生成新的文件路径
    new_image_path = os.path.join(normal_dir, new_image_name)
    new_annotator_path = os.path.join(annotator_dir, new_annotator_name)

    # 检查文件是否存在
    if not os.path.exists(full_image_path):
        print(f"图片文件不存在: {full_image_path}")
        continue
    if not os.path.exists(full_annotator_path):
        print(f"标注文件不存在: {full_annotator_path}")
        continue

    # 复制图片和标注文件
    shutil.copy(full_image_path, new_image_path)
    shutil.copy(full_annotator_path, new_annotator_path)

print("完成图片和标注文件的复制与重命名。")
