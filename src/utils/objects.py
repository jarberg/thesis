import math


class Vector:

    def __init__(self, *args):
        self.elements = []
        if len(args) != 0:
            if type(args[0]).__name__ == list.__name__:
                for i in range(0, len(args[0])):
                    self.elements.append(float(args[0][i]))
            else:
                for i in args:
                    self.elements.append(float(i))

    def __repr__(self):
        return self.elements

    def __neg__(self):
        for i in range(len(self)):
            self[i] = -self[i]
        return self

    def __str__(self):
        return str(self.elements)

    def __eq__(self, other):
        other_type = type(other).__name__
        if type(self).__name__ == other_type:
            if len(other) != len(self): return False

            for j in range(len(self)):
                if other[j] != self[j]: return False

            return True

        else:
            return False

    def __getitem__(self, item):
        return self.elements[item]

    def __setitem__(self, key, value):
        self.elements[key] = value

    def __len__(self):
        return len(self.elements)

    def __iter__(self):
        for i in range(len(self.elements)):
            yield self.elements[i]

    def __add__(self, other):
        result = []

        if type(self).__name__ == (type(other).__name__):
            if len(self) != len(other):
                raise Exception("Trying to add matrices of different dimensions")

            for i in range(len(self)):
                if len(self[i]) != len(other[i]):
                    raise Exception("Trying to add matrices of different dimensions")

                result.append([])
                for j in range(len(other)):
                    result[i].append(self[i][j] + other[i][j])

            return Matrix(result)
        else:
            raise Exception("Addition with matrix and object type {} is not supported".format(type(other).__name__))

    def __sub__(self, other):
        result = []

        if type(self).__name__ == (type(other).__name__):
            if len(self) != len(other):
                raise Exception("Trying to subtract vectors of different dimensions")

            for i in range(len(self)):
                result.append(self[i] - other[i])

            return Vector(result)

    def __mul__(self, other):
        result = []
        other_len = None
        other_type = type(other).__name__

        if type(self).__name__ == other_type:
            other_len = len(other)
            if len(self) == other_len:
                res = []
                res.append(self[1] * other[2] - self[2] * other[1])
                res.append(self[2] * other[0] - self[0] * other[2])
                res.append(self[0] * other[1] - self[1] * other[0])

                return Vector(res)
            else:
                raise Exception("Trying to multiply a matrix with a vector of different dimensions")

        elif other_type == Matrix.__name__:
            other_len = len(other)
            if len(self) != other_len:
                raise Exception("Trying to add matrices of different dimensions")
            for i in range(other_len):
                sum = 0.0
                for j in range(other_len):
                    sum += other[i][j] * self[j]
                result.append(sum)

            return Vector(result)

        elif other_type in [int.__name__ , float.__name__]:
            for i in range(len(self)):
                result.append(self[i] * other)

            return Vector(result)

        raise Exception("Trying to multiply a matrix with a illegal type: ".format(other_type))


    def __truediv__(self, other):
        result = []
        other_type = type(other).__name__
        if int.__name__ == other_type:
            for i in range(len(self)):
                result.append(self.elements[i] / other)
            return Vector(result)
        raise Exception("Trying to multiply a matrix with a illegal type: ".format(other.__name__))



class Matrix:

    def __init__(self, inputData = None, n = 4, m = None):
        self.m = []
        if inputData is not None and type(inputData) == list:
            for i in range(len(inputData)):
                self.m.append([])
                for j in range(len(inputData[i])):
                    self.m[i].append(inputData[i][j])
        else:
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
        other_type = type(other).__name__
        if type(self).__name__ == other_type:
            for i in range(len(self)):
                if len(other[i]) != len(self[i]): return False

                for j in range(len(self[i])):
                    if other[i][j] != self[i][j]: return False

        else:
            return False

    def __repr__(self):
        return "What ever you did, you ended up using represent on a Matrix"

    def __str__(self):
        t = " \n".join([str(x) for x in self.m])

        return t

    def __getitem__(self, item):
        return self.m[item]

    def __setitem__(self, key, value):
        self.m[key] = value

    def __len__(self):
        return len(self.m)

    def __iter__(self):
        for i, o in enumerate(self.m):
            for j, oo in enumerate(self.m[i]):
                yield self.m[i][j]

    def __add__(self, other):
        result = []

        if type(self).__name__ == (type(other).__name__):
            if len(self) != len(other):
                raise Exception("Trying to add matrices of different dimensions")

            for i in range(len(self)):
                if len(self[i]) != len(other[i]):
                    raise Exception("Trying to add matrices of different dimensions")

                result.append([])
                for j in range(len(other)):
                    result[i].append(self[i][j] + other[i][j])

            return Matrix(result)
        else:
            raise Exception("Addition with matrix and object type {} is not supported".format(type(other).__name__))

    def __sub__(self, other):
        result = []

        if type(self).__name__ == (type(other).__name__):
            if len(self) != len(other):
                print("Trying to add matrices of different dimensions")
                return self

            for i in range(len(self)):
                if len(self[i]) != len(other[i]):
                    print("Trying to add matrices of different dimensions")
                    return self

                result.append([])
                for j in range(len(other)):
                    result[i].append(self[i][j] - other[i][j])

            return Matrix(result)

    def __mul__(self, other):
        result = []

        other_type = type(other).__name__
        if type(self).__name__ == other_type:
            other_len = len(other)
            if len(self) != other_len:
                raise Exception("Trying to add matrices of different dimensions")

            for i in range(len(self)):
                if len(self[i]) != len(other[i]):
                    raise Exception("Trying to add matrices of different dimensions")

                result.append([])
                for j in range(other_len):
                    sum = 0.0
                    for k in range(len(self)):
                        sum+=self[i][k] * other[k][j]

                    result[i].append(sum)

            return Matrix(result)

        elif other_type in [int.__name__ , float.__name__]:
            for i in range(len(self)):
                result.append([])
                for j in range(len(self)):
                    result[i].append(self[i][j] * other)
            return Matrix(result)

        elif other_type in [Vector.__name__, list.__name__]:
            other_len = len(other)
            result = []
            if len(self) == other_len:
                for i in range(other_len):
                    sum = 0.0
                    for j in range(other_len):
                        sum += self[i][j] * other[j]
                    result.append(sum)

                return Vector(result)

            else:
                raise Exception("Trying to multiply a matrix with a vector of different dimensions")

        raise Exception("Trying to multiply a matrix with a illegal type: ".format(other.__name__))

    def __truediv__(self, other):
        result = []
        if int.__name__ == type(other).__name__:
            for i in range(len(self)):
                result.append([])
                for j in range(len(self)):
                    result[i].append(self[i][j] / other)
            return Matrix(result)

        raise Exception("Trying to multiply a matrix with a illegal type: ".format(other.__name__))


class Transform:

    def __init__(self, size=4):
        self.m = Matrix(n=size)

    def getTransform(self):
        return self.m

    def get_position(self):
        return [self.m[0][3],self.m[1][3],self.m[2][3]]

    def get_scale(self):
        sx = length([self.m[0][0], self.m[1][0], self.m[2][0]])
        sy = length([self.m[0][1], self.m[1][1], self.m[2][1]])
        sz = length([self.m[0][2], self.m[1][2], self.m[2][2]])

        print(sx, sy,sz)

    def get_rotation(self):
        sy = math.sqrt(self.m[0][0]*self.m[0][0] + self.m[1][0] * self.m[1][0])

        singular = sy < 1e-6

        if not singular:
            x = -math.atan2(self.m[2][1], self.m[2][2])
            y = -math.atan2(-self.m[2][0], sy)
            z = -math.atan2(self.m[1][0], self.m[0][0])

        else:
            x = math.atan2(-self.m[1][2], self.m[1][1])
            y = math.atan2(-self.m[2][0], sy)
            z = 0

        return [x, y, z]

class Model(Transform):
    pass


class Shader:
    pass


class ShadingGroup:

    def __init__(self, _shader: Shader):
        self.shader = _shader
        self.objList = []

    def register_obj(self, obj):
        self.objList.append(obj)

    def deregister_obj(self, obj):
        self.objList.remove(obj)


def length(v):
    xx = v[0] * v[0]
    yy = v[1] * v[1]
    zz = v[2] * v[2]

    return math.sqrt(xx + yy + zz)