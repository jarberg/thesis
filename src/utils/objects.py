import math
from src.utils.objectUtils import Matrix, degrees, quat_2_euler, matrix_to_quaternion, get_pointLight_radius, \
    Quaternion, euler_to_quaternion, quaternion_2_matrix
from src.utils.objectUtils import Vector
from src.utils.objectUtils import rotate


class Transform:

    def __init__(self, size=4):
        self.T = Matrix(n=size)
        self.S = Matrix(n=size)
        self.R = Matrix(n=size)
        self.m = Matrix(n=size)
        self._update_transform()

    def getTransform(self):
        return self.m

    def get_position(self):
        return [self.T[0][3], self.T[1][3], self.T[2][3]]

    def get_scale(self):
        ret = [0, 0, 0]

        for i in range(min(len(self.S) - 1, 3)):
            for j in range(min(len(self.S[i]) - 1, 3)):
                ret[i] += math.pow(self.S[j][i], 2)
            ret[i] = math.sqrt(ret[i])

        return ret

    def get_rotation(self):

        q = Quaternion(quats=matrix_to_quaternion(self.R.m))
        x,y,z = quat_2_euler(q)

        return [degrees(x), degrees(y), degrees(z)]

    def set_scale(self, s: list):
        scale = [1,1,1]
        for i in range(len(self.m) - 1):
            self.S[i][i] = s[i]
        self._update_transform()

    def _update_transform(self):
        self.m = (self.T*self.R)*self.S

    def set_rotation(self, newrot: list or Vector):


        q = euler_to_quaternion(newrot)
        self.R.m = quaternion_2_matrix(q).m

        self._update_transform()
        """
        newrot = [x * math.pi / 180 for x in newrot]
        ch = math.cos(newrot[0])
        sh = math.sin(newrot[0])
        ca = math.cos(newrot[1])
        sa = math.sin(newrot[1])
        cb = math.cos(newrot[2])
        sb = math.sin(newrot[2])

        m00 = ch * ca
        m01 = sh * sb - ch * sa * cb
        m02 = ch * sa * sb + sh * cb
        m10 = sa
        m11 = ca * cb
        m12 = -ca * sb
        m20 = -sh * ca
        m21 = sh * sa * cb + ch * sb
        m22 = -sh * sa * sb + ch * cb

        self.R.m =[[m00,m01,m02,0],
                   [m10,m11,m12,0],
                   [m20,m21,m22,0],
                   [0,0,0,1]
                   ]
        """


    def set_position(self, newPos: list or Vector):
        minval = min(len(self.m) - 1, 3)
        for i in range(min(minval, 3)):
            self.T[i][min(minval, 3)] = newPos[i]
        self._update_transform()


class Model(Transform):

    def __init__(self):
        super().__init__()
        self.boundingBox = []
        self.vertexArray = []

    def _add_vertex(self, vertex: list):
        self.vertexArray.append(vertex)
        self._update_boundingBox(vertex)

    def _update_boundingBox(self, p):
        p1 = self.boundingBox[0]
        p2 = self.boundingBox[1]
        p3 = self.boundingBox[2]
        p4 = self.boundingBox[3]

        self.boundingBox[0] = Vector(min(p[0], p1[0]), min(p[1], p1[1]), min(p[2], p1[2]))
        self.boundingBox[1] = Vector(max(p[0], p2[0]), min(p[1], p2[1]), min(p[2], p2[2]))
        self.boundingBox[2] = Vector(min(p[0], p3[0]), max(p[1], p3[1]), min(p[2], p3[2]))
        self.boundingBox[3] = Vector(min(p[0], p4[0]), min(p[1], p4[1]), max(p[2], p4[2]))


class Attenuation:
    def __init__(self, const=1, linear=1, exp=1):
        self.const = const
        self.linear = linear
        self.exp = exp


class BaseLight(Transform):

    def __init__(self):
        super(BaseLight, self).__init__()
        self.intensity = 1
        self.colour = Vector(1, 1, 1)

class PointLight(BaseLight):

    def __init__(self):
        super(PointLight, self).__init__()
        self.attenuation = Attenuation()
        self.radius = get_pointLight_radius(self)


class Shader:
    pass


class Material:
    def __init__(self, *args):
        pass


