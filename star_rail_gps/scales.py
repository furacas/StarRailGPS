# -*- coding: utf-8 -*-
import cv2
import numpy as np

from star_rail_gps.utils.resources import resource_path


def get_mask_from_rgb(img_r):
    img_hsv = cv2.cvtColor(img_r, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(img_hsv)
    # 筛选白色 H S<10  V 60~90%
    mask1 = (s < 25) * (v > 255 * 0.6) * (v < 255 * 0.9)
    # 筛选蓝色摄像头扫过的白色
    mask2 = (95 < h) * (h < 105) * (0 < s) * (s < 50) * (200 < v) * (v < 240)
    mask = mask1 | mask2
    img_mask = mask.astype(np.uint8) * 255
    return img_mask


def get_mask_from_gray_image(map_bgra):
    b, g, r, a = cv2.split(map_bgra)
    gray = b
    mask = (a > 250) & (gray > 80)
    return mask.astype(np.uint8) * 255


img = cv2.imread(resource_path('maps/50.png'), cv2.IMREAD_UNCHANGED)
img = get_mask_from_gray_image(img)

screen = cv2.imread(resource_path('test_data/screen_1920_1080.png'))
minimap_rect = [77, 88, 127, 127]  # (x, y, width, height)
template = screen[minimap_rect[1]:minimap_rect[1] + minimap_rect[3], minimap_rect[0]:minimap_rect[0] + minimap_rect[2]]
template = get_mask_from_rgb(template)

h, w = template.shape[::]
# 创建尺度的列表
scales = np.linspace(0.8, 0.9, 100)

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
