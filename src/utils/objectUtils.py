import decimal
from typing import Union
import math

from src.utils.objects import Matrix
from src.utils.objects import Vector


EPSILON = 0.00000000000001
EPISLON_LEN = abs(decimal.Decimal(str(EPSILON)).as_tuple().exponent)


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
                ratio = m[j][i]/m[i][i]
                for k in range(2*size):
                    m[j][k] = m[j][k] - ratio * m[i][k]


def row_operations_principal_diagonal(m, size):
    for i in range(0, size):
        for j in range(size, 2*size):
            m[i][j] = m[i][j]/m[i][i]


def flatten(obj):
    return [x for x in obj]


def radians(degrees):
    return degrees * math.pi / 180.0


def degrees(radians):
    return round(radians / math.pi * 180.0, EPISLON_LEN)


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
    a = inverse(transpose(m))
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

    return Vector(v.elements)


def dot(u: Vector, v: Vector) -> float:
    if len(u) != len(v):
        raise Exception("tried to dot vectors of different lengths")

    ret = 0.0
    for i in range(len(u)):
        ret += u[i] * v[i]

    return ret


def length(v: Vector) -> float:
    return math.sqrt(dot(v, v))




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

    return rotateZ(axis[2])*rotateY(axis[1])*rotateX(axis[0])


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
                           [ 0.0, c, s, 0.0],
                           [0.0, -s, c, 0.0],
                           [0.0, 0.0, 0.0, 1.0]
                           ])
    return rz

def rotateY(theta):
    c = math.cos(radians(theta))
    s = math.sin(radians(theta))
    rz = Matrix(inputData=[[c, 0.0, -s, 0.0],
                           [0.0, 1.0, 0.0, 0.0],
                           [s, 0.0, c, 0.0],
                           [0.0, 0.0, 0.0, 1.0]
                           ])
    return rz


def rotateZ(theta):
    c = math.cos(radians(theta))
    s = math.sin(radians(theta))
    rz = Matrix(inputData=[[c, s, 0.0, 0.0],
                           [-s, c, 0.0, 0.0,],
                           [0.0, 0.0, 1.0, 0.0],
                           [0.0, 0.0, 0.0, 1.0]
                           ])
    return rz


def scale(input):

    m = Matrix(n=4)
    m[0][0] = input[0]
    m[1][1] = input[1]
    m[2][2] = input[2]

    return m