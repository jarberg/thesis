import os
import numpy
from OpenGL import GL
from OpenGL.GL import glGetUniformLocation, glUniformMatrix4fv, glDrawArrays, GL_TRIANGLES, glUniform1i, glFlush, \
    GL_ACTIVE_PROGRAM, GL_CURRENT_PROGRAM, glBindTexture, GL_TEXTURE_2D_MULTISAMPLE

import constants
from opengl_interfacing.texture import Texture_Manager
from utils.objectUtils import flatten, perspective
from utils.objects import Transform, Model
from PIL import Image


class Renderer:

    def __init__(self, program, _obj=None):
        self.objects = _obj or []
        self.persp = flatten(perspective(90, 1, 0, 100))

    def draw(self):

        for obj in self.objects:
            mat = obj.get_material()
            if mat.tex_diffuse_b:
                loc = glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "tex_diffuse")
                if loc != -1:
                    slot = mat.get_diffuse()
                    glUniform1i(loc, slot)
            glUniformMatrix4fv(2, 1, False, self.persp)
            glUniformMatrix4fv(3, 1, False, flatten(obj.getTransform()))
            obj.draw()

            glDrawArrays(GL_TRIANGLES, 0, len(obj.vertexArray))

    def postDraw(self, objects, program, tex):
        GL.glUseProgram(program)

        glBindTexture(GL_TEXTURE_2D_MULTISAMPLE, tex)

        for obj in objects:
            mat = obj.get_material()
            if mat.tex_diffuse_b:
                loc = glGetUniformLocation(program, "screencapture")
                if loc != -1:

                    glUniform1i(loc, tex)
            #glUniformMatrix4fv(2, 1, False, self.persp)
            glUniformMatrix4fv(3, 1, False, flatten(obj.getTransform()))
            obj.draw()

            glDrawArrays(GL_TRIANGLES, 0, len(obj.vertexArray))


    def bind(self):
        pass

    def unbind(self):
        pass


class Plane(Model):
    def __init__(self,plane=None):
        plane = plane or [[0.5, 0.5, 0],
                 [0.5, -0.5, 0],
                 [-0.5, 0.5, 0],
                 [-0.5, -0.5, 0],
                 [-0.5, 0.5, 0],
                 [0.5, -0.5, 0],
                 ]
        self.coordArray = [
            [0.0, 0.0],
            [0.0, 1.0],
            [1.0, 0.0],
            [1.0, 1.0],
            [1.0, 0.0],
            [0.0, 1.0],
        ]
        super().__init__(plane, self.coordArray)


class ImagePlane(Plane):

    def __init__(self, path=None, size=None):
        super().__init__()
        if path:
            root = constants.ROOT_DIR
            path = os.path.abspath(root + path).replace("\\", "/")
            im = Image.open(fp=path)
            imdata = numpy.array(list(im.getdata()))

            self.material.set_tex_diffuse(
                Texture_Manager().createNewTexture(size=[im.size[0], im.size[1]], data=imdata, mipmap=True))
        else:
            self.material.set_tex_diffuse(
                Texture_Manager().createNewTexture(size=[size[0], size[1]]))