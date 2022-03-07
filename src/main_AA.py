import numpy
from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.raw.GLU import gluPerspective
from PIL import Image, ImageOps
import time

from opengl_interfacing.framebuffer import FrameBuffer, FrameBuffer_Tex_MS, FrameBuffer_blit_MS, FrameBuffer_target_MS, \
    blit_to_default
from opengl_interfacing.initshader import initShaders
from opengl_interfacing.renderer import ImagePlane, Renderer, Plane
from opengl_interfacing.texture import bind
from utils.objectUtils import flatten, Matrix, ortho, perspective, transpose

width, height = 800, 800
aspectRatio = width / height
program = None
postProgram = None
window = None
count = 0

global renderer
global t2
global blit
global target


def update_persp_event(w, h):
    global renderer
    glViewport(0, 0, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    renderer.persp = flatten(perspective(90, glutGet(GLUT_WINDOW_WIDTH) / glutGet(GLUT_WINDOW_HEIGHT), 0, 100))


def init():
    global start_time
    global fps_counter
    global post
    global program
    global postProgram
    global t
    global t2
    global renderer
    global blit
    global target
    global quad
    fps_counter = 0
    start_time = time.time()

    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow("Opengl Window In Python")

    glutReshapeFunc(update_persp_event)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    GL.glEnable(GL.GL_BLEND)

    glDisable(GL_CULL_FACE)


    #glEnable(GL_TEXTURE_2D)
    glEnable(GL_MULTISAMPLE)

    blit = FrameBuffer_blit_MS(width, height)
    target = FrameBuffer_target_MS(width, height)
    post = FrameBuffer_Tex_MS(width, height)

    glutDisplayFunc(render)
    glutIdleFunc(render)

    program = initShaders("/shader/vertex-shader.glsl", "/shader/fragment-shader.glsl")
    postProgram = initShaders("/shader/aa_v_shader.glsl", "/shader/aa_f_shader.glsl")

    glUseProgram(program)

    quad = Plane(plane= [[1, 1, 0],
                 [1, -1, 0],
                 [-1, 1, 0],
                 [-1, -1, 0],
                 [-1, 1, 0],
                 [1, -1, 0],
                 ])
    quad.set_rotation([0, 180, 0])
    t = ImagePlane("/res/images/body_05.png")
    t.set_position([0.5, 0, -1])
    t.set_scale([-1, 1, 1])
    t.set_rotation([-45, 0, 0])
    t2 = ImagePlane("/res/images/body_05.png")
    t2.set_position([-0.5, 0, -1])
    t2.set_rotation([45, 0, 0])


    renderer = Renderer(program, [t, t2])

    post.bind()


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
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.3, 0.3, 0.0, 1.0)



def render():
    global program
    global postProgram
    global renderer
    global post
    global quad
    global blit
    global target

    clear_framebuffer()

    renderer.draw()
    renderer.postDraw([quad], postProgram, post.texture)
    blit_to_default(post)

    glFlush()
    fps_update()


init()
