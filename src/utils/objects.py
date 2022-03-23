import math

from OpenGL.GL import glVertexAttribPointer, GL_CURRENT_PROGRAM, glGenVertexArrays, \
    glBindVertexArray, glGenBuffers, glGetIntegerv, GL_FLOAT, glBindBuffer, GL_ARRAY_BUFFER, glBufferData, \
    GL_STATIC_DRAW, glEnableVertexAttribArray, glGetAttribLocation, GL_INT

from src.utils.objectUtils import Matrix, get_pointLight_radius, \
    flatten, cross, normal_matrix, inverse, euler_to_matrix
from src.utils.objectUtils import Vector


def calc_normal_from_points(p0, p1, p2):
    v1 = Vector(p1) - Vector(p0)
    v2 = Vector(p2) - Vector(p0)
    n = cross(v1, v2)
    return n


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

    def getTransform(self, useParent=False):
        if self.parent and useParent:
            return self.parent.getTransform()*self.m
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
        self.m = self.T * self.R * self.S

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

class Joint(Transform):
    def __init__(self, id, parent=None, children=None, bindTransform=None):
        super(Joint, self).__init__(parent=parent, children=children)
        self.id = id
        self.bindTransform = bindTransform or Transform()
        self.inverseBindTransform = inverse(self.bindTransform.m)

        self.vertexArray = [[0, 0, 0], [0.5, 0, 0]]
        self.initBuffers()
        self.initDataToBuffers()

    def getTransform(self):
        return self.m

    def add_child(self, child):
        self.children.append(child)

    def set_bind_transform(self, transform):
        self.bindTransform = transform
        self.calcInverseBindTransform(self.bindTransform)

    def calcInverseBindTransform(self, parentBindTransform):
        self.bindTransform.m = parentBindTransform.m * self.bindTransform.m
        self.inverseBindTransform.m = inverse(self.bindTransform.m)

        for child in self.children:
            child.calcInverseBindTransform(self.bindTransform)

    def initBuffers(self):
        self.vBuffer = glGenBuffers(1)

    def initDataToBuffers(self):
        self.vPosition = glGetAttribLocation(glGetIntegerv(GL_CURRENT_PROGRAM), "a_Position")

        v_array = flatten(self.vertexArray)

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.vBuffer)
        glBufferData(GL_ARRAY_BUFFER, v_array.nbytes, v_array, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(self.vPosition)


class Model(Transform):

    def __init__(self, vertexlist, coordArray=None, n_array = None):
        super().__init__()

        self.boundingBox = []
        self.vertexArray = []
        self.normalArray = []
        self.coordArray = coordArray or []

        if n_array:
            self.normalArray = n_array
        else:
            for i in range(len(vertexlist)):
                self._add_vertex(vertexlist[i])
                j = i+1
                if i != 0 and (j % 3) == 0:
                    p1 = vertexlist[i - 2]
                    p2 = vertexlist[i - 1]
                    p3 = vertexlist[i]
                    normal = calc_normal_from_points(p1, p2, p3)

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

    def getVAO(self):
        return self.VAO

    def get_vertexArray_len(self):
        return len(self.vertexArray)

    def initBuffers(self):
        self.vBuffer = glGenBuffers(1)
        self.cBuffer = glGenBuffers(1)
        self.nBuffer = glGenBuffers(1)
        # self.iBuffer = GL.glGenBuffers(1)

    def initDataToBuffers(self):
        self.vPosition = glGetAttribLocation(glGetIntegerv(GL_CURRENT_PROGRAM), "a_Position")
        self.vCoord = glGetAttribLocation(glGetIntegerv(GL_CURRENT_PROGRAM), "InTexCoords")
        self.vNormal = glGetAttribLocation(glGetIntegerv(GL_CURRENT_PROGRAM), "inNormal")

        v_array = flatten(self.vertexArray)
        c_array = flatten(self.coordArray)
        n_array = flatten(self.normalArray)

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.vBuffer)
        glBufferData(GL_ARRAY_BUFFER, v_array.nbytes, v_array, GL_STATIC_DRAW)
        glVertexAttribPointer(self.vPosition, 3, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(self.vPosition)

        glBindBuffer(GL_ARRAY_BUFFER, self.cBuffer)
        glBufferData(GL_ARRAY_BUFFER, c_array.nbytes, c_array, GL_STATIC_DRAW)
        glVertexAttribPointer( self.vCoord, 2, GL_FLOAT, False, 0, None)
        if self.vCoord > 0:
            glEnableVertexAttribArray(self.vCoord)

        glBindBuffer(GL_ARRAY_BUFFER, self.nBuffer)
        glBufferData(GL_ARRAY_BUFFER, n_array.nbytes, n_array, GL_STATIC_DRAW)
        glVertexAttribPointer(self.vNormal, 3, GL_FLOAT, False, 0, None)
        if self.vNormal > 0:
            glEnableVertexAttribArray(self.vNormal)

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
            self.boundingBox.append([p[0], p[1], p[2]])
            self.boundingBox.append([p[0], p[1], p[2]])
            self.boundingBox.append([p[0], p[1], p[2]])
            self.boundingBox.append([p[0], p[1], p[2]])


class Animated_model:
    def __init__(self, model: Model, rootJoint, jointCount):
        self.model = model
        self.rootJoint = rootJoint
        self.jointCount = jointCount
        self.skinned = 1

        self.joint_indices = [
            [0],
            [0],
            [0],
            [0],
            [0],
            [0],
            [0],
            [0],
            [0],
            [0],
            [0],
            [0],
            [0],
            [0],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
        ]
        self.weights = [
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
        ]

        self.model.material.tex_diffuse_b = False

        glBindVertexArray(self.model.VAO)
        jointIndice_array = flatten(self.joint_indices)

        self.JointIndices_Loc = glGetAttribLocation(glGetIntegerv(GL_CURRENT_PROGRAM), "in_joint_indices")
        self.JIBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.JIBuffer)
        glBufferData(GL_ARRAY_BUFFER, jointIndice_array.nbytes, jointIndice_array, GL_STATIC_DRAW)
        glVertexAttribPointer(self.JointIndices_Loc, 3, GL_INT, False, 0, None)
        glEnableVertexAttribArray(self.JointIndices_Loc)

        glBindVertexArray(self.model.VAO)
        w_array = flatten(self.joint_indices)
        self.skinWieghts_Loc = glGetAttribLocation(glGetIntegerv(GL_CURRENT_PROGRAM), "in_weights")
        self.swBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.swBuffer)
        glBufferData(GL_ARRAY_BUFFER, w_array.nbytes, w_array, GL_STATIC_DRAW)
        glVertexAttribPointer(self.skinWieghts_Loc, 3, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(self.skinWieghts_Loc)



    def _update_transform(self):
        self.model._update_transform()

    def get_normalMatrix(self):
        return self.model.normalMatrix

    def get_material(self):
        return self.model.get_material()

    def getTransform(self):
        return self.model.getTransform()

    def getVAO(self):
        return self.model.VAO

    def get_vertexArray_len(self):
        return self.model.get_vertexArray_len()

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


def initAttributeVariable(a_attribute, buffer, size, var_type, offset=0, step=0):
    glBindBuffer(GL_ARRAY_BUFFER, buffer)
    glVertexAttribPointer(a_attribute, size, var_type, True, offset, step)
    glEnableVertexAttribArray(a_attribute)
