import numpy
from OpenGL.GL import glGetUniformLocation, glUniformMatrix4fv, glUniform1i, \
    GL_CURRENT_PROGRAM, glBindVertexArray, glUniformMatrix3fv, glDepthFunc, GL_ALWAYS, GL_LESS, glUniform1f, \
    glUniform3fv, glDrawElementsInstanced, GL_UNSIGNED_SHORT, \
    glUseProgram, glBlendFunc, GL_ONE, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, glEnable, GL_CULL_FACE, glDisable, \
    glCullFace, GL_BACK, GL_FRONT, GL_BLEND, GL_DEPTH_TEST, glGetIntegerv, glFlush, glViewport

from opengl_interfacing import texture
from opengl_interfacing.framebuffer import G_Buffer, L_Buffer, blit_to_default, clear_framebuffer
from opengl_interfacing.initshader import initShaders
from opengl_interfacing.sceneObjects import Plane, Sphere
from opengl_interfacing.utils import get_window_width, get_window_height
from utils.general import fps_update
from utils.objectUtils import flatten


class Renderer:

    def __init__(self, currScene, size):
        self.forwardProgram = initShaders("/shader/forward/vertex-shader.glsl",
                                          "/shader/forward/fragment-shader.glsl")
        self.deferred_program = initShaders("/shader/defered/defered_v_shader.glsl",
                                            "/shader/defered/defered_f_shader.glsl")
        self.lightProgram = initShaders("/shader/defered/defered_light_v_shader.glsl",
                                        "/shader/defered/defered_light_f_shader.glsl")
        self.lightSphereShader = initShaders("/shader/defered/deferred_lightSphere_v_shader.glsl",
                                             "/shader/defered/deferred_lightSphere_f_shader.glsl")

        glUseProgram(self.deferred_program)

        self.currScene = currScene
        self.width = size[0]
        self.height = size[1]
        self.quad = Plane()
        self.quad.set_rotation([180, 0, 0])
        self.lightSphere = Sphere()

        self.lightBuffer = L_Buffer([size[0], size[1]])
        self.GBuffer = G_Buffer([size[0], size[1]])

        _set_window_properties(size[0], size[1])
        self.lightAmount = 1

    def resize(self, w, h):
        glViewport(0, 0, get_window_width(), get_window_height())

        self.currScene.get_current_camera().update_pMatrix(w/h)
        self.lightBuffer.resize(w, h)
        self.GBuffer.resize(w, h)
        self.width = w
        self.height = h
        _set_window_properties(w, h)

        clear_framebuffer([0, 0, 0, 1])

    def forward(self):
        clear_framebuffer([0,1,0,1])

        glUseProgram(self.forwardProgram)
        light_num_slot = glGetUniformLocation(self.forwardProgram, "lightnum")
        if light_num_slot > 0:
            glUniform1i(light_num_slot,  self.lightAmount)
        self.draw()

        glFlush()

        fps_update(self.height, self)

    def deferred_render(self):
        glUseProgram(self.deferred_program)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

        glDisable(GL_BLEND)
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        self.GBuffer.bind()


        self.draw()

        self.GBuffer.unbind()

        glUseProgram(self.lightProgram)
        light_num_slot = glGetUniformLocation(self.lightProgram, "lightnum")
        if light_num_slot > 0:
            glUniform1i(light_num_slot,  self.lightAmount)
        self.light_draw()

        glFlush()

        fps_update(renderer=self)

    def deferred_lightPass_render(self):
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        glUseProgram(self.deferred_program)
        clear_framebuffer([0,0,0,1])

        self.GBuffer.bind()
        self.draw()
        self.GBuffer.unbind()


        self._instance_light_draw(self.lightSphere)
        #blit_to_default(self.lightBuffer, 0)

        glFlush()

        fps_update( renderer=self)

    def draw(self):
        _set_cam_attributes(self.currScene.get_current_camera())

        for obj in self.currScene.get_entity_list():
            _set_obj_mat_attributes(obj)
            _set_normalMatrix_attribute(obj)
            _set_obj_transform_attributes(obj)
            obj.draw()

    def _instance_light_draw(self, parentObj):
        glUseProgram(self.lightSphereShader)
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_FRONT)
        glDepthFunc(GL_ALWAYS)

        self.lightBuffer.bind()
        _set_cam_attributes(self.currScene.get_current_camera())

        light_num_slot = glGetUniformLocation(self.lightSphereShader, "lightnum")
        if light_num_slot > 0:
            glUniform1i(light_num_slot, self.lightAmount)

        loc1 = glGetUniformLocation(self.lightSphereShader, "geoPosRender")
        glUniform1i(loc1, self.GBuffer.position_tex.slot)
        loc2 = glGetUniformLocation(self.lightSphereShader, "geoNormRender")
        glUniform1i(loc2, self.GBuffer.normal_tex.slot)

        glBindVertexArray(parentObj.VAO)
        glDrawElementsInstanced(parentObj.renderType, len(parentObj.indices), GL_UNSIGNED_SHORT, None, self.lightAmount)
        self.lightBuffer.unbind()

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthFunc(GL_LESS)
        glCullFace(GL_BACK)

    def light_draw_cubes(self, buffer: G_Buffer):
        currProgram = glGetIntegerv(GL_CURRENT_PROGRAM)
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


    def light_draw(self):
        currProgram = glGetIntegerv(GL_CURRENT_PROGRAM)
        cam = self.currScene.get_current_camera()
        texture.bind(self.GBuffer.position_tex)
        texture.bind(self.GBuffer.normal_tex)
        texture.bind(self.GBuffer.albedo_tex)

        loc1 = glGetUniformLocation(currProgram, "pos")
        glUniform1i(loc1, self.GBuffer.position_tex.slot)
        loc2 = glGetUniformLocation(currProgram, "norm")
        glUniform1i(loc2, self.GBuffer.normal_tex.slot)
        loc3 = glGetUniformLocation(currProgram, "albedo")
        glUniform1i(loc3, self.GBuffer.albedo_tex.slot)
        v_loc = glGetUniformLocation(currProgram, "viewPos")
        glUniform3fv(v_loc, 1, flatten(cam.eye))
        glUniformMatrix4fv(glGetUniformLocation(currProgram, "obj_transform"), 1, False,
                           flatten(self.quad.getTransform()))

        self.quad.draw()


def _set_cam_attributes(cam):
    if cam:
        program = glGetIntegerv(GL_CURRENT_PROGRAM)
        p_loc = glGetUniformLocation(program, "projection")
        v_loc = glGetUniformLocation(program, "v_matrix")
        if p_loc != -1:
            glUniformMatrix4fv(p_loc, 1, False, cam.pMatrix)
        if v_loc != -1:
            glUniformMatrix4fv(v_loc, 1, False, flatten(cam._getTransform()), False)



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
