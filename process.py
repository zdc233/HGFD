import os
import shutil
from pathlib import Path

src_dir   = Path('../output')
root_dst  = Path('./data/HGLane')
categories = {'snow', 'rain', 'fog', 'night', 'dusk'}

for old_path in src_dir.glob('*.png'):
    # 去掉后缀 '_00001_.png'，得到新文件名
    new_name = old_path.name.replace('_00001_.png', '')
    category = new_name.split('_')[0]          # 取前缀如dusk、rain...
    if category not in categories:
        continue                               # 忽略未知类别
    new_path = root_dst / category / new_name
    shutil.move(str(old_path), str(new_path))   # 移动（相当于重命名+移动）

print('Done.')
