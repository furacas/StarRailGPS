import cv2

from star_rail_gps.utils.resources import resource_path

# 加载图像
img = cv2.imread(resource_path('test_data/screen_1920_1080.png'))
top_left = (11, 1024)
bottom_right = (152, 1061)

img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] = [0, 0, 0]

cv2.imwrite(resource_path('test_data/screen_1920_1080.png'), img)
