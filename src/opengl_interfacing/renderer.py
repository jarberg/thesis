from random import randrange

import numpy
from OpenGL import GL
from OpenGL.GL import glGetUniformLocation, glUniformMatrix4fv, glDrawArrays, GL_TRIANGLES, glUniform1i, \
    GL_CURRENT_PROGRAM, glBindVertexArray, glUniform1fv, glUniform2fv, glUniformMatrix3fv, GL_LINES, \
    glDepthFunc, GL_ALWAYS, GL_LESS, glUniform1f, glUniform3fv

from opengl_interfacing import texture
from opengl_interfacing.framebuffer import G_Buffer
from utils.objectUtils import flatten, flatten_list
from utils.objects import Plane


class Renderer:

    def __init__(self, currScene):

        self.currScene = currScene
        self.quad = Plane()
        self.quad.set_rotation([0, 180, 0])


    def draw(self):
        _set_cam_attributes(self.currScene.get_current_camera())

        for obj in self.currScene.get_entity_list():

            _set_obj_mat_attributes(obj)
            _set_normalMatrix_attribute(obj)
            _set_obj_transform_attributes(obj)

            obj.draw()

    def skinning_draw(self):

        _set_cam_attributes(self.currScene.get_current_camera())

        for obj in self.currScene.get_entity_list():
            if self.currScene.GPU:
                _set_animator_attributes(obj)
            else:
                _set_animator_attributes(obj)

            _set_obj_mat_attributes(obj)
            _set_normalMatrix_attribute(obj)
            _set_obj_transform_attributes(obj)
            _set_obj_skin_attributes(obj)

            obj.draw()

    def debug_draw(self):

        _set_cam_attributes(self.currScene.get_current_camera())

        glUniform1i(glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "debug"), 1)
        glDepthFunc(GL_ALWAYS)

        for obj in self.currScene.get_entity_list():
            _set_animator_attributes(obj)
            _set_obj_transform_attributes(obj)
            _set_obj_skin_attributes(obj)

            obj.draw(True)

        glUniform1i(glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "debug"), 0)
        glDepthFunc(GL_LESS)

    def joint_draw(self):
        cam = self.currScene.get_current_camera()
        glDepthFunc(GL_ALWAYS)
        glUniformMatrix4fv(glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "projection"), 1, False, cam.pMatrix)
        glUniformMatrix4fv(glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "v_matrix"), 1, False, flatten(cam._getTransform()), False)


        for obj in  self.currScene.get_joints():
            if len(self.currScene.animators[0].curPoseList) > 0 and False:
                glUniformMatrix4fv(glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "obj_transform"), 1, False, flatten(animator.curPoseList[obj.id]))
            else:
                glUniformMatrix4fv(glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "obj_transform"), 1, False, flatten(obj.getTransform()))

            glBindVertexArray(obj.getVAO())
            glDrawArrays(GL_LINES, 0, obj.get_vertexArray_len())

        glDepthFunc(GL_LESS)

    def light_draw(self, buffer: G_Buffer):
        currProgram = GL.glGetIntegerv(GL_CURRENT_PROGRAM)
        cam = self.currScene.get_current_camera()
        texture.bind(buffer.position_tex)
        texture.bind(buffer.normal_tex)
        texture.bind(buffer.albedo_tex)

        loc1 = glGetUniformLocation(currProgram, "pos")
        glUniform1i(loc1, buffer.position_tex.slot)
        loc2 = glGetUniformLocation(currProgram, "norm")
        glUniform1i(loc2, buffer.normal_tex.slot)
        loc3 = glGetUniformLocation(currProgram, "albedo")
        glUniform1i(loc3, buffer.albedo_tex.slot)
        v_loc = glGetUniformLocation(currProgram, "viewPos")
        glUniform3fv(v_loc, 1, flatten(cam.eye))
        glUniformMatrix4fv(glGetUniformLocation(currProgram, "obj_transform"), 1, False,
                           flatten(self.quad.getTransform()))

        self.quad.draw()

    def postDraw(self, program, tex, postBuffer):
        GL.glUseProgram(program)

        loc = glGetUniformLocation(program, "screencapture")
        if loc != -1:
            glUniform1i(loc, tex.slot)


        glUniform1i(glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "viewport_width"), postBuffer.width)
        glUniform1i(glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "viewport_height"), postBuffer.height)
        glUniform1i(glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "samples"), postBuffer.get_samples())


        glUniformMatrix4fv(3, 1, False, flatten(self.quad.getTransform()))

        glBindVertexArray(self.quad.VAO)
        glDrawArrays(GL_TRIANGLES, 0, len(self.quad.vertexArray))

    def randDraw(self, objects, program, fps):
        GL.glUseProgram(program)
        v = []
        for i in range(4):
            v.append([])
            for j in range(4):
                v[i].append(randrange(-1, 1))
                v[i].append(randrange(-1, 1))

        glUniform1fv(glGetUniformLocation(program, "timeI"), 1, fps / 10000000)
        loc = glGetUniformLocation(program, "vectors")
        vv = flatten(v)
        glUniform2fv(loc, vv.nbytes, vv)

        for obj in objects:
            glBindVertexArray(obj.VAO)
            glDrawArrays(GL_TRIANGLES, 0, len(obj.vertexArray))

def _set_cam_attributes(cam):
    if cam:
        p_loc = glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "projection")
        v_loc = glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "v_matrix")
        if p_loc != -1:
            glUniformMatrix4fv(p_loc, 1, False, cam.pMatrix)
        if v_loc != -1:
            glUniformMatrix4fv(v_loc, 1, False, flatten(cam._getTransform()), False)

def _set_animator_attributes(obj):
    if hasattr(obj, "animator"):
        animator = obj.animator
        if animator and len(animator.curPoseList) > 0:
            trans = []
            for k in range(len(animator.curPoseList)):
                trans.append(animator.curPoseList[k])
            transforms = flatten_list(trans)
            glUniformMatrix4fv(glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "jointTransforms"),
                               len(animator.curPoseList),
                               False, transforms)

def _set_obj_mat_attributes(obj):
    mat = obj.get_material()
    program = GL.glGetIntegerv(GL_CURRENT_PROGRAM)

    b_tex_loc = glGetUniformLocation(program, "tex_diffuse_b")
    if b_tex_loc != -1:
        glUniform1i(b_tex_loc, mat.tex_diffuse_b)
    tex_loc = glGetUniformLocation(program, "tex_diffuse")
    if tex_loc != -1 and mat.tex_diffuse_b:
        tex = mat.get_diffuse()
        texture.bind(tex)
        glUniform1i(tex_loc, tex.slot)

def _set_obj_transform_attributes(obj):
    t_loc = glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "obj_transform")
    if t_loc != -1:
        glUniformMatrix4fv(t_loc, 1, False, flatten(obj.getTransform()))

def _set_obj_skin_attributes(obj):
    skin_loc = glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "skinned")
    if skin_loc != -1:
        if hasattr(obj, "skinned"):
            glUniform1i(skin_loc, obj.skinned)
        else:
            glUniform1i(skin_loc, 0)

def _set_normalMatrix_attribute(obj):
    loc = glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "normal_matrix")
    if loc != -1:
        glUniformMatrix3fv(loc, 1, False, flatten(obj.get_normalMatrix()))

def _set_GPU_animation_attributes(animator):
    stamp_loc = glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "timestamp")
    if stamp_loc > -1:
        glUniform1f(stamp_loc, flatten(animator.animTime))
    rowLength_loc = glGetUniformLocation(GL.glGetIntegerv(GL_CURRENT_PROGRAM), "rowLength")
    if rowLength_loc:
        glUniform1i(rowLength_loc, flatten(len(animator.animation.keyframes[0].transforms), data_type=numpy.int16))

