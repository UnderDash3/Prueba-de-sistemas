import os, sys, unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from geo_location import Position

class TestPositionBoundaries(unittest.TestCase):
    def test_latitude_below_min_raises_value_error(self):
        with self.assertRaises(ValueError):
            Position(-90.0001, 0.0, 0.0)

    def test_longitude_below_min_raises_value_error(self):
        with self.assertRaises(ValueError):
            Position(0.0, -180.0001, 0.0)

    def test_latitude_above_max_raises_value_error(self):
        with self.assertRaises(ValueError):
            Position(90.0001, 0.0, 0.0)

    def test_longitude_above_max_raises_value_error(self):
        with self.assertRaises(ValueError):
            Position(0.0, 180.0001, 0.0)

    def test_boundary_values_are_valid(self):
        Position(-90.0, -180.0, 0.0)
        Position(90.0, 180.0, 0.0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
