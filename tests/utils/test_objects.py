import unittest
from src.utils.objects import Vector, Transform
from utils.constants import *
from tests.utils.stubs.objects import Stub_Matrix3, Stub_Matrix4


class test_Vector3(unittest.TestCase):

    def setUp(self) -> None:
        self.v = Vector(1, 2, 3)
        self.u = Vector(3, 2, 1)
        self.w = Vector(5, 2, 3)
        self.up = Vector(0, 1, 0)
        self.zero = Vector(0, 0, 0)

        self.m = Stub_Matrix3()
        self.m.m = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


class test_vectorMath(test_Vector3):

    def test_mult_vectorVector(self):
        self.assertEqual((self.u * self.v).elements, [4.0, -8.0, 4.0])
        self.assertEqual((self.v * self.u).elements, [-4.0, 8.0, -4.0])
        self.assertEqual((self.v * self.w).elements, [0, 12, -8])
        self.assertEqual((Vector(0, 0, 0) * self.u).elements, [0.0, 0.0, 0.0])

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
                self.assertEqual(round(ls[i][j] / 4, EPISLON_LEN), res[i][j])

    def test_add_vectorVector(self):
        pass

    def test_add_vectorScalar(self):
        pass

    def test_sub_vectorVector(self):
        pass


class test_Vector4(unittest.TestCase):

    def setUp(self) -> None:
        self.v = Vector(1, 2, 3, 4)
        self.u = Vector(4, 3, 2, 1)
        self.w = Vector(5, 2, 3, 1)
        self.up = Vector(0, 1, 0, 0)
        self.zero = Vector(0, 0, 0, 0)

        self.m = Stub_Matrix4()
        self.m.m = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]


class test_vector_dunderMath(test_Vector4):

    def test_mult_vectorVector(self):
        self.assertEqual((self.u * self.v).elements, [4.0, -8.0, 4.0])
        self.assertEqual((self.v * self.u).elements, [-4.0, 8.0, -4.0])
        self.assertEqual((self.v * self.w).elements, [0, 12, -8])
        self.assertEqual((Vector(0, 0, 0) * self.u).elements, [0.0, 0.0, 0.0])

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
                self.assertEqual(round(ls[i][j] / 4, EPISLON_LEN), res[i][j])

    def test_add_vectorVector(self):
        pass

    def test_add_vectorScalar(self):
        pass

    def test_sub_vectorVector(self):
        pass


class test_Transform(unittest.TestCase):

    def setUp(self) -> None:
        self.transform = Transform()

    def test_get_set_position(self):
        self.assertEqual(self.transform.get_position(), [0, 0, 0])
        self.transform.set_position([1, 2, 3])
        self.assertEqual(self.transform.get_position(), [1, 2, 3])

    def test_get_set_scale(self):
        self.assertEqual(self.transform.get_scale(), [1, 1, 1])
        self.transform.set_scale([2, 2, 2])
        self.assertEqual(self.transform.get_scale(), [2, 2, 2])

    def test_get_set_rotation(self):
        self.assertEqual(self.transform.get_rotation(), [0, 0, 0])
        self.transform.set_rotation([0, 0, 0])
        self.assertEqual(self.transform.get_rotation(), [0, 0, 0])
        self.transform.set_rotation([2, 2, 2])
        self.assertEqual(self.transform.get_rotation(), [2, 2, 2])
        self.transform.set_rotation([45, 45, -45])
        self.assertEqual(self.transform.get_rotation(), [45, 45, -45])
        self.transform.set_rotation([90, 45, -45])
        self.assertEqual(self.transform.get_rotation(), [90, 45, -45])
        self.transform.set_rotation([90, 45, -45])
        self.assertEqual(self.transform.get_rotation(), [90, 45, -45])
        self.transform.set_rotation([90, 45, -90])
        self.assertEqual(self.transform.get_rotation(), [90, 45, -90])
        self.transform.set_rotation([90, 0, 45])
        self.assertEqual(self.transform.get_rotation(), [90, 0, 45])
        self.transform.set_rotation([90, 0, 90])
        self.assertEqual(self.transform.get_rotation(), [90, 0, 90])
        self.transform.set_rotation([90, 90, 90])
        self.assertEqual(self.transform.get_rotation(), [180, 90, 0])


