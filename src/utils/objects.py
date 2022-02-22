import math
from src.utils.objectUtils import Matrix, degrees, quat_2_euler, to_quaternion, get_pointLight_radius
from src.utils.objectUtils import Vector
from src.utils.objectUtils import rotate


class Transform:

    def __init__(self, size=4):
        self.T = Matrix(n=size)
        self.S = Matrix(n=size)
        self.R = Matrix(n=size)
        self.m = Matrix(n=size)

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

        m = to_quaternion(self.R)
        x,y,z = quat_2_euler(*m)

        return [degrees(x), degrees(y), degrees(z)]

    def set_scale(self, s: list):
        scale = [1,1,1]
        for i in range(len(self.m) - 1):
            self.S[i][i] = s[i]
        self._update_transform()

    def _update_transform(self):
        self.m = (self.T*self.R)*self.S

    def set_rotation(self, newrot: list or Vector):

        self.m *= rotate(newrot)
        newrot = [math.radians(x) for x in newrot]

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

        tx,ty,tz = self.get_position()
        sx,sy,sz = self.get_scale()
        self.R.m =[[m00*sx,m01,m02,tx],
                   [m10,m11*sy,m12,ty],
                   [m20,m21,m22*sz,tz],
                   [0,0,0,1]
                   ]

        self._update_transform()

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
    pass


class PointLight(BaseLight):
    const = 4 * math.pi

    def __init__(self):
        super(PointLight, self).__init__()
        self.intensity = 1
        self.colour = Vector(1, 1, 1)
        self.attenuation = Attenuation()
        self.radius = get_pointLight_radius(self)


class Shader:
    pass


class Material:
    def __init__(self, *args):
        pass

