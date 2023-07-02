import unittest

from StarRailGPS.gps import calculate_direction, position
from StarRailGPS.utils.resources import resource_path
import cv2 as cv


class TestGPS(unittest.TestCase):
    def test_get_direction(self):
        im = cv.imread(resource_path('test_data/screen_1920_1080_1.png'))
        d = calculate_direction(im)
        print(d)

    def test_position_normal(self):
        im = cv.imread(resource_path('test_data/screen_1920_1080_1.png'))
        options = {'map_name': '城郊雪原'}
        pos = position(im, options)

        print(pos)

    def test_position_running(self):
        im = cv.imread(resource_path('test_data/screen_1920_1080_run.png'))
        options = {'map_name': '城郊雪原'}
        pos = position(im, options)
        print(pos)
        options['is_running'] = True
        pos = position(im, options)
        print(pos)


if __name__ == '__main__':
    unittest.main()
