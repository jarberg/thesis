import unittest
from utils.objectUtils import *
from utils.objects import *
from tests.utils.stubs import *


EPSILON = 0.000001
EPISLON_LEN = abs(decimal.Decimal(str(EPSILON)).as_tuple().exponent)

class test_Vector3(unittest.TestCase):

    def setUp(self) -> None:
        self.v = [1,2,3]
        self.u = [3,2,1]
        self.w = [5,2,3]
        self.up = [0,1,0]
        self.zero = [0,0,0]

        self.m = [[1,0,0],[0,1,0],[0,0,1]]

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
            self.assertEqual(round(vlength(ls[i]), EPISLON_LEN), res[i])


    def test_dot(self):
        res = [10.0, 10.0, 38.0, 2.0, 2.0, 38.0, 1]
        ls = [self.v, self.u, self.w, self.u, self.up,self.w]

        for i in range(len(ls)):
            u = ls[i]
            v = ls[1+-i]
            self.assertEqual(dot(u, v), res[i])

