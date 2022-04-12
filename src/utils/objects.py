import math
import os

import numpy
from OpenGL.GL import glVertexAttribPointer, GL_CURRENT_PROGRAM, glGenVertexArrays, \
    glBindVertexArray, glGenBuffers, glGetIntegerv, GL_FLOAT, glBindBuffer, GL_ARRAY_BUFFER, glBufferData, \
    GL_STATIC_DRAW, glEnableVertexAttribArray, glGetAttribLocation, GL_INT, GL_TRIANGLE_STRIP, GL_ELEMENT_ARRAY_BUFFER, \
    glDrawArrays, GL_UNSIGNED_SHORT, glDrawElements, GL_LINES, glVertexAttribIPointer, \
    GL_LINE_STRIP, GL_TRIANGLES

from PIL import Image
import constants
from opengl_interfacing.texture import Texture, Texture_Manager
from src.utils.objectUtils import Matrix, get_pointLight_radius, \
    flatten, cross, normal_matrix, inverse, euler_to_matrix, det4, get_opengl_format, is_mipmapable
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
        self.m = self.T * self.R/det4(self.R) * self.S

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
    def __init__(self, id, name="", parent=None, children=None):
        super(Joint, self).__init__(parent=parent, children=children)
        self.id = id
        self.name = name
        self.vertexArray = [[0, 0, 0], [0.5, 0, 0]]
        self.initBuffers()
        self.initDataToBuffers()

    def draw(self, debug=False):
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_LINES, 0, self.get_vertexArray_len())

    def add_child(self, child):
        self.children.append(child)

    def set_anim_transform(self, m):
        self.anim_transform = m

    def get_anim_transform(self):
        return self.anim_transform

    def set_local_bind_transform(self, transform=None):
        self.localBindTransform = transform or self.getTransform()

    def calcInverseBindTransform(self, parentBindTransform):
        bindTransform = parentBindTransform * self.localBindTransform
        self.inverseBindTransform = inverse(bindTransform)

        for child in self.children:
            child.calcInverseBindTransform(bindTransform)

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

    def getVAO(self):
        return self.VAO

    def get_vertexArray_len(self):
        return len(self.vertexArray)

def set_bind_transform_from_self(joint):
    joint.localBindTransform = joint.getTransform()
    for child in joint.children:
        set_bind_transform_from_self(child)

def calcInverseBindTransform(joint, parentBindTransform):
    joint.localBindTransform = parentBindTransform * joint.localBindTransform
    joint.inverseBindTransform = inverse(joint.localBindTransform)

    for child in joint.children:
        child.calcInverseBindTransform(joint.localBindTransform)


class Model(Transform):

    def __init__(self, vertexlist, coordArray=None, n_array=None, weights=None, windices=None, renderType=GL_TRIANGLE_STRIP):
        super().__init__()

        self.have_windices = windices is not None
        self.have_weights = weights is not None

        self.windices = windices

        self.weights = weights or []
        self.boundingBox = []
        self.vertexArray = []
        self.normalArray = n_array or []
        self.coordArray = coordArray or []
        self.renderType = renderType

        for i in range(len(vertexlist)):
            self._add_vertex(vertexlist[i])

        self.material = Material()

        coords = False
        normals = False
        if coordArray:
            coords = True
        if n_array:
            normals = True

        self.buffers = {}

        self.initBuffers(normals, coords,(self.have_weights and self.have_windices))
        self.initDataToBuffers(normals, coords,( self.have_weights and self.have_windices))

    def draw(self, debug=False):
        glBindVertexArray(self.getVAO())
        glDrawArrays(self.renderType, 0, self.get_vertexArray_len())

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

    def initBuffers(self, normal, coords, influences):
        self.buffers["vertex_pos"] = Buffer()

        if normal:
            self.buffers["normal"] = Buffer()
        if coords:
            self.buffers["tex_coords"] = Buffer()
        if influences:
            self.buffers["influ_indices"] = Buffer()
            self.buffers["influ_weights"] = Buffer()

        self.buffers["indices"] = Buffer(buf_type=GL_ELEMENT_ARRAY_BUFFER)

    def initDataToBuffers(self, normal=True, coords=True, influences=None):

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)
        self.buffers["vertex_pos"] .bind_vertex_attribute("a_Position", flatten(self.vertexArray), 3, GL_FLOAT, 0)
        if normal:
            self.buffers["normal"].bind_vertex_attribute("inNormal", flatten(self.normalArray), 3, GL_FLOAT, 0)
        if coords:
            self.buffers["tex_coords"].bind_vertex_attribute("InTexCoords", flatten(self.coordArray), 2, GL_FLOAT, 0)
        if influences:
            self.buffers["influ_indices"].bind_vertex_attribute("in_joint_indices", flatten(self.windices), 4, GL_FLOAT, 0)
            self.buffers["influ_weights"].bind_vertex_attribute("in_weights", flatten(self.weights), 4, GL_FLOAT, 0)


    def _add_vertex(self, vertex: list):
        self.vertexArray.append(vertex)
        #self._update_boundingBox(vertex)

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


class IndicedModel(Transform):

    def __init__(self, vertexlist, indices, coordArray=None, n_array=None, weights=None, windices=None, renderType=GL_TRIANGLE_STRIP):
        super().__init__()

        self.have_windices = windices is not None
        self.have_weights = weights is not None

        self.windices = windices

        self.weights = weights or []
        self.indices = indices
        self.boundingBox = []
        self.vertexArray = []
        self.normalArray = n_array or []
        self.coordArray = coordArray or []
        self.renderType = renderType

        for i in range(len(vertexlist)):
            self._add_vertex(vertexlist[i])

        self.material = Material()

        coords = False
        normals = False
        if coordArray:
            coords = True
        if n_array:
            normals = True

        self.buffers = {}

        self.initBuffers(normals, coords,(self.have_weights and self.have_windices))
        self.initDataToBuffers(normals, coords,( self.have_weights and self.have_windices))

    def draw(self, debug=False):
        if debug:
            glBindVertexArray(self.getVAO())
            glDrawElements(GL_LINE_STRIP, len(self.indices), GL_UNSIGNED_SHORT, None)
        else:
            glBindVertexArray(self.getVAO())
            glDrawElements(self.renderType, len(self.indices), GL_UNSIGNED_SHORT, None)

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

    def initBuffers(self, normal, coords, influences):
        self.buffers["vertex_pos"] = Buffer()

        if normal:
            self.buffers["normal"] = Buffer()
        if coords:
            self.buffers["tex_coords"] = Buffer()
        if influences:
            self.buffers["influ_indices"] = Buffer()
            self.buffers["influ_weights"] = Buffer()

        self.buffers["indices"] = Buffer(buf_type=GL_ELEMENT_ARRAY_BUFFER)

    def initDataToBuffers(self, normal=True, coords=True, influences=None):

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)
        self.buffers["vertex_pos"] .bind_vertex_attribute("a_Position", flatten(self.vertexArray), 3, GL_FLOAT, 0)
        if normal:
            self.buffers["normal"].bind_vertex_attribute("inNormal", flatten(self.normalArray), 3, GL_FLOAT, 0)
        if coords:
            self.buffers["tex_coords"].bind_vertex_attribute("InTexCoords", flatten(self.coordArray), 2, GL_FLOAT, 0)
        if influences:
            self.buffers["influ_indices"].bind_vertex_attribute("in_joint_indices", flatten(self.windices), 4, GL_FLOAT, 0)
            self.buffers["influ_weights"].bind_vertex_attribute("in_weights", flatten(self.weights), 4, GL_FLOAT, 0)


        self.buffers["indices"].bind(flatten(self.indices, data_type=numpy.uint16))

    def _add_vertex(self, vertex: list):
        self.vertexArray.append(vertex)
        #self._update_boundingBox(vertex)

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


class Buffer:
    def __init__(self, buf_type=GL_ARRAY_BUFFER, usage=GL_STATIC_DRAW):
        self.slot = glGenBuffers(1)
        self.buffer_type = buf_type
        self.usage = usage
        self.attributes = {}

    def bind(self, indice=None):
        glBindBuffer(self.buffer_type, self.slot)
        if indice is not None:
            glBufferData(self.buffer_type, indice.nbytes, indice, self.usage)

    def add_data(self, data):
        glBufferData(self.buffer_type, data.nbytes, data, self.usage)

    def get_attribute_location(self, name):
        return glGetAttribLocation(glGetIntegerv(GL_CURRENT_PROGRAM), name)

    def bind_vertex_attribute(self, name, data=None, data_len=3, data_type=GL_FLOAT, offset=0, VAO=None):
        if VAO:
            glBindVertexArray(VAO)
        self.bind()
        self.add_data(data)
        attributeSlot = self.get_attribute_location(name)
        if attributeSlot >= 0:
            if data_type == GL_INT:
                glVertexAttribIPointer(attributeSlot, data_len, data_type, offset, None)
            elif data_type == GL_FLOAT:
                glVertexAttribPointer(attributeSlot, data_len, data_type, False, offset, None)

            glEnableVertexAttribArray(attributeSlot)
            self.attributes[name] = attributeSlot


class Animated_model:
    def __init__(self, model, rootJoint, jointCount):
        self.model = model
        self.rootJoint = rootJoint
        self.jointCount = jointCount
        self.skinned = 1
        self.animator = None

    def set_animator(self, animator):
        self.animator = animator

    def draw(self, debug=False):
        self.model.draw(debug=debug)

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
            return self.tex_diffuse.slot
        else:
            return self.diffuse_color

    def set_tex_diffuse(self, tex):
        self.tex_diffuse_b = True
        self.tex_diffuse = tex



class Plane(Model):
    def __init__(self):
        plane = [[1, 1, 0],
                 [1, -1, 0],
                 [-1, 1, 0],
                 [-1, -1, 0],
                 [-1, 1, 0],
                 [1, -1, 0],
                 ]
        coordArray = [
            [0.0, 0.0],
            [0.0, 1.0],
            [1.0, 0.0],
            [1.0, 1.0],
            [1.0, 0.0],
            [0.0, 1.0],
        ]
        normals = [[0, 0, -1],
                   [0, 0, -1],
                   [0, 0, -1],
                   [0, 0, -1],
                   [0, 0, -1],
                   [0, 0, -1]
                   ]
        super().__init__(vertexlist=plane, n_array=normals, coordArray=coordArray)




class ImagePlane(Plane):

    def __init__(self, path=None, size=None):
        super().__init__()
        if path:
            Texture_Manager().createNewTexture(path)
        else:
            im_mipmap = is_mipmapable(size[0], size[1])
            self.material.set_tex_diffuse(Texture(size=[size[0], size[1]]))


class Cube(IndicedModel):

    def __init__(self):
        vertex = [[-0.500000, -0.500000, 0.500000],
                  [0.500000, -0.500000, 0.500000],
                  [-0.500000, 0.500000, 0.500000],
                  [0.500000, 0.500000, 0.500000],

                  [-0.500000, 0.500000, -0.500000],
                  [0.500000, 0.500000, -0.500000],
                  [-0.500000, -0.500000, -0.500000],
                  [0.500000, -0.500000, -0.500000],

                  [-0.500000, -0.500000, 0.500000],
                  [0.500000, -0.500000, 0.500000],
                  [0.500000, 0.500000, 0.500000],
                  [-0.500000, 0.500000, 0.500000],

                  [0.500000, 0.500000, 0.500000],
                  [0.500000, 0.500000, -0.500000],
                  [-0.500000, 0.500000, -0.500000],
                  [-0.500000, 0.500000, 0.500000],

                  [0.500000, 0.500000, -0.500000],
                  [0.500000, -0.500000, -0.500000],
                  [-0.500000, -0.500000, -0.500000],
                  [-0.500000, 0.500000, -0.500000],

                  [0.500000, -0.500000, -0.500000],
                  [0.500000, -0.500000, 0.500000],
                  [-0.500000, -0.500000, -0.500000],
                  [-0.500000, -0.500000, 0.500000]]
        coord = [[0.000000, 0.000000],
                 [1.000000, 0.000000],
                 [1.000000, 1.000000],
                 [0.000000, 1.000000],
                 [1.000000, 0.000000],
                 [0.000000, 0.000000],
                 [0.000000, 1.000000],
                 [1.000000, 1.000000],
                 [0.000000, 0.000000],
                 [1.000000, 0.000000],
                 [1.000000, 1.000000],
                 [0.000000, 1.000000],
                 [1.000000, 0.000000],
                 [1.000000, 1.000000],
                 [0.000000, 1.000000],
                 [0.000000, 0.000000],
                 [1.000000, 1.000000],
                 [1.000000, 0.000000],
                 [0.000000, 0.000000],
                 [0.000000, 1.000000],
                 [1.000000, 1.000000],
                 [1.000000, 0.000000],
                 [0.000000, 1.000000],
                 [0.000000, 0.000000]]
        normal = [
           [-1.000000, 0.000000, 0.000000],
           [1.000000, 0.000000, 0.000000],
           [-1.000000, 0.000000, 0.000000],
           [1.000000, 0.000000, 0.000000],

           [-1.000000, 0.000000, 0.000000],
           [1.000000, 0.000000, 0.000000],
           [-1.000000, 0.000000, 0.000000],
           [1.000000, 0.000000, 0.000000],

           [0.000000, 0.000000, 1.000000],
           [0.000000, 0.000000, 1.000000],
           [0.000000, 0.000000, 1.000000],
           [0.000000, 0.000000, 1.000000],

            [0.000000, 1.000000, 0.000000],
            [0.000000, 1.000000, 0.000000],
            [0.000000, 1.000000, 0.000000],
            [0.000000, 1.000000, 0.000000],

            [0.000000, 0.000000, -1.000000],
            [0.000000, 0.000000, -1.000000],
            [0.000000, 0.000000, -1.000000],
            [0.000000, 0.000000, -1.000000],

            [0.000000, -1.000000, 0.000000],
            [0.000000, -1.000000, 0.000000],
            [0.000000, -1.000000, 0.000000],
            [0.000000, -1.000000, 0.000000], ]
        indice = [8, 9, 10,
                  8, 10, 11,
                  15, 12, 13,
                  15, 13, 14,
                  19, 16, 17,
                  19, 17, 18,
                  22, 20, 21,
                  22, 21, 23,
                  1, 7, 5,
                  1, 5, 3,
                  6, 0, 2,
                  6, 2, 4]
        super().__init__(indices=indice, vertexlist=vertex, n_array=normal, coordArray=coord, renderType=GL_TRIANGLES)





def initAttributeVariable(a_attribute, buffer, size, var_type, offset=0, step=0):
    glBindBuffer(GL_ARRAY_BUFFER, buffer)
    glVertexAttribPointer(a_attribute, size, var_type, True, offset, step)
    glEnableVertexAttribArray(a_attribute)
