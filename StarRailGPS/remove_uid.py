import cv2

from StarRailGPS.utils.resources import resource_path


def remove(path):
    # 加载图像
    img = cv2.imread(path)
    top_left = (11, 1024)
    bottom_right = (152, 1061)

    img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] = [0, 0, 0]

    cv2.imwrite(path, img)


remove(resource_path('test_data/screen_1920_1080.png'))
remove(resource_path('test_data/screen_1920_1080_1.png'))
remove(resource_path('test_data/screen_1920_1080_run.png'))
