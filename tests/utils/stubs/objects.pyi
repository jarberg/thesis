import unittest
from src.utils.objects import *

class Stub_Matrix4:

    def __init__(self, n = 4, m = None):
        self.m =[]

        for i in range(n):
            self.m.append([])
            if m is None:
                m = n
            for j in range(m):
                if i == j:
                    self.m[i].append(1)
                else:
                    self.m[i].append(0)

    def __eq__(self, other):
        return False

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def __getitem__(self, item):
        return self.m[item]

    def __setitem__(self, key, value):
        super().__setitem__(key, value)

    def __len__(self):
        return super().__len__()

    def __iter__(self):
        return super().__iter__()

    def __add__(self, other):
        return super().__add__(other)

    def __sub__(self, other):
        return super().__sub__(other)

    def __mul__(self, other):
        return super().__mul__(other)

    def __truediv__(self, other):
        return super().__truediv__(other)





