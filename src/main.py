import numpy
from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.raw.GL.NV.multisample_filter_hint import GL_MULTISAMPLE_FILTER_HINT_NV
from OpenGL.raw.GLU import gluPerspective
from PIL import Image, ImageOps
import time

from opengl_interfacing.framebuffer import FrameBuffer, FrameBuffer_Tex_MS, FrameBuffer_blit_MS, FrameBuffer_target_MS, \
    blit_to_default, G_Buffer
from opengl_interfacing.initshader import initShaders
from opengl_interfacing.renderer import ImagePlane, Renderer, Plane, Cube
from opengl_interfacing.texture import bind
from utils.objectUtils import flatten, Matrix, ortho, perspective, transpose

width, height = 800, 800
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
    buffer.resize(w,h)
    clear_framebuffer()


def init():
    global start_time
    global fps_counter

    global renderer, cube
    global blit
    global target

    fps_counter = 0
    start_time = time.time()

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow("Opengl Window In Python")

    glutReshapeFunc(update_persp_event)

    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    GL.glEnable(GL.GL_CULL_FACE)
    GL.glEnable(GL.GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glDepthRange(0.1, 100)


    glEnable(GL_MULTISAMPLE)

    glutDisplayFunc(render)
    glutIdleFunc(render)

    program = initShaders("/shader/vertex-shader.glsl", "/shader/fragment-shader.glsl")
    program = initShaders("/shader/defered_v_shader.glsl", "/shader/defered_f_shader.glsl")
    # light_program = initShaders("/shader/defered_v_shader.glsl", "/shader/defered_f_shader.glsl")

    glUseProgram(program)

    quad = Plane(plane=[[1, 1, 0],
                        [1, -1, 0],
                        [-1, 1, 0],
                        [-1, -1, 0],
                        [-1, 1, 0],
                        [1, -1, 0],
                        ])
    cube = Cube()
    cube.set_position([0, -1, -1])
    cube.set_rotation([-45, 0, 0])

    t = ImagePlane("/res/images/body_05.png")
    t.set_position([0.5, 0, -1])
    t.set_rotation([135, 0, 0])

    t2 = ImagePlane("/res/images/body_05.png")
    t2.set_position([-0.5, 0, -1])
    t2.set_rotation([-135, 0, 0])

    renderer = Renderer(program, [t, cube, t2])

    global buffer
    buffer = G_Buffer([width, height])
    buffer.bind()
    glutMainLoop()


def save_current_framebuffer_as_png(bufferid):
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    GL.glBindFramebuffer(GL_READ_FRAMEBUFFER, bufferid)
    data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGBA", (width, height), data)
    image = ImageOps.flip(image)  # in my case image is flipped top-bottom for some reason
    image.save('glutout.png', 'PNG')


def fps_update():
    global fps_counter
    global start_time
    global time_per_frame

    if (time.time() - start_time) > 1:
        time_per_frame = 1 / fps_counter / (time.time() - start_time)
        print("FPS: ", fps_counter / (time.time() - start_time))
        fps_counter = 0
        start_time = time.time()

    fps_counter += 1


def clear_framebuffer():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)



def render():
    global renderer, buffer

    clear_framebuffer()
    renderer.draw()

    blit_to_default(buffer)
    glFlush()
    fps_update()


init()
