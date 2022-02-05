from math import sqrt
from utils.objectUtils import *
from numpy import float32 as f32

class Transform:

    def __init__(self):
        pass

class Vector:

    def __init__(self, *args):
        self.elements = []

        if type(args[0]).__name__ == list.__name__:
            for i in range(0, len(args[0])):
                self.elements.append(args[0][i])
        else:
            for i in args:
                self.elements.append(i)


    def __repr__(self):
        return "What ever you did, you ended up using represent on a Vector"

    def __str__(self):
        return str(self.elements)

    def __eq__(self, other):
        other_type = type(other).__name__
        if type(self).__name__ == other_type:
            if len(other) != len(self): return False

            for j in range(len(self)):
                if other[j] != self[j]: return False

        else: return False

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
                return self

            for i in range(len(self)):
                if len(self[i]) != len(other[i]):
                    raise Exception("Trying to add matrices of different dimensions")
                    return self

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
                result[i].append(self[i] - other[i])

            return Vector(result)

    def __mul__(self, other):
        result = []
        other_len = None
        other_type = type(other).__name__

        if type(self).__name__ == other_type:
            other_len = len(other)
            if len(self) == other_len:
                for i in range(other_len):
                    result.append(self[i] * other[i])

                return Vector(result)
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

        elif int.__name__ == other_type:
            for i in range(len(self)):
                result.append(self[i] * other)

            return Vector(result)

        raise Exception("Trying to multiply a matrix with a illegal type: ".format(other_type))


    def __truediv__(self, other):
        result = []
        if int.__name__ == type(other).__name__:
            for i in range(len(self)):
                result[i].append(self[i] / other)
            return Vector(result)

        raise Exception("Trying to multiply a matrix with a illegal type: ".format(other.__name__))

class Matrix:

    def __init__(self, input = None, n = 1, m = None):
        self.m = []
        if input is not None and type(input) == list:
            for i in range(len(input)):
                self.m.append([])
                for j in range(len(input[i])):
                    if len(input) != len(input[i]):
                        print("Trying to create matrix with different row/colomns")
                    self.m[i].append(input[i][j])
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
        return str(self.m)

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
                return self

            for i in range(len(self)):
                if len(self[i]) != len(other[i]):
                    raise Exception("Trying to add matrices of different dimensions")
                    return self

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
        other_len = len(other)
        other_type = type(other).__name__
        if type(self).__name__ == other_type:
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

        elif int.__name__ == other_type:
            for i in range(len(self)):
                result.append([])
                for j in range(len(self)):
                    result[i].append(self[i][j] * other)
            return Matrix(result)

        elif other_type in [Vector.__name__, list.__name__]:
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



def flatten(obj):
    return [ x for x in obj]


def transpose(obj):
    result = []
    for i in range(len(obj)):
        result.append([])
        for j in range(len(obj[i])):
            result[i].append(obj.m[j][i])

    return Matrix(result)


def det(m):
     if (type(m).__name__) != Matrix.__name__: \
         raise Exception("Cant find determinant on a non Matrix")
     if len(m) == 2:
         return det2(m)
     if len(m) == 3:
         return det3(m)
     if len(m) == 4:
         return det4(m)


def inverse(m):
    n = len(m)
    a = Matrix(n= n, m =2*n)

    for i in range(n):
        for j in range(n):
            a[i][j] = m[i][j]

    set_identity(a, n)
    gaus_jordan(a, n)
    row_operations_principal_diagonal(a, n)

    im = Matrix(n = n)
    for i in range(n):
        for j in range(n):
            im[i][j] = a[i][j+n]

    return im


def normalMatrix(matrix, as_lower_order = False):

    a = inverse(transpose(matrix))
    if not as_lower_order: return a
    else:
        l = len(a)
        b = Matrix(n=l-1)
        for i in range(l-1):
            for j in range(l-1):
                b[i][j] = a[i][j]
        return b


def sizeOf(input):
    inputType = type(input).__name__
    if inputType not in [Matrix.__name__, Vector.__name__]:
        raise Exception("attempted to sizeOf of unsupported datastructure")

    inputSize = len(input)
    retdict = {
            Matrix.__name__: 4*inputSize*inputSize,
            Vector.__name__: 4*inputSize
           }
    ret = retdict.get(inputType)
    if inputType not in [Matrix.__name__, Vector.__name__]:
        raise Exception("attempted to sizeOf of unsupported datastructure2")
    return ret

t = Vector([1,2])

print(sizeOf(t))
