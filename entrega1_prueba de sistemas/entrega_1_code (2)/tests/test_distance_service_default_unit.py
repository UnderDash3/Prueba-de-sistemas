import os, sys, unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import grpc
from geopy.distance import geodesic
import distance_unary_pb2 as pb2
import distance_unary_pb2_grpc as pb2_grpc

HOST = "localhost:50051"  # cambia si usaste otro puerto

class TestDistanceServiceDefaultUnit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stub = pb2_grpc.DistanceServiceStub(grpc.insecure_channel(HOST))
        try:
            cls.stub.geodesic_distance(pb2.SourceDest(
                source=pb2.Position(latitude=0.0, longitude=0.0),
                destination=pb2.Position(latitude=0.0, longitude=0.1),
                unit="km"), timeout=1.0)
            cls.server_up = True
        except Exception:
            cls.server_up = False

    def setUp(self):
        if not self.server_up:
            self.skipTest(f"gRPC server no disponible en {HOST}")

    def test_default_unit_is_km_numerically(self):
        lat1, lon1 = -33.0351516, -70.5955963
        lat2, lon2 = -33.0348327, -71.5980458
        r = self.stub.geodesic_distance(pb2.SourceDest(
            source=pb2.Position(latitude=lat1, longitude=lon1),
            destination=pb2.Position(latitude=lat2, longitude=lon2),
            unit=""  # default
        ))
        expected_km = geodesic((lat1, lon1), (lat2, lon2)).km
        self.assertAlmostEqual(r.distance, expected_km, delta=0.05)
        self.assertEqual(r.unit, "km")

    def test_explicit_km_and_nm(self):
        msg = pb2.SourceDest(
            source=pb2.Position(latitude=-33.0, longitude=-70.0),
            destination=pb2.Position(latitude=-33.5, longitude=-70.5),
            unit="km",
        )
        r_km = self.stub.geodesic_distance(msg)
        msg.unit = "nm"
        r_nm = self.stub.geodesic_distance(msg)
        self.assertAlmostEqual(r_km.distance, r_nm.distance * 1.852, delta=0.1)

if __name__ == "__main__":
    unittest.main(verbosity=2)
