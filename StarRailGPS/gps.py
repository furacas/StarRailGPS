import json
from typing import Dict, Any

import cv2 as cv
import numpy as np

from StarRailGPS.utils.resources import resource_path

SCALE = 0.82
RUNNING_SCALE = 1.03
minimap_coordinate = (77, 88, 127, 127)
arrow_coordinate = (117, 128, 47, 47)

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


def position(screen, options: Dict[str, Any] = None) -> Dict[str, Any]:
    if options is None:
        options = {}

    map_name = options.get('map_name')

    # template
    min_map = crop_image(screen, minimap_coordinate)
    template = get_mask_from_rgb_min_map(min_map)

    scale = options.get('scale', None)

    if not scale:
        is_running = options.get('is_running', False)
        if is_running:
            scale = RUNNING_SCALE
        else:
            scale = SCALE

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

    result = {'position': (int(x), int(y))}
    if options.get('return_match_quality', False):
        result['match_quality'] = max_val
    return result


def calculate_direction(screen) -> int:
    target_color = np.array([234, 191, 4])
    arrow = cv.imread(resource_path("imgs/arrow.jpg"))
    cropped_image = crop_image(screen, arrow_coordinate)
    cropped_image[np.sum(np.abs(cropped_image - target_color), axis=-1) <= 50] = target_color
    cropped_image[np.sum(np.abs(cropped_image - target_color), axis=-1) > 0] = [0, 0, 0]
    max_corr_value = 0
    best_match_angle = 0
    for i in range(0, 360, 30):
        rotated_image = rotate_image(arrow, -i)
        result = cv.matchTemplate(cropped_image, rotated_image, cv.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if max_val > max_corr_value:
            max_corr_value = max_val
            max_loc = (max_loc[0] + 12, max_loc[1] + 12)
            best_match_angle = i

    for offset in range(-30, 30, 6):
        i = (best_match_angle + offset) % 360
        rotated_image = rotate_image(arrow, -i)
        result = cv.matchTemplate(cropped_image, rotated_image, cv.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if max_val > max_corr_value:
            max_corr_value = max_val
            max_loc = (max_loc[0] + 12, max_loc[1] + 12)
            best_match_angle = i

    for offset in range(-6, 6, 1):
        i = (best_match_angle + offset) % 360
        rotated_image = rotate_image(arrow, -i)
        result = cv.matchTemplate(cropped_image, rotated_image, cv.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if max_val > max_corr_value:
            max_corr_value = max_val
            max_loc = (max_loc[0] + 12, max_loc[1] + 12)
            best_match_angle = i
    best_match_angle = (best_match_angle - 90) % 360

    return best_match_angle


def crop_image(image, crop_region):
    left, top, width, height = crop_region
    return image[top: top + height, left: left + width]


def rotate_image(src, rotation_angle=0):
    height, width, channels = src.shape
    rotation_matrix = compute_rotation_matrix(width // 2, height // 2, rotation_angle)
    rotated_img = cv.warpAffine(src, rotation_matrix, (width, height))
    return rotated_img


def compute_rotation_matrix(x, y, rotation_angle):
    cos_val = np.cos(np.deg2rad(rotation_angle))
    sin_val = np.sin(np.deg2rad(rotation_angle))
    return np.float32(
        [
            [cos_val, sin_val, x * (1 - cos_val) - y * sin_val],
            [-sin_val, cos_val, x * sin_val + y * (1 - cos_val)],
        ]
    )
