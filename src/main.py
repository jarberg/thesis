import math

from OpenGL import GL
import time

from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image, ImageOps

from opengl_interfacing.framebuffer import G_Buffer, blit_to_default
from opengl_interfacing.initshader import initShaders
from opengl_interfacing.renderer import ImagePlane, Renderer, Cube, Bigbrainjoints
from utils.objectUtils import flatten, perspective, euler_to_quaternion, quat_2_euler, degrees
from utils.objects import Transform, Joint

width, height = 200, 200
aspectRatio = width / height
program = None
postProgram = None
window = None

global renderer
global t2
global blit
global target
global count, cube
count = 0


def update_persp_event(w, h):
    global renderer, buffer
    glViewport(0, 0, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    renderer.persp = flatten(perspective(90, glutGet(GLUT_WINDOW_WIDTH) / glutGet(GLUT_WINDOW_HEIGHT), 0.1, 100))
    # buffer.resize(w, h)
    clear_framebuffer()


def init():
    global start_time
    global fps_counter

    global renderer, cube, program, lightProgram, jointProgram
    global blit
    global target

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
    GL.glEnable(GL.GL_CULL_FACE)
    GL.glEnable(GL.GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    glutDisplayFunc(render)
    glutIdleFunc(render)

    program = initShaders("/shader/defered_v_shader.glsl", "/shader/defered_f_shader.glsl")
    lightProgram = initShaders("/shader/defered_light_v_shader.glsl", "/shader/defered_light_f_shader.glsl")
    jointProgram = initShaders("/shader/joint_v_shader.glsl", "/shader/joint_f_shader.glsl")
    glUseProgram(program)

    cube = Cube()
    cube.set_position([0, -1, -1])
    cube.set_rotation([-45, 0, 0])

    cube2 = Cube()
    cube2.set_position([0, 0, -10])
    cube2.set_rotation([-45, 0, 0])

    t = ImagePlane("/res/images/body_05.png")
    t.set_position([0.5, 0, -1])
    t.set_rotation([135, 0, 0])

    t2 = ImagePlane("/res/images/body_05.png")
    t2.set_position([-0.5, 0, -1])
    t2.set_rotation([-135, 0, 0])

    renderer = Renderer()
    renderer.objects = [t, cube, cube2, t2]

    global buffer, bbj, joint, joint2
    buffer = G_Buffer([width, height])

    t = Transform()
    t.set_position([0, 1, 0])

    joint = Joint()
    joint2 = Joint(parent=joint)
    joint.set_position([0, 0, -1.5])
    joint.set_rotation([0, 0, 88])

    joint2.set_position([0.5, 0, 0])
    joint2.set_rotation([0, 0, -45])

    joint.set_bind_transform(t)

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

    if (time.time() - start_time) > 1:
        tim = (time.time() - start_time)
        if tim == 0:
            return
        time_per_frame = 1 / tim
        print("FPS: ", fps_counter / (time.time() - start_time))
        fps_counter = 0
        start_time = time.time()

    fps_counter += 1


def clear_framebuffer():
    glClearColor(0.0, 1.0, 1, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


def render():
    global renderer, buffer, program, lightProgram, cube, bbj, joint, joint2

    buffer.bind()
    glUseProgram(program)
    # renderer.draw()
    buffer.unbind()
    rot = joint.get_rotation()
    rot2 = joint2.get_rotation()
    joint.set_rotation([0, 0, rot[2] + 0.1])
    joint2.set_rotation([0, 0, -rot[2]])

    glUseProgram(jointProgram)
    renderer.joint_draw([joint, joint2])

    # glUseProgram(lightProgram)
    # renderer.light_draw(buffer)
    glFlush()

    fps_update()


init()

