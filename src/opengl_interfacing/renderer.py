import os
from random import randrange

import numpy
from OpenGL import GL
from OpenGL.GL import glGetUniformLocation, glUniformMatrix4fv, glDrawArrays, GL_TRIANGLES, glUniform1i, \
    GL_CURRENT_PROGRAM, glBindVertexArray, glUniform1fv, glUniform2fv, glUniformMatrix3fv
from PIL import Image

import constants
from opengl_interfacing.framebuffer import G_Buffer
from opengl_interfacing.texture import Texture_Manager
from utils.objectUtils import flatten, perspective
from utils.objects import Model


class Renderer:

    def __init__(self, _obj=None):
        self.objects = _obj or []
        self.persp = flatten(perspective(90, 1, 0.01, 100))
        self.quad = Plane(plane=[[1, 1, 0],
                        [1, -1, 0],
                        [-1, 1, 0],
                        [-1, -1, 0],
                        [-1, 1, 0],
                        [1, -1, 0],
                        ])
        self.quad.set_rotation([0,180,0])

    def draw(self):
        for obj in self.objects:
            mat = obj.get_material()
            glUniform1i(glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "tex_diffuse_b"), mat.tex_diffuse_b)
            if mat.tex_diffuse_b:
                loc = glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "tex_diffuse")
                if loc != -1:
                    slot = mat.get_diffuse()
                    glUniform1i(loc, slot)

            loc = glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "normal_matrix")
            if loc != -1:
                glUniformMatrix3fv(loc, 1, False, flatten(obj.get_normalMatrix()))

            glUniformMatrix4fv(2, 1, False, self.persp)
            glUniformMatrix4fv(3, 1, False, flatten(obj.getTransform()))

            glBindVertexArray(obj.VAO)
            glDrawArrays(GL_TRIANGLES, 0, len(obj.vertexArray))

    def light_draw(self, buffer: G_Buffer):
        loc1 = glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "pos")
        glUniform1i(loc1, buffer.position_tex.slot)
        loc2 = glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "norm")
        glUniform1i(loc2, buffer.normal_tex.slot)
        loc3 = glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "albedo")
        glUniform1i(loc3, buffer.normal_tex.slot)

        glUniformMatrix4fv(3, 1, False, flatten(self.quad.getTransform()))

        glBindVertexArray(self.quad.VAO)
        glDrawArrays(GL_TRIANGLES, 0, len(self.quad.vertexArray))

    def postDraw(self, program, tex):
        GL.glUseProgram(program)

        loc = glGetUniformLocation(program, "screencapture")
        if loc != -1:
            glUniform1i(loc, tex.slot)

        glUniformMatrix4fv(3, 1, False, flatten(self.quad.getTransform()))

        glBindVertexArray(self.quad.VAO)
        glDrawArrays(GL_TRIANGLES, 0, len(self.quad.vertexArray))

    def randDraw(self, objects, program, fps):
        GL.glUseProgram(program)
        v=[]
        for i in range(4):
            v.append([])
            for j in range(4):
                v[i].append(randrange(-1, 1))
                v[i].append(randrange(-1, 1))

        glUniform1fv(glGetUniformLocation(program, "timeI"), 1, fps/10000000)
        loc = glGetUniformLocation(program, "vectors")
        vv = flatten(v)
        glUniform2fv(loc, vv.nbytes, vv)

        for obj in objects:
            glBindVertexArray(obj.VAO)
            glDrawArrays(GL_TRIANGLES, 0, len(obj.vertexArray))




class Bigbrainjoints(Model):

    def __init__(self, vertexlist):
        super().__init__(vertexlist)
        self.joints = []
        self.parents = {}
        self.transforms = {}
        self.bindTransforms = {}
        self.inverseBindTransforms = {}
        self.children = {}




class Plane(Model):
    def __init__(self, plane=None):
        plane = plane or [
                        [0.5, 0.5, 0],
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


class Cube(Model):
    def __init__(self):
        vertexes = [
            [-0.5, -0.5, -0.5],
            [-0.5, -0.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 0.5, -0.5],
            [-0.5, -0.5, -0.5],
            [-0.5, 0.5, -0.5],
            [0.5, -0.5, 0.5],
            [-0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
            [0.5, -0.5, -0.5],
            [-0.5, -0.5, -0.5],
            [-0.5, -0.5, -0.5],
            [-0.5, 0.5, 0.5],
            [-0.5, 0.5, -0.5],
            [0.5, -0.5, 0.5],
            [-0.5, -0.5, 0.5],
            [-0.5, -0.5, -0.5],
            [-0.5, 0.5, 0.5],
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5],
            [0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
            [0.5, -0.5, -0.5],
            [0.5, 0.5, 0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5],
            [0.5, 0.5, -0.5],
            [-0.5, 0.5, -0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 0.5, -0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, -0.5, 0.5]]
        vertexcoord = [
            [-1.0, -1.0],
            [-1.0, -1.0],
            [-1.0, 1.0],
            [1.0, 1.0],
            [-1.0, -1.0],
            [-1.0, 1.0],
            [1.0, -1.0],
            [-1.0, -1.0],
            [1.0, -1.0],
            [1.0, 1.0],
            [1.0, -1.0],
            [-1.0, -1.0],
            [-1.0, -1.0],
            [-1.0, 1.0],
            [-1.0, 1.0],
            [1.0, -1.0],
            [-1.0, -1.0],
            [-1.0, -1.0],
            [-1.0, 1.0],
            [-1.0, -1.0],
            [1.0, -1.0],
            [1.0, 1.0],
            [1.0, -1.0],
            [1.0, 1.0],
            [1.0, -1.0],
            [1.0, 1.0],
            [1.0, -1.0],
            [1.0, 1.0],
            [1.0, 1.0],
            [-1.0, 1.0],
            [1.0, 1.0],
            [-1.0, 1.0],
            [-1.0, 1.0],
            [1.0, 1.0],
            [-1.0, 1.0],
            [1.0, -1.0]]
        super().__init__(vertexes, vertexcoord)
        self.material.tex_diffuse_b = False
