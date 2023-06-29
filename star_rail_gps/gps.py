import json
from typing import Tuple

import cv2 as cv
import numpy as np

from star_rail_gps.utils.resources import resource_path

scale = 0.82
minimap_rect = [77, 88, 127, 127]

with open(resource_path('maps/name_id.json'), 'r', encoding='utf-8') as f:
    name_id_map = json.load(f)


def get_mask_from_gray_map(bgra_img):
    b, g, r, a = cv.split(bgra_img)
    gray = b
    mask = (a > 250) & (gray > 80)
    return mask.astype(np.uint8) * 255


def get_mask_from_rgb_min_map(rgb_img):
    img_hsv = cv.cvtColor(rgb_img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(img_hsv)
    # 筛选白色 H S<10  V 60~90%
    mask1 = (s < 25) * (v > 255 * 0.6) * (v < 255 * 0.9)
    # 筛选蓝色摄像头扫过的白色
    mask2 = (95 < h) * (h < 105) * (0 < s) * (s < 50) * (200 < v) * (v < 240)
    mask = mask1 | mask2
    img_mask = mask.astype(np.uint8) * 255
    return img_mask


def position(screen, map_name=None) -> Tuple[int, int]:
    # template
    min_map = screen[minimap_rect[1]:minimap_rect[1] + minimap_rect[3],
              minimap_rect[0]:minimap_rect[0] + minimap_rect[2]]
    template = get_mask_from_rgb_min_map(min_map)

    # 调整模板的大小到最佳匹配大小
    resized_template = cv.resize(template, None, fx=scale, fy=scale, interpolation=cv.INTER_AREA)

    # map
    map_id = name_id_map[map_name]
    map_gry = cv.imread(resource_path('maps/{}.png'.format(map_id)), cv.IMREAD_UNCHANGED)
    map = get_mask_from_gray_map(map_gry)

    # 进行模板匹配
    res = cv.matchTemplate(map, resized_template, cv.TM_CCORR_NORMED)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    h, w = resized_template.shape[:2]
    x, y = max_loc[0] + w / 2, max_loc[1] + h / 2
    return int(x), int(y)
