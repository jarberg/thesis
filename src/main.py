from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image, ImageOps
import time

from opengl_interfacing.framebuffer import FrameBuffer
from opengl_interfacing.initshader import initShaders

width, height = 800, 800
aspectRatio = width / height
program = None
window = None
global count
count = 0


def init():
    global start_time
    global fps_counter
    fps_counter = 0
    start_time = time.time()

    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow("Opengl Window In Python")

    global Fbo
    Fbo = FrameBuffer(50, 50)

    glutDisplayFunc(render)
    glutIdleFunc(render)

    program = initShaders("src/shader/vertex-shader.glsl", "src/shader/fragment-shader.glsl")
    glUseProgram(program)
    glutMainLoop()

    glUniform1f(glGetUniformLocation(program, "test.position"), [1, 1, 1])

def save_current_framebuffer_as_png():
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, Fbo.width, Fbo.height, GL_RGBA, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGBA", (Fbo.width, Fbo.height), data)
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


def render():
    global count

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1.0, 0.0, 0.0, 1.0)

    Fbo.bind(3)
    glutSolidTeapot(0.5)
    Fbo.unbind()


    fps_update()


init()
