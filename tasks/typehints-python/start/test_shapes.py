import math
import unittest

from shapes import area_circle, area_rect, describe, perimeter_rect, scale


class Shapes(unittest.TestCase):
    def test_circle(self):
        self.assertAlmostEqual(area_circle(1), math.pi)

    def test_rect(self):
        self.assertEqual(area_rect(2, 3), 6)
        self.assertEqual(perimeter_rect(2, 3), 10)

    def test_scale(self):
        self.assertEqual(scale([(1, 2), (3, 4)], 2), [(2, 4), (6, 8)])

    def test_describe(self):
        self.assertEqual(describe("disc", math.pi), "disc: 3.14")


if __name__ == "__main__":
    unittest.main()
