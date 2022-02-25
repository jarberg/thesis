import math

from utils.objectUtils import Vector


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


class Stub_Matrix3:

    def __init__(self):
        self.m =[[1,0,0],
                 [0,1,0],
                 [0,0,1]]


    def __eq__(self, other):
        return False

    def __getitem__(self, item):
        return self.m[item]

    def __setitem__(self, key, value):
        self.m[key] = value

    def __len__(self):
        return len(self.m)

    def __iter__(self):
        for i in self.m:
            for j in i:
                yield j


class Stub_Vector3:
    pass


class Stub_Transform:

    def __init__(self):
        self.pos = [1,2,3]
        self.rot = [45,45,0]
        self.sca = [3,2,1]
        self.m = [[1.5000000000000004, -1.0000000000000002, 0.7071067811865476, 2.0],
                  [2.121320343559643, 1.4142135623730951, 0.0, 4.0],
                  [-1.5000000000000004, 1.0000000000000002, 0.7071067811865476, 6.0],
                  [0.0, 0.0, 0.0, 1.0]]

    def get_transform(self):
        return self.m

    def get_position(self):
        return self.pos

    def get_scale(self):
        return self.sca

    def get_rotation(self):
        return self.rot

    def set_scale(self, s: list):
        pass

    def _update_transform(self):
        pass

    def set_rotation(self, newRot: list or Vector):
        pass

    def set_position(self, newPos: list or Vector):
        pass




