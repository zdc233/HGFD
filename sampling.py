import os
import random
import shutil

# 定义文件路径
base_path = './data/CULane'
out_dir = './data/HGLane'
test_file_path = f"{base_path}/list/test_split/test0_normal.txt"
normal_dir = f"{out_dir}/normal"
canny_dir = f"{out_dir}/canny"
snow_dir = f"{out_dir}/snow"
rain_dir = f"{out_dir}/rain"
fog_dir = f"{out_dir}/fog"
night_dir = f"{out_dir}/night"
dusk_dir = f"{out_dir}/dusk"
list_dir = f"{out_dir}/list"
laneseg_label_w16_dir = f"{out_dir}/laneseg_label_w16"

# 确保目标文件夹存在
os.makedirs(normal_dir, exist_ok=True)
os.makedirs(canny_dir, exist_ok=True)
os.makedirs(snow_dir, exist_ok=True)
os.makedirs(rain_dir, exist_ok=True)
os.makedirs(fog_dir, exist_ok=True)
os.makedirs(night_dir, exist_ok=True)
os.makedirs(dusk_dir, exist_ok=True)
os.makedirs(list_dir, exist_ok=True)
os.makedirs(laneseg_label_w16_dir, exist_ok=True)

# 读取图片路径
with open(test_file_path, 'r') as file:
    image_paths = [line.strip() for line in file.readlines()]  # 使用strip()去除多余空格和换行符

# 系统抽样
# m = random.randint(0, 9)  # 随机生成一个0到9的数
m = 1
selected_images = []
for i in range(1,4501):  # 抽取4500张图片
    index = m + i * 2
    if index < len(image_paths):  # 确保索引在图片列表范围内
        selected_images.append(image_paths[index])
for i in range(9100,9600):
    selected_images.append(image_paths[i])

# 复制图片和标注文件
for idx, image_path in enumerate(selected_images):
    # 获取图片的完整路径
    full_image_path = os.path.join(base_path, image_path)
    # 获取标注文件的完整路径
    annotator_file = image_path.replace(".jpg", ".lines.txt")
    full_annotator_path = os.path.join(base_path, annotator_file)

    # 生成新的文件名
    new_image_name = f"normal_{idx}.jpg"
    new_annotator_name_normal = f"normal_{idx}.lines.txt"
    new_annotator_name_snow = f"snow_{idx}.lines.txt"
    new_annotator_name_rain = f"rain_{idx}.lines.txt"
    new_annotator_name_fog = f"fog_{idx}.lines.txt"
    new_annotator_name_night = f"night_{idx}.lines.txt"
    new_annotator_name_dusk = f"dusk_{idx}.lines.txt"

    # 生成新的文件路径
    new_image_path = os.path.join(normal_dir, new_image_name)
    new_annotator_path_normal = os.path.join(normal_dir, new_annotator_name_normal)
    new_annotator_path_snow = os.path.join(snow_dir, new_annotator_name_snow)
    new_annotator_path_rain = os.path.join(rain_dir, new_annotator_name_rain)
    new_annotator_path_fog = os.path.join(fog_dir, new_annotator_name_fog)
    new_annotator_path_night = os.path.join(night_dir, new_annotator_name_night)
    new_annotator_path_dusk = os.path.join(dusk_dir, new_annotator_name_dusk)

    # 检查文件是否存在
    if not os.path.exists(full_image_path):
        print(f"图片文件不存在: {full_image_path}")
        continue
    if not os.path.exists(full_annotator_path):
        print(f"标注文件不存在: {full_annotator_path}")
        continue

    # 复制图片和标注文件
    shutil.copy(full_image_path, new_image_path)
    shutil.copy(full_annotator_path, new_annotator_path_normal)
    shutil.copy(full_annotator_path, new_annotator_path_snow)
    shutil.copy(full_annotator_path, new_annotator_path_rain)
    shutil.copy(full_annotator_path, new_annotator_path_fog)
    shutil.copy(full_annotator_path, new_annotator_path_night)
    shutil.copy(full_annotator_path, new_annotator_path_dusk)

print("完成图片和标注文件的复制与重命名。")
