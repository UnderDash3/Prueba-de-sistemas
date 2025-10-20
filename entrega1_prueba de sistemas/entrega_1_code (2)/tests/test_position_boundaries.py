
import os, sys, unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from geo_location import Position


EPS_IN  = 1e-4      
EPS_OUT = 1e-6       

class TestPositionBoundaries(unittest.TestCase):

    def test_latitude_exact_edges_are_valid(self):
        Position(-90.0, 0.0, 0.0)
        Position(+90.0, 0.0, 0.0)

    def test_latitude_just_inside_edges_are_valid(self):
        Position(-90.0 + EPS_IN, 0.0, 0.0)
        Position(+90.0 - EPS_IN, 0.0, 0.0)

    def test_latitude_below_min_raises(self):
        with self.assertRaises(ValueError):
            Position(-90.0 - EPS_OUT, 0.0, 0.0)

    def test_latitude_above_max_raises(self):
        with self.assertRaises(ValueError):
            Position(+90.0 + EPS_OUT, 0.0, 0.0)


    def test_longitude_exact_edges_are_valid(self):
        Position(0.0, -180.0, 0.0)
        Position(0.0, +180.0, 0.0)

    def test_longitude_just_inside_edges_are_valid(self):
        Position(0.0, -180.0 + EPS_IN, 0.0)
        Position(0.0, +180.0 - EPS_IN, 0.0)

    def test_longitude_below_min_raises(self):
        with self.assertRaises(ValueError):
            Position(0.0, -180.0 - EPS_OUT, 0.0)

    def test_longitude_above_max_raises(self):
        with self.assertRaises(ValueError):
            Position(0.0, +180.0 + EPS_OUT, 0.0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
