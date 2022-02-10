import unittest


class TestVector1(unittest.TestCase):
    def setUp(self):
        self.v = Vector(1)


class TestInit(TestVector1):
    def test_length(self):
        self.assertEqual(len(self.v), 1)









