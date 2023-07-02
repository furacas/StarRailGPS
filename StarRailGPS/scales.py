# -*- coding: utf-8 -*-
import cv2
import numpy as np

from StarRailGPS.gps import get_mask_from_gray_map, get_mask_from_rgb_min_map
from StarRailGPS.utils.resources import resource_path

img = cv2.imread(resource_path('maps/50.png'), cv2.IMREAD_UNCHANGED)
img = get_mask_from_gray_map(img)

screen = cv2.imread(resource_path('test_data/screen_1920_1080_1.png'))
# screen = cv2.imread(resource_path('test_data/screen_1920_1080_run.png'))
minimap_rect = [77, 88, 127, 127]  # (x, y, width, height)
template = screen[minimap_rect[1]:minimap_rect[1] + minimap_rect[3], minimap_rect[0]:minimap_rect[0] + minimap_rect[2]]
template = get_mask_from_rgb_min_map(template)

h, w = template.shape[::]
# 创建尺度的列表
scales = np.linspace(0.8, 0.9, 100)
# scales = np.linspace(0.8, 1.2, 200)

# 对每个尺度进行模板匹配
best_match = None
best_score = -np.inf
max_scale = None
for scale in scales:
    # 调整模板的大小
    resized_template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    h, w = resized_template.shape[::-1]

    # 进行模板匹配
    res = cv2.matchTemplate(img, resized_template, cv2.TM_CCORR_NORMED)

    # 找到最好的匹配
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val > best_score:
        best_score = max_val
        best_match = max_loc, (max_loc[0] + w, max_loc[1] + h)
        max_scale = scale

print(max_scale, best_score)

# 0.82
# 1.03
