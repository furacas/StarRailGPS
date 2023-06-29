import unittest

from StarRailGPS.gps import calculate_direction
from StarRailGPS.utils.resources import resource_path
import cv2 as cv


class TestGPS(unittest.TestCase):
    def test_get_direction(self):
        im = cv.imread(resource_path('test_data/screen_1920_1080_1.png'))
        d = calculate_direction(im)
        print(d)


if __name__ == '__main__':
    unittest.main()
