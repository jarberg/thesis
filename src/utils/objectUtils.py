import math
from typing import Union

from constants import PI, EPISLON_LEN


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
                raise Exception("Trying to add vectors of different dimensions")

            for i in range(len(self)):
                result.append(self[i] + other[i])

            return Vector(result)
        elif type(other).__name__ == list.__name__:

            for i in range(len(self)):
                if len(self) != len(other):
                    raise Exception("Trying to add vectors of different dimensions")
                result.append(self[i] + other[i])

            return Vector(result)
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

        elif "Matrix" in other_type:
            other_len = len(other)
            if len(self) != other_len:
                raise Exception("Trying to add matrices of different dimensions")
            for i in range(other_len):
                sum = 0.0
                for j in range(other_len):
                    sum += other[i][j] * self[j]
                result.append(sum)

            return Vector(result)

        elif other_type in [int.__name__, float.__name__]:
            for i in range(len(self)):
                result.append(self[i] * other)

            return Vector(result)

        raise Exception("Trying to multiply a matrix with a illegal type: ".format(other_type))

    def __truediv__(self, other):
        result = []
        other_type = type(other).__name__
        if other_type in [int.__name__, float.__name__]:
            for i in range(len(self)):
                result.append(self.elements[i] / other)
            return Vector(result)
        raise Exception("Trying to multiply a Vector with a illegal type: ".format(other.__name__))


class Matrix:

    def __init__(self, inputData=None, n=4, m=None):
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
                        self.m[i].append(1.0)
                    else:
                        self.m[i].append(0.0)

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
        if other_type in [type(self).__name__, "Transform"]:
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
                        sum += self[i][k] * other[k][j]

                    result[i].append(sum)

            return Matrix(result)

        elif other_type in [int.__name__, float.__name__]:
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

        raise Exception("Trying to multiply a matrix with a illegal type: {}".format(type(other).__name__))

    def __truediv__(self, other):
        result = []
        if int.__name__ == type(other).__name__:
            for i in range(len(self)):
                result.append([])
                for j in range(len(self)):
                    result[i].append(self[i][j] / other)
            return Matrix(result)

        raise Exception("Trying to multiply a matrix with a illegal type: ".format(type(other).__name__))


class Quaternion:

    def __init__(self, quats=None, euler=None, matrix=None):
        if euler:
            self.i, self.j, self.k, self.w = euler_to_quaternion(euler)
        elif matrix:
            self.i, self.j, self.k, self.w = matrix_to_quaternion(matrix)
        elif quats:

            self.i = quats[0]
            self.j = quats[1]
            self.k = quats[2]
            self.w = quats[3]
            d = normalize_q(self)
            if d == 0:
                d = 1
            self.i /= d
            self.j /= d
            self.k /= d
            self.w /= d
        else:
            self.i, self.j, self.k, self.w = (0, 0, 0, 1)

    def __len__(self):
        return 4

    def __getitem__(self, item):
        return [self.i, self.j, self.k, self.w][item]

    def __setitem__(self, key, value):
        [self.i, self.j, self.k, self.w][key] = value

    def __str__(self):
        return str([self.i, self.j, self.k, self.w])

    def __add__(self, other):
        result = []
        if type(self).__name__ in [list.__name__, type(other).__name__]:
            if len(self) != len(other):
                raise Exception("Trying to add Quaternion of different dimensions")

            for i in range(len(self)):
                result.append(self[i] + other[i])

            return Quaternion(result)
        else:
            raise Exception("Addition with Quaternion and object type {} is not supported".format(type(other).__name__))

    def __mul__(self, other):
        other_type = type(other).__name__
        if type(self).__name__ == other_type:
            ret = Quaternion()
            ret.w = self.w * other.w - self.i * other.i - self.j * other.j - self.k * other.k  # 1
            ret.i = self.w * other.i + self.i * other.w + self.j * other.k - self.k * other.j  # i
            ret.j = self.w * other.j - self.i * other.k + self.j * other.w + self.k * other.i  # j
            ret.k = self.w * other.k + self.i * other.j - self.j * other.i + self.k * other.w  # k
            return ret
        elif other_type in [int.__name__, float.__name__]:
            ret = Quaternion()
            ret.w = self.w*other
            ret.i = self.i*other
            ret.j = self.j*other
            ret.k = self.k*other
            return ret
        else:
            raise Exception("Somethign whent wrong".format(type(other).__name__))

    def __truediv__(self, other):
        other_type = type(other).__name__
        if other_type in [float.__name__, int.__name__]:
            if other == 0:
                other = 1
            self.w /= other
            self.i /= other
            self.j /= other
            self.k /= other
        return self

    def __iter__(self):
        for i in [self.i, self.j, self.k, self.w]:
            yield i


def length(v):
    xx = v[0] * v[0]
    yy = v[1] * v[1]
    zz = v[2] * v[2]

    return math.sqrt(xx + yy + zz)


def sub(v1, v2):
    res = []
    for i in range(len(v1)):
        res.append(v1[i] - v2[i])
    return res


def div(vec, flo):
    res = []
    for i in range(len(vec)):
        res.append(vec[i] / flo)
    return res


def cross(v1, v2):
    if len(v1) == len(v2):
        res = []
        res.append(v1[1] * v2[2] - v1[2] * v2[1])
        res.append(v1[2] * v2[0] - v1[0] * v2[2])
        res.append(v1[0] * v2[1] - v1[1] * v2[0])

        return Vector(res)


def det2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def det3(m):
    d = m[0][0] * m[1][1] * m[2][2] + \
        m[0][1] * m[1][2] * m[2][0] + \
        m[0][2] * m[2][1] * m[1][0] - \
        m[2][0] * m[1][1] * m[0][2] - \
        m[1][0] * m[0][1] * m[2][2] - \
        m[0][0] * m[1][2] * m[2][1]
    return d


def det4(m):
    m0 = [
        [m[1][1], m[1][2], m[1][3]],
        [m[2][1], m[2][2], m[2][3]],
        [m[3][1], m[3][2], m[3][3]]
    ]
    m1 = [
        [m[1][0], m[1][2], m[1][3]],
        [m[2][0], m[2][2], m[2][3]],
        [m[3][0], m[3][2], m[3][3]]
    ]
    m2 = [
        [m[1][0], m[1][1], m[1][3]],
        [m[2][0], m[2][1], m[2][3]],
        [m[3][0], m[3][1], m[3][3]]
    ]
    m3 = [
        [m[1][0], m[1][1], m[1][2]],
        [m[2][0], m[2][1], m[2][2]],
        [m[3][0], m[3][1], m[3][2]]
    ]
    return m[0][0] * det3(m0) - m[0][1] * det3(m1) + m[0][2] * det3(m2) - m[0][3] * det3(m3)


def set_identity(m, n):
    for i in range(0, n):
        for j in range(0, n):
            if i == j:
                m[i][j + n] = 1
            else:
                m[i][j + n] = 0


def gaus_jordan(m, size):
    for i in range(0, size):
        if m[i][i] == 0:
            raise Exception("MATHMATILCAL ERROR")
        for j in range(0, size):
            if i != j:
                ratio = m[j][i] / m[i][i]
                for k in range(2 * size):
                    m[j][k] = m[j][k] - ratio * m[i][k]


def row_operations_principal_diagonal(m, size):
    for i in range(0, size):
        for j in range(size, 2 * size):
            m[i][j] = m[i][j] / m[i][i]


import numpy

def flatten_list(list_obj, transposes=True, data_type=numpy.float32):
    res = []
    for obj in list_obj:
        if Matrix.__name__ == type(obj).__name__ and transposes:
            ret = transpose(obj)
            for each in ret:
                res.append(each)
        else:
            ret = obj

    return numpy.array(res, dtype=data_type)

def flatten(obj, transposes=True, data_type=numpy.float32):
    ret = []
    if Matrix.__name__ == type(obj).__name__ and transposes:
        ret = transpose(obj)
    elif(list.__name__ == type(obj).__name__):
        if list.__name__ == type(obj[0]).__name__:
            for each in obj:
                for j in each:
                    ret.append(j)
        else:
            ret = obj
    else:
        ret = obj


    return numpy.array(ret, dtype=data_type)


def radians(degrees):
    return (degrees / 180.0) * PI


def degrees(radians):
    return round(radians / PI * 180, EPISLON_LEN)


def transpose(m: Matrix):
    result = []
    for i in range(len(m)):
        result.append([])
        for j in range(len(m[i])):
            result[i].append(m.m[j][i])

    return Matrix(result)


def det(m: Matrix):
    if type(m).__name__ != Matrix.__name__:
        raise Exception("Cant find determinant on a non Matrix")
    if len(m) == 2:
        return det2(m)
    if len(m) == 3:
        return det3(m)
    if len(m) == 4:
        return det4(m)


def inverse(m: Matrix) -> Matrix:
    n = len(m)
    a = Matrix(n=n, m=2 * n)

    for i in range(n):
        for j in range(n):
            a[i][j] = m[i][j]

    set_identity(a, n)
    gaus_jordan(a, n)
    row_operations_principal_diagonal(a, n)

    im = Matrix(n=n)
    for i in range(n):
        for j in range(n):
            im[i][j] = a[i][j + n]

    return im


def normal_matrix(m: Matrix, as_lower_order: bool = False):
    a = transpose(inverse(m))
    if not as_lower_order:
        return a
    else:
        le = len(a)
        b = Matrix(n=le - 1)
        for i in range(le - 1):
            for j in range(le - 1):
                b[i][j] = a[i][j]
        return b


def size_of(obj: Union[Vector, Matrix]) -> int:
    inputType = type(obj).__name__
    inputSize = len(obj)
    retdict = {
        Matrix.__name__: 4 * inputSize * inputSize,
        Vector.__name__: 4 * inputSize
    }
    ret = retdict.get(inputType)

    return ret


def normalize(v, exclude_last_comp: bool = False) -> Vector:
    variables = [x * x for x in v]
    v_length = 0.0
    for i in variables:
        v_length += i
    v_length = math.sqrt(abs(v_length))

    if not math.isfinite(float(v_length)):
        raise Exception("normalize vector {} has zero length".format(v))

    if exclude_last_comp:
        excep = 1
    else:
        excep = 0

    if v_length == 0:
        return Vector(0, 0, 0)

    for i in range(len(v) - excep):
        v[i] /= v_length

    if type(v).__name__ == list.__name__:
        return Vector(v)
    else:
        return Vector(v.elements)


def dot(u: Vector or list, v: Vector or list) -> float:
    if len(u) != len(v):
        raise Exception("tried to dot vectors of different lengths")

    ret = 0.0
    for i in range(len(u)):
        ret += u[i] * v[i]

    return ret


def vlength(v: Vector) -> float:
    ret = 0
    for i in range(len(v)):
        ret += v[i] * v[i]

    return math.sqrt(ret)


def look_at(eye, at, up) -> Matrix:
    if eye == at:
        return Matrix()

    v = normalize(at - eye)
    n = normalize(v * up)
    u = normalize(n * v)

    v = -v

    result = Matrix([
        [*n, -dot(n, eye)],
        [*u, -dot(u, eye)],
        [*v, -dot(v, eye)],
        [0, 0, 0, 1]])

    return result


def ortho(left, right, bottom, top, near, far) -> Matrix:
    if left == right:
        raise Exception("ortho(): left and right are equal")
    if bottom == top:
        raise Exception("ortho(): bottom and top are equal")
    if near == far:
        raise Exception("ortho(): near and far are equal")

    w = right - left
    h = top - bottom
    d = far - near

    result = Matrix()

    result[0][0] = 2.0 / w
    result[1][1] = 2.0 / h
    result[2][2] = -2.0 / d
    result[0][3] = -(left + right) / w
    result[1][3] = -(top + bottom) / h
    result[2][3] = -(near + far) / d

    return result


def perspective(fovy, aspect, near, far) -> Matrix:
    f = 1.0 / math.tan(radians(fovy) / 2)
    d = far - near

    result = Matrix()
    result[0][0] = f / aspect
    result[1][1] = f
    result[2][2] = -(near + far) / d
    result[2][3] = -2 * near * far / d
    result[3][2] = -1
    result[3][3] = 0.0

    return result


def translate(input):
    m = Matrix(n=4)
    m[0][3] = input[0]
    m[1][3] = input[1]
    m[2][3] = input[2]

    return input


def rotate(axis):
    return rotateZ(axis[2]) * rotateY(axis[1]) * rotateX(axis[0])

    """
    c = math.cos(radians(angle))
    omc = 1.0-c
    s = math.sin(angle)

    m = Matrix([[x*x*omc + c,   x*y*omc - z*s, x*z*omc + y*s, 0.0],
                [x*y*omc + z*s, y*y*omc + c,   y*z*omc - x*s, 0.0],
                [x*z*omc - y*s, y*z*omc + x*s, z*z*omc + c,   0.0],
                [0,0,0,1]
                ])
    return m
    """


def rotateX(theta):
    c = math.cos(radians(theta))
    s = math.sin(radians(theta))
    rz = Matrix(inputData=[[1.0, 0.0, 0.0, 0.0],
                           [0.0, c, -s, 0.0],
                           [0.0, s, c, 0.0],
                           [0.0, 0.0, 0.0, 1.0]
                           ])
    return rz


def rotateY(theta):
    c = math.cos(radians(theta))
    s = math.sin(radians(theta))
    rz = Matrix(inputData=[[c, 0.0, s, 0.0],
                           [0.0, 1.0, 0.0, 0.0],
                           [-s, 0.0, c, 0.0],
                           [0.0, 0.0, 0.0, 1.0]
                           ])
    return rz


def rotateZ(theta):
    c = math.cos(radians(theta))
    s = math.sin(radians(theta))
    rz = Matrix(inputData=[[c, -s, 0.0, 0.0],
                           [s, c, 0.0, 0.0, ],
                           [0.0, 0.0, 1.0, 0.0],
                           [0.0, 0.0, 0.0, 1.0]
                           ])
    return rz


def matrix_to_euler(m):
    if (m[1][0] > 0.999999999):
        # singularity at north pole
        heading = math.atan2(m[0][2], m[2][2])
        attitude = math.pi / 2
        bank = 0

    elif (m[1][0] < -0.999999999):
        # // singularity at south pole
        heading = math.atan2(m[0][2], m[2][2])
        attitude = -math.pi / 2
        bank = 0
    else:
        heading = math.atan2(-m[2][0], m[0][0])
        attitude = math.asin(m[1][0])
        bank = math.atan2(-m[1][2], m[1][1])

    return degrees(bank), degrees(heading), degrees(attitude)


def scale(input):
    m = Matrix(n=4)
    m[0][0] = input[0]
    m[1][1] = input[1]
    m[2][2] = input[2]

    return m


def euler_to_quaternion(euler_angles):
    heading = radians(euler_angles[0])
    attitude = radians(euler_angles[1])
    bank = radians(euler_angles[2])

    c1 = math.cos(heading / 2)
    s1 = math.sin(heading / 2)
    c2 = math.cos(attitude / 2)
    s2 = math.sin(attitude / 2)
    c3 = math.cos(bank / 2)
    s3 = math.sin(bank / 2)

    c1c2 = c1 * c2
    s1s2 = s1 * s2

    w = c1c2 * c3 - s1s2 * s3
    x = c1c2 * s3 + s1s2 * c3
    y = s1 * c2 * c3 + c1 * s2 * s3
    z = c1 * s2 * c3 - s1 * c2 * s3

    return Quaternion(quats=(x, y, z, w))


def euler_to_matrix(euler_angles):
    heading = radians(euler_angles[0])
    attitude = radians(euler_angles[1])
    bank = radians(euler_angles[2])

    ch = math.cos(heading)
    sh = math.sin(heading)
    ca = math.cos(attitude)
    sa = math.sin(attitude)
    cb = math.cos(bank)
    sb = math.sin(bank)

    res = Matrix([[ch * ca, sh * sb - ch * sa * cb, ch * sa * sb + sh * cb, 0],
                  [sa, ca * cb, -ca * sb, 0],
                  [-sh * ca, sh * sa * cb + ch * sb, -sh * sa * sb + ch * cb, 0],
                  [0, 0, 0, 1]])

    """res = Matrix([[cb * ca, sh * sa * cb - ch * sb, ch * sa * ca + sh * sa, 0],
                  [ca * sb, sh * sa * sb + ch * cb, ch * sa * sb - sh * cb, 0],
                  [-sa, sh * ca, ch * ca, 0],
                  [0, 0, 0, 1]])"""
    return res


def matrix_to_quaternion(m):
    trace = m[0][0] + m[1][1] + m[2][2]

    if trace > 0:
        S = 0.5 / math.sqrt(trace + 1.0)
        qw = 0.25 / S
        qx = (m[2][1] - m[1][2]) * S
        qy = (m[0][2] - m[2][0]) * S
        qz = (m[1][0] - m[0][1]) * S
    elif m[0][0] > m[1][1] and m[0][0] > m[2][2]:
        S = 2.0 * math.sqrt(1.0 + m[0][0] - m[1][1] - m[2][2])
        S1 = 1 / S

        qw = (m[2][1] - m[1][2]) * S1
        qx = 0.25 * S
        qy = (m[0][1] + m[1][0]) * S1
        qz = (m[0][1] - m[2][0]) * S1
    elif m[1][1] > m[2][2]:
        S = math.sqrt(1.0 + m[1][1] - [0][0] - m[2][2]) * 2.0
        S1 = 1 / S
        qw = (m[0][2] - m[2][0]) * S1
        qx = (m[0][1] + m[1][0]) * S1
        qy = 0.25 * S
        qz = (m[1][2] + m[2][1]) * S1
    else:
        S = math.sqrt(1.0 + m[2][2] - m[0][0] - m[1][1]) * 2
        S1 = 1 / S

        qw = (m[1][0] - m[0][1]) * S1
        qx = (m[0][2] + m[2][0]) * S1
        qy = (m[1][2] + m[2][1]) * S1
        qz = 0.25 * S

    return Quaternion(quats=[qx, qy, qz, qw])


def quaternion_to_matrix(q):
    m = Matrix(n=4)

    sqw = q.w * q.w
    sqx = q.i * q.i
    sqy = q.j * q.j
    sqz = q.k * q.k

    denom =  (sqx + sqy + sqz + sqw)
    if denom ==0:
        denom = 1
    invs = 1 / denom
    m00 = (sqx - sqy - sqz + sqw) * invs
    m11 = (-sqx + sqy - sqz + sqw) * invs
    m22 = (-sqx - sqy + sqz + sqw) * invs
    tmp1 = q.i * q.j
    tmp2 = q.k * q.w
    m10 = 2.0 * (tmp1 + tmp2) * invs
    m01 = 2.0 * (tmp1 - tmp2) * invs
    tmp1 = q.i * q.k
    tmp2 = q.j * q.w
    m20 = 2.0 * (tmp1 - tmp2) * invs
    m02 = 2.0 * (tmp1 + tmp2) * invs
    tmp1 = q.j * q.k
    tmp2 = q.i * q.w
    m21 = 2.0 * (tmp1 + tmp2) * invs
    m12 = 2.0 * (tmp1 - tmp2) * invs

    m.m = [[m00, m01, m02, 0],
           [m10, m11, m12, 0],
           [m20, m21, m22, 0],
           [0, 0, 0, 1]]

    return m


def normalize_q(q):
    return math.sqrt(q.w * q.w + q.i * q.i + q.j * q.j + q.k * q.k)


def conjugate(quat: Quaternion):
    i = quat.i * -1
    j = quat.j * -1
    k = quat.k * -1
    return Quaternion(i, j, k, quat.w)


def quat_2_euler(q: Quaternion):
    d = normalize_q(q)

    q = q / d

    sqw = q.w * q.w
    sqx = q.i * q.i
    sqy = q.j * q.j
    sqz = q.k * q.k

    unit = sqx + sqy + sqz + sqw

    test = q.i * q.j + q.k * q.w

    if test > 0.4999999:  # * unit:  # singularity at north pole
        heading = 2 * math.atan2(q.i, q.w)
        attitude = math.pi / 2
        bank = 0
        return degrees(heading), degrees(attitude), degrees(bank)

    if test < -0.499999:  # * unit:  # singularity at south pole
        heading = -2 * math.atan2(q.i, q.w)
        attitude = - math.pi / 2
        bank = 0
        return degrees(heading), degrees(attitude), degrees(bank)

    sqx = q.i * q.i
    sqy = q.j * q.j
    sqz = q.k * q.k

    heading = math.atan2(2 * q.j * q.w - 2 * q.i * q.k, 1 - 2 * sqy - 2 * sqz)
    tt = 2 * test
    attitude = math.asin(tt / unit)
    bank = math.atan2(2 * q.i * q.w - 2 * q.j * q.k, 1 - 2 * sqx - 2 * sqz)

    # heading = math.atan2(2 * q.j * q.w - 2 * q.i * q.k, sqx - sqy - sqz + sqw)
    # attitude = math.asin(2 * test / unit)
    # bank = math.atan2(2 * q.i * q.w - 2 * q.j * q.k, -sqx + sqy - sqz + sqw)

    return degrees(heading), degrees(attitude), degrees(bank)


def within_radius(position, light):
    if type(light).__name__ == "PointLight":
        if vlength(light - position) <= light.radius:
            return True


def get_pointLight_radius(pointLight):
    """
    method for calculating the bounding Sphere radius of a given point light
    based on anything less than 1/256 is total black
    :param pointLight:
    :return:
    """
    colour_range = 256
    maxchannel = (pointLight.colour[0] + pointLight.colour[1] + pointLight.colour[2]) / 3
    attenuation = pointLight.attenuation
    intensity = pointLight.intensity
    linear = attenuation.linear
    const = attenuation.const
    exp = attenuation.exp

    ret = (-linear + math.sqrt(linear * linear - 4 * exp * (const - colour_range * maxchannel * intensity))) / 2 * exp
    return ret
