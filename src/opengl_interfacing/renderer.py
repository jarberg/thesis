import os
import numpy
from OpenGL.GL import glGetUniformLocation, glUniformMatrix4fv, glDrawArrays, GL_TRIANGLES, glUniform1i

import constants
from opengl_interfacing.texture import Texture_Manager
from utils.objectUtils import flatten, perspective
from utils.objects import Transform, Model
from PIL import Image


class Renderer:

    def __init__(self, program, _obj = None):
        self.objects = _obj or []
        self.program = program
        self.persp = flatten(perspective(90, 1, 0, 100))

    def draw(self):
        for obj in self.objects:
            mat = obj.get_material()
            if mat.tex_diffuse_b:
                loc = glGetUniformLocation(self.program, "tex_diffuse")
                slot = mat.get_diffuse()
                glUniform1i(loc, slot)

            glUniformMatrix4fv(2, 1, False,  self.persp)
            glUniformMatrix4fv(3, 1, False, flatten(obj.getTransform()))

            obj.draw()

            glDrawArrays(GL_TRIANGLES, 0, len(obj.vertexArray))

    def bind(self):
        pass

    def unbind(self):
        pass


class Plane(Model):
    def __init__(self, program):
        plane = [[0.5, 0.5,   0],
                 [0.5, -0.5,  0],
                 [-0.5, 0.5,  0],
                 [-0.5, -0.5, 0],
                 [-0.5, 0.5,  0],
                 [0.5, -0.5,  0],
                 ]
        self.coordArray = [
            [0.0, 0.0],
            [0.0, 1.0],
            [1.0, 0.0],
            [1.0, 1.0],
            [1.0, 0.0],
            [0.0, 1.0],
        ]
        super().__init__(program, plane,  self.coordArray)


class ImagePlane(Plane):

    def __init__(self, path, program):
        super().__init__(program)
        root = constants.ROOT_DIR
        path = os.path.abspath(root + path).replace("\\", "/")
        im = Image.open(fp=path)
        imdata = numpy.array(list(im.getdata()))


        Texture_Manager().createNewTexture(size=[im.size[0], im.size[1]], data=imdata, mipmap = True)

        self.material.set_tex_diffuse(Texture_Manager().createNewTexture(size=[im.size[0], im.size[1]], data=imdata, mipmap = True))
