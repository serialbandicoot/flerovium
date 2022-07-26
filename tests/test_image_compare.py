from http.client import OK
from re import A
import unittest
from src.image_compare import ImageCompare, MatchType
import os


class TestImageCompare(unittest.TestCase):
    
    def setUp(self):
        self.about_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "data",
            "images",
            "about.png",
        )
    
    def test_image_compare_bad(self):
        about2_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "data",
            "images",
            "bad_about.png",
        )
        ic = ImageCompare(self.about_path, about2_path)
        res = ic.match()
        assert res == MatchType.BAD

    def test_image_compare_good(self):
        about2_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "data",
            "images",
            "good_about.png",
        )
        ic = ImageCompare(self.about_path, about2_path)
        res = ic.match()
        assert res == MatchType.GOOD

    def test_image_compare_ok(self):
        about2_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "data",
            "images",
            "perfect_about.png",
        )
        ic = ImageCompare(self.about_path, about2_path)
        res = ic.match()
        assert res == MatchType.PERFECT
