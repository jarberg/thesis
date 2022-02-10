import unittest
from utils.objectUtils import *
from utils.objects import *


EPSILON = 0.000001
EPISLON_LEN = abs(decimal.Decimal(str(EPSILON)).as_tuple().exponent)


class test_Vector3(unittest.TestCase):

    def setUp(self) -> None:
        self.v = Vector(1,2,3)
        self.u = Vector(3,2,1)
        self.w = Vector(5,2,3)
        self.up = Vector(0,1,0)
        self.zero = Vector(0,0,0)

        self.m = Matrix([[1,0,0],[0,1,0],[0,0,1]])

class test_vectorMath(test_Vector3):

    def test_normalize(self):
        self.n = normalize(self.v)
        res = [0.267261, 0.534522, 0.801784]
        for i in range(len(self.n)):
            self.assertEqual(round(self.n[i], EPISLON_LEN), res[i])

    def test_length(self):
        res = [3.741657, 3.741657, 6.164414, 1.0]
        ls = [self.v, self.u, self.w, self.up]
        for i in range(len(ls)):
            self.assertEqual(round(length(ls[i]), EPISLON_LEN), res[i])

    def test_dot(self):
        pass

    def test_mult_vectorVector(self):
        self.assertEqual((self.u * self.v).elements, [4.0, -8.0, 4.0])
        self.assertEqual((self.v * self.u).elements, [-4.0, 8.0, -4.0])
        self.assertEqual((self.v * self.w).elements, [0, 12, -8])
        self.assertEqual((Vector(0,0,0)*self.u).elements, [0.0, 0.0, 0.0])

    def test_mult_vectorMatrix(self):
        self.assertEqual((self.u * self.m).elements, [3.0, 2.0, 1.0])
        self.assertEqual((self.v * self.m).elements, [1.0, 2.0, 3.0])
        self.assertEqual((self.w * self.m).elements, [5.0, 2.0, 3.0])
        self.assertEqual((Vector(0, 0, 0) * self.m).elements, [0.0, 0.0, 0.0])

    def test_mult_vectorScalar(self):
        self.assertEqual((self.u * 3).elements, [9.0, 6.0, 3.0])
        self.assertEqual((self.v * 5).elements, [5.0, 10.0, 15.0])
        self.assertEqual((self.w * 4).elements, [20.0, 8.0, 12.0])
        self.assertEqual((self.w * 0).elements, [0, 0, 0])

    def test_div_vectorScalar(self):
        ls = [self.v, self.u, self.w]
        res = [[round(0.25, EPISLON_LEN), round(0.5, EPISLON_LEN), round(0.75, EPISLON_LEN)],
               [round(0.75, EPISLON_LEN), round(0.5, EPISLON_LEN), round(0.25, EPISLON_LEN)],
               [round(1.25, EPISLON_LEN), round(0.5, EPISLON_LEN), round(0.75, EPISLON_LEN)]
               ]

        for i in range(len(ls)):
            for j in range(len(ls[i])):
                self.assertEqual(round(ls[i][j]/4, EPISLON_LEN), res[i][j])

    def test_add_vectorVector(self):
        pass

    def test_add_vectorScalar(self):
        pass

    def test_sub_vectorVector(self):
        pass

