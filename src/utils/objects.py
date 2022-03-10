import math

import numpy
from OpenGL import GL
from OpenGL.GL import glVertexAttribPointer, GL_CURRENT_PROGRAM, glDisableVertexAttribArray, glGenVertexArrays, \
    glBindVertexArray
from OpenGL.raw.GL.VERSION.GL_1_5 import glBindBuffer, GL_ARRAY_BUFFER, glBufferData, GL_STATIC_DRAW
from OpenGL.raw.GL.VERSION.GL_2_0 import glEnableVertexAttribArray
from OpenGL.raw.GL._types import GLfloat, GL_FLOAT

from src.utils.objectUtils import Matrix, degrees, quat_2_euler, matrix_to_quaternion, get_pointLight_radius, \
    Quaternion, euler_to_quaternion, quaternion_2_matrix, flatten, cross, normal_matrix
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
        x, y, z = quat_2_euler(q)

        return [degrees(x), degrees(y), degrees(z)]

    def set_scale(self, s: list):
        scale = [1, 1, 1]
        for i in range(len(self.m) - 1):
            self.S[i][i] = s[i]
        self._update_transform()

    def _update_transform(self):
        self.m = self.T * (self.R * self.S)

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


def calc_normal_from_points(p0, p1, p2):
    v1 = Vector(p1) - Vector(p0)
    v2 = Vector(p2) - Vector(p0)
    n = cross(v1, v2)
    return n


class Model(Transform):

    def __init__(self, vertexlist, coordArray=None):
        super().__init__()

        self.boundingBox = []
        self.vertexArray = []
        self.normalArray = []
        self.coordArray = coordArray or []

        for i in range(len(vertexlist)):
            self._add_vertex(vertexlist[i])
            j = i + 1
            if i != 0 and (j % 3) == 0:
                normal = calc_normal_from_points(vertexlist[i - 2], vertexlist[i - 1], vertexlist[i])
                self.normalArray.append(normal)
                self.normalArray.append(normal)
                self.normalArray.append(normal)

        self.material = Material()
        self.initBuffers()
        self.initDataToBuffers()

    def _update_transform(self):
        super()._update_transform()
        self.normalMatrix = normal_matrix(self.getTransform(), True)

    def get_normalMatrix(self):
        return self.normalMatrix

    def get_material(self):
        return self.material

    def initBuffers(self):
        self.vBuffer = GL.glGenBuffers(1)
        self.cBuffer = GL.glGenBuffers(1)
        self.nBuffer = GL.glGenBuffers(1)
        # self.iBuffer = GL.glGenBuffers(1)

    def initDataToBuffers(self):
        self.vPosition = GL.glGetAttribLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "a_Position")
        self.vCoord = GL.glGetAttribLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "InTexCoords")
        self.vNormal = GL.glGetAttribLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "inNormal")

        v_array = flatten(self.vertexArray)
        c_array = flatten(self.coordArray)
        n_array = flatten(self.normalArray)

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.vBuffer)
        glBufferData(GL_ARRAY_BUFFER, v_array.nbytes, v_array, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(self.vPosition)

        glBindBuffer(GL_ARRAY_BUFFER, self.cBuffer)
        glBufferData(GL_ARRAY_BUFFER, c_array.nbytes, c_array, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 2, GL_FLOAT, False, 0, None)
        if self.vCoord > 0:
            glEnableVertexAttribArray(self.vCoord)

        glBindBuffer(GL_ARRAY_BUFFER, self.nBuffer)
        glBufferData(GL_ARRAY_BUFFER, n_array.nbytes, n_array, GL_STATIC_DRAW)
        glVertexAttribPointer(4, 3, GL_FLOAT, False, 0, None)
        if self.vNormal > 0:
            glEnableVertexAttribArray(self.vNormal)

    def initAttributeVariable(self, a_attribute, buffer, size, var_type, offset=0, step=0):
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, buffer)
        GL.glVertexAttribPointer(a_attribute, size, var_type, True, offset, step)
        GL.glEnableVertexAttribArray(a_attribute)


    def _add_vertex(self, vertex: list):
        self.vertexArray.append(vertex)
        self._update_boundingBox(vertex)

    def _update_boundingBox(self, p):
        if len(self.boundingBox) > 3:
            p1 = self.boundingBox[0]
            p2 = self.boundingBox[1]
            p3 = self.boundingBox[2]
            p4 = self.boundingBox[3]
            self.boundingBox[0] = [min(p[0], p1[0]), min(p[1], p1[1]), min(p[2], p1[2])]
            self.boundingBox[1] = [max(p[0], p2[0]), min(p[1], p2[1]), min(p[2], p2[2])]
            self.boundingBox[2] = [min(p[0], p3[0]), max(p[1], p3[1]), min(p[2], p3[2])]
            self.boundingBox[3] = [min(p[0], p4[0]), min(p[1], p4[1]), max(p[2], p4[2])]
        else:
            p1 = p
            p2 = p
            p3 = p
            p4 = p
            self.boundingBox.append([min(p[0], p1[0]), min(p[1], p1[1]), min(p[2], p1[2])])
            self.boundingBox.append([max(p[0], p2[0]), min(p[1], p2[1]), min(p[2], p2[2])])
            self.boundingBox.append([min(p[0], p3[0]), max(p[1], p3[1]), min(p[2], p3[2])])
            self.boundingBox.append([min(p[0], p4[0]), min(p[1], p4[1]), max(p[2], p4[2])])


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
    def __init__(self, tex_diffuse=None):
        if tex_diffuse is not None:
            self.tex_diffuse_b = True
            self.tex_diffuse = tex_diffuse
            self.diffuse_color = [1, 1, 1, 1]
        else:
            self.tex_diffuse_b = False

    def get_diffuse(self):
        if self.tex_diffuse_b:
            return self.tex_diffuse.slot
        else:
            return self.diffuse_color

    def set_tex_diffuse(self, tex):
        self.tex_diffuse_b = True
        self.tex_diffuse = tex
