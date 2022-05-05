import numpy
from OpenGL.GL import glGetUniformLocation, glUniformMatrix4fv, glDrawArrays, glUniform1i, \
    GL_CURRENT_PROGRAM, glBindVertexArray, glUniformMatrix3fv, GL_LINES, \
    glDepthFunc, GL_ALWAYS, GL_LESS, glUniform1f, glUseProgram, glGetIntegerv, glFlush, glViewport

from opengl_interfacing import texture
from opengl_interfacing.framebuffer import G_Buffer, L_Buffer, clear_framebuffer
from opengl_interfacing.initshader import initShaders
from opengl_interfacing.sceneObjects import Plane, Sphere
from opengl_interfacing.utils import get_window_width, get_window_height
from utils.general import fps_update
from utils.objectUtils import flatten


class Renderer:

    def __init__(self, currScene, size):

        self.skinningProgram = initShaders("/shader/skinning/skinning_v_cpu_interpolate.glsl", "/shader/skinning/skinning_f.glsl")
        self.jointProgram = initShaders("/shader/debug/joint_v_shader.glsl", "/shader/debug/joint_f_shader.glsl")

        glUseProgram(self.skinningProgram)

        self.currScene = currScene
        self.width = size[0]
        self.height = size[1]
        self.quad = Plane()
        self.quad.set_rotation([180, 0, 0])
        self.lightSphere = Sphere()

        self.lightBuffer = L_Buffer([size[0], size[1]])
        self.GBuffer = G_Buffer([size[0], size[1]])

        _set_window_properties(size[0], size[1])
        self.lightAmount = 0

    def resize(self, w, h):
        glViewport(0, 0, get_window_width(), get_window_height())

        self.currScene.get_current_camera().update_pMatrix(w/h)
        self.lightBuffer.resize(w, h)
        self.GBuffer.resize(w, h)
        self.width = w
        self.height = h
        _set_window_properties(w, h)

        clear_framebuffer([0, 0, 0, 1])


    def skinning_draw(self):

        clear_framebuffer()
        glUseProgram(self.skinningProgram)

        _set_cam_attributes(self.currScene.get_current_camera())

        for obj in self.currScene.get_entity_list():

            _set_animator_attributes(obj)

            _set_obj_mat_attributes(obj)
            _set_normalMatrix_attribute(obj)
            _set_obj_transform_attributes(obj)
            _set_obj_skin_attributes(obj)

            obj.draw()

        if self.currScene.debug:
            self.debug_draw()
            glUseProgram(self.jointProgram)
            self.joint_draw()


        glFlush()

        self.currScene.animators[0].update(fps_update())


    def debug_draw(self):

        _set_cam_attributes(self.currScene.get_current_camera())

        glUniform1i(glGetUniformLocation(glGetIntegerv(GL_CURRENT_PROGRAM), "debug"), 1)
        glDepthFunc(GL_ALWAYS)

        for obj in self.currScene.get_entity_list():
            _set_animator_attributes(obj)
            _set_obj_transform_attributes(obj)
            _set_obj_skin_attributes(obj)

            obj.draw(True)

        glUniform1i(glGetUniformLocation(glGetIntegerv(GL_CURRENT_PROGRAM), "debug"), 0)
        glDepthFunc(GL_LESS)

    def joint_draw(self):
        cam = self.currScene.get_current_camera()
        glDepthFunc(GL_ALWAYS)
        glUniformMatrix4fv(glGetUniformLocation(glGetIntegerv(GL_CURRENT_PROGRAM), "projection"), 1, False,
                           cam.pMatrix)
        glUniformMatrix4fv(glGetUniformLocation(glGetIntegerv(GL_CURRENT_PROGRAM), "v_matrix"), 1, False,
                           flatten(cam._getTransform()), False)

        for obj in self.currScene.get_joints():

            glUniformMatrix4fv(glGetUniformLocation(glGetIntegerv(GL_CURRENT_PROGRAM), "obj_transform"), 1,
                               False, flatten(obj.getTransform()))

            glBindVertexArray(obj.getVAO())
            glDrawArrays(GL_LINES, 0, obj.get_vertexArray_len())

        glDepthFunc(GL_LESS)


def _set_cam_attributes(cam):
    if cam:
        program = glGetIntegerv(GL_CURRENT_PROGRAM)
        p_loc = glGetUniformLocation(program, "projection")
        v_loc = glGetUniformLocation(program, "v_matrix")
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
            transforms = flatten(trans)
            glUniformMatrix4fv(glGetUniformLocation(glGetIntegerv(GL_CURRENT_PROGRAM), "jointTransforms"),
                               len(animator.curPoseList),
                               False, transforms)


def _set_window_properties(w, h):
    program = glGetIntegerv(GL_CURRENT_PROGRAM)

    glUniform1i(glGetUniformLocation(program, "width"), w)
    glUniform1i(glGetUniformLocation(program, "height"), h)


def _set_obj_lights_attributes(lightList):
    program = glGetIntegerv(GL_CURRENT_PROGRAM)

    lights_loc = glGetUniformLocation(program, "lights")
    if lights_loc != -1 and len(lightList) > 0:
        data = flatten(lightList)
        glUniform1i(lights_loc, data)
    lightsNum_loc = glGetUniformLocation(program, "lightnum")
    if lightsNum_loc != -1:
        glUniform1i(lightsNum_loc, 0)


def _set_obj_mat_attributes(obj):
    mat = obj.get_material()
    program = glGetIntegerv(GL_CURRENT_PROGRAM)

    b_tex_loc = glGetUniformLocation(program, "tex_diffuse_b")
    if b_tex_loc != -1:
        glUniform1i(b_tex_loc, mat.tex_diffuse_b)
    tex_loc = glGetUniformLocation(program, "tex_diffuse")
    if tex_loc != -1 and mat.tex_diffuse_b:
        tex = mat.get_diffuse()
        texture.bind(tex)
        glUniform1i(tex_loc, tex.slot)


def _set_obj_transform_attributes(obj):
    t_loc = glGetUniformLocation(glGetIntegerv(GL_CURRENT_PROGRAM), "obj_transform")
    if t_loc != -1:
        glUniformMatrix4fv(t_loc, 1, False, flatten(obj.getTransform()))


def _set_obj_skin_attributes(obj):
    skin_loc = glGetUniformLocation(glGetIntegerv(GL_CURRENT_PROGRAM), "skinned")
    if skin_loc != -1:
        if hasattr(obj, "skinned"):
            glUniform1i(skin_loc, obj.skinned)
        else:
            glUniform1i(skin_loc, 0)


def _set_normalMatrix_attribute(obj):
    loc = glGetUniformLocation(glGetIntegerv(GL_CURRENT_PROGRAM), "normal_matrix")
    if loc != -1:
        glUniformMatrix3fv(loc, 1, False, flatten(obj.get_normalMatrix()))


def _set_GPU_animation_attributes(animator):
    stamp_loc = glGetUniformLocation(glGetIntegerv(GL_CURRENT_PROGRAM), "timestamp")
    if stamp_loc > -1:
        glUniform1f(stamp_loc, flatten(animator.animTime))
    rowLength_loc = glGetUniformLocation(glGetIntegerv(GL_CURRENT_PROGRAM), "rowLength")
    if rowLength_loc:
        glUniform1i(rowLength_loc, flatten(len(animator.animation.keyframes[0].transforms), data_type=numpy.int16))
