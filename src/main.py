import math
import time
from collections import OrderedDict

import numpy
from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image, ImageOps

from opengl_interfacing.animator import Animator, Animation, KeyFrame
from opengl_interfacing.camera import Camera
from opengl_interfacing.framebuffer import G_Buffer
from opengl_interfacing.initshader import initShaders
from opengl_interfacing.renderer import ImagePlane, Renderer, Cube
from utils.objects import Joint, Animated_model

width, height = 200, 200
aspectRatio = width / height
program = None
postProgram = None
window = None

global renderer
global t2
global blit
global target
global count, cube, animator
count = 0


def update_persp_event(w, h):
    global renderer, buffer, cam
    glViewport(0, 0, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    cam.update_pMatrix()
    buffer.resize(w, h)

    clear_framebuffer()


def buttons(key, x, y):
    pass  # print(key, x, y)


def on_click(button, state, x, y):
    global cam, dragx_start, dragy_start
    if button == 0:
        if state == 0:
            dragx_start = x
            dragy_start = y

    if button == 3:
        cam.adjustDistance(-0.1)
    elif button == 4:
        cam.adjustDistance(0.1)
        # scrool backward


def mouseControl(mx, my):
    global cam, dragx_start, dragy_start
    ratio = glutGet(GLUT_WINDOW_WIDTH) / glutGet(GLUT_WINDOW_HEIGHT)

    deltax = ((mx - dragx_start) * ratio) / glutGet(GLUT_WINDOW_WIDTH)
    deltay = (my - dragy_start) / glutGet(GLUT_WINDOW_HEIGHT)

    cam.updateHorizontal(-deltax * 100)
    cam.updateVertical(-deltay * 100)

    dragx_start = mx
    dragy_start = my


def init():
    global start_time
    global fps_counter

    global renderer, cube, program, lightProgram, jointProgram, animator, time_per_frame
    global blit
    global target
    global buffer, bbj, joint, joint2
    time_per_frame = 0
    fps_counter = 0
    start_time = time.time()

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow("Opengl Window In Python")

    glutReshapeFunc(update_persp_event)
    GL.glLineWidth(1)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

    GL.glEnable(GL.GL_BLEND)
    glEnable(GL_DEPTH_TEST)

    glDisable(GL_CULL_FACE)
    glutDisplayFunc(render)
    glutIdleFunc(render)

    program = initShaders("/shader/defered/defered_v_shader.glsl", "/shader/defered/defered_f_shader.glsl")
    lightProgram = initShaders("/shader/defered/defered_light_v_shader.glsl",
                               "/shader/defered/defered_light_f_shader.glsl")
    jointProgram = initShaders("/shader/debug/joint_v_shader.glsl", "/shader/debug/joint_f_shader.glsl")
    glUseProgram(program)

    cube = Cube()
    # cube.set_position([0.5, 0.3, -2])
    # cube.set_rotation([30, 0, 45])

    cube2 = Cube()
    # cube2.set_position([-0.5, 0, -2])

    t = ImagePlane("/res/images/box.png")
    t.set_position([0.5, 0, -1])
    t.set_rotation([0, 135, 0])

    t2 = ImagePlane("/res/images/box.png")
    t2.set_position([-0.5, 0, -1])
    t2.set_rotation([0, -135, 0])

    buffer = G_Buffer([width, height])

    glutKeyboardFunc(buttons)
    glutMotionFunc(mouseControl)
    glutMouseFunc(on_click)

    cube.material.set_tex_diffuse(t.get_material().tex_diffuse)

    global cam
    cam = Camera()

    cube.set_position([1, 0, 0])
    renderer = Renderer()
    renderer.objects = [cube]

    glutMainLoop()


def save_current_framebuffer_as_png(bufferid):
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    GL.glBindFramebuffer(GL_READ_FRAMEBUFFER, bufferid)
    data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGBA", (width, height), data)
    image = ImageOps.flip(image)  # in my case image is flipped top-bottom for some reason
    image.save('glutout.png', 'PNG')
    GL.glBindFramebuffer(GL_FRAMEBUFFER, 0)


def fps_update():
    global fps_counter
    global start_time
    global time_per_frame
    tim = (time.time() - start_time)

    if tim != 0:
        time_per_frame = tim
        # print("FPS: ", 1 / tim)


def clear_framebuffer():
    glClearColor(0.0, 1.0, 1, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


def render():
    global renderer, buffer, program, lightProgram, cube, bbj, joint, joint2, start_time, cam
    start_time = time.time()

    buffer.bind()
    glUseProgram(program)
    renderer.draw(cam)

    buffer.unbind()

    glUseProgram(lightProgram)
    renderer.light_draw(buffer)

    glFlush()

    fps_update()


init()
