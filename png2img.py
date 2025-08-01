import os
from PIL import Image

# 定义当前目录
current_dir = "./tmpdata"  # 当前目录
new_dir = "./tmpdata_new"

# 遍历当前目录中的所有文件
for filename in os.listdir(current_dir):
    # 检查文件是否是图片文件（支持常见图片格式）
    if filename.lower().endswith((".png", ".jpeg", ".jpg", ".bmp", ".gif", ".tiff")):
        # 截取文件名的[:-12]部分
        new_filename = filename[:-11]
        
        # 构造完整的源文件路径和目标文件路径
        source_path = os.path.join(current_dir, filename)
        target_path = os.path.join(new_dir, new_filename)
        
        # 打开图片并转换为JPG格式
        try:
            with Image.open(source_path) as img:
                # 确保图片是RGB模式（避免保存时出错）
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 保存为JPG格式
                img.save(target_path, "JPEG")
            
            print(f"文件已处理并重命名：{filename} -> {new_filename}")
        except Exception as e:
            print(f"处理文件时出错：{filename}，错误信息：{e}")
