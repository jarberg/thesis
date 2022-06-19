import math

from utils.objectUtils import Matrix, get_pointLight_radius, \
    euler_to_matrix, det4
from utils.objectUtils import Vector


class Transform:

    def __init__(self, parent=None, children=None, size=4):
        self.rot = [0, 0, 0]
        self.T = Matrix(n=size)
        self.S = Matrix(n=size)
        self.R = Matrix(n=size)
        self.m = Matrix(n=size)

        self.children = children or []
        self.parent = parent

        if self.parent:
            self.parent.children.append(self)

        self._update_transform()

    def __len__(self):
        return len(self.m)

    def getTransform(self, useParent=False):
        if self.parent and useParent:
            return self.parent.getTransform(useParent) * self.m
        else:
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
        return self.rot

    def set_scale(self, s: list):
        for i in range(len(self.m) - 1):
            self.S[i][i] = s[i]
        self._update_transform()

    def _update_transform(self):
        self.m = self.T * self.R / det4(self.R) * self.S

    def set_rotation(self, newrot: list or Vector):
        self.rot[0] = newrot[0] % 360
        self.rot[1] = newrot[1] % 360
        self.rot[2] = newrot[2] % 360

        self.R = euler_to_matrix(self.rot)
        self._update_transform()

    def set_position(self, newPos: list or Vector):
        minval = min(len(self.m) - 1, 3)
        for i in range(min(minval, 3)):
            self.T[i][min(minval, 3)] = newPos[i]
        self._update_transform()

    def set_transform(self, m):
        self.m = m


class Attenuation:
    def __init__(self, const=1, linear=1, exp=1):
        self.const = const
        self.linear = linear
        self.exp = exp


class BaseLight(Transform):

    def __init__(self, intensity=None, color=None):
        super(BaseLight, self).__init__()
        self.intensity = 1
        self.colour = Vector(1, 1, 1)


class PointLight(BaseLight):

    def __init__(self, intensity=None, color=None, attenuation=None):
        super(PointLight, self).__init__()
        self.intensity = intensity or 1
        self.color = color or Vector(1, 1, 1)
        self.attenuation = attenuation or Attenuation(1, 1, 1)
        self.radius = get_pointLight_radius(self)


class Shader:
    pass


class Material:
    def __init__(self, tex_diffuse=None, col=None):
        if col is None:
            self.diffuse_color = [1, 1, 1, 1]
        else:
            self.diffuse_color = col
        if tex_diffuse is not None:
            self.tex_diffuse_b = True
            self.tex_diffuse = tex_diffuse
        else:
            self.tex_diffuse_b = False

    def get_diffuse(self):
        if self.tex_diffuse_b:
            return self.tex_diffuse
        else:
            return self.diffuse_color

    def set_tex_diffuse(self, tex):
        self.tex_diffuse_b = True
        self.tex_diffuse = tex


