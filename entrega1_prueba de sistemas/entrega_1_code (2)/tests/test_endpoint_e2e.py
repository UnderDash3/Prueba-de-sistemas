
import os, sys, unittest, math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import grpc
from geopy.distance import geodesic
import distance_unary_pb2 as pb2
import distance_unary_pb2_grpc as pb2_grpc

HOST = "localhost:50051"

class TestEndpointE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stub = pb2_grpc.DistanceServiceStub(grpc.insecure_channel(HOST))
        try:
            cls.stub.geodesic_distance(
                pb2.SourceDest(
                    source=pb2.Position(latitude=0.0, longitude=0.0),
                    destination=pb2.Position(latitude=0.0, longitude=0.1),
                    unit="km",
                ),
                timeout=1.0,
            )
            cls.server_up = True
        except Exception:
            cls.server_up = False

    def setUp(self):
        if not self.server_up:
            self.skipTest(f"gRPC server no disponible en {HOST}")

    def test_same_point_is_zero(self):
        p = pb2.Position(latitude=-12.3456, longitude=+23.4567)
        r = self.stub.geodesic_distance(pb2.SourceDest(source=p, destination=p, unit="km"))
        self.assertEqual(r.unit, "km")
        self.assertTrue(math.isclose(r.distance, 0.0, abs_tol=1e-9))

    def test_cross_180_meridian_against_geopy(self):
       
        p1 = pb2.Position(latitude=+10.0, longitude=+179.9999)
        p2 = pb2.Position(latitude=+10.0, longitude=-179.9999)
        r = self.stub.geodesic_distance(pb2.SourceDest(source=p1, destination=p2, unit="km"))
        expected = geodesic((p1.latitude, p1.longitude), (p2.latitude, p2.longitude)).km
        self.assertAlmostEqual(r.distance, expected, delta=0.05)
        self.assertEqual(r.unit, "km")

    def test_almost_antipodal_against_geopy(self):
    
        p1 = pb2.Position(latitude=-22.2222, longitude=+44.4444)
        p2 = pb2.Position(latitude=+22.2222, longitude=-(44.4444 - 179.9999)) 
        r = self.stub.geodesic_distance(pb2.SourceDest(source=p1, destination=p2, unit="km"))
        expected = geodesic((p1.latitude, p1.longitude), (p2.latitude, p2.longitude)).km
        self.assertAlmostEqual(r.distance, expected, delta=0.05)
        self.assertEqual(r.unit, "km")

    def test_consistency_km_vs_nm(self):
        src = pb2.Position(latitude=-12.3456, longitude=+23.4567)
        dst = pb2.Position(latitude=-12.345599, longitude=+23.4567)
        r_km = self.stub.geodesic_distance(pb2.SourceDest(source=src, destination=dst, unit="km"))
        r_nm = self.stub.geodesic_distance(pb2.SourceDest(source=src, destination=dst, unit="nm"))
        self.assertAlmostEqual(r_km.distance, r_nm.distance * 1.852, delta=0.05)
        self.assertEqual(r_km.unit, "km")
        self.assertEqual(r_nm.unit, "nm")

if __name__ == "__main__":
    unittest.main(verbosity=2)

