# -*- coding: utf-8 -*-
# tests/test_endpoint_lower_boundaries.py
import os, sys, unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import grpc
import distance_unary_pb2 as pb2
import distance_unary_pb2_grpc as pb2_grpc

HOST = "localhost:50051"  # cámbialo si tu server usa otro puerto

class TestEndpointLowerBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stub = pb2_grpc.DistanceServiceStub(grpc.insecure_channel(HOST))
        try:
            # ping rápido para saber si el server está arriba
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

    def test_latitude_below_min_returns_invalid(self):
        # frontera inferior: -90 - ε
        r = self.stub.geodesic_distance(
            pb2.SourceDest(
                source=pb2.Position(latitude=-90.0001, longitude=0.0),
                destination=pb2.Position(latitude=0.0, longitude=0.0),
                unit="km",
            )
        )
        self.assertEqual(r.unit, "invalid")
        self.assertEqual(r.distance, -1.0)

    def test_longitude_below_min_returns_invalid(self):
        # frontera inferior: -180 - ε
        r = self.stub.geodesic_distance(
            pb2.SourceDest(
                source=pb2.Position(latitude=0.0, longitude=-180.0001),
                destination=pb2.Position(latitude=0.0, longitude=0.0),
                unit="km",
            )
        )
        self.assertEqual(r.unit, "invalid")
        self.assertEqual(r.distance, -1.0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
