import numpy
from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image, ImageOps
import time

from opengl_interfacing.framebuffer import FrameBuffer
from opengl_interfacing.initshader import initShaders
from opengl_interfacing.renderer import ImagePlane
from opengl_interfacing.texture import bind
from utils.objectUtils import flatten, Matrix, ortho, perspective

width, height = 800, 800
aspectRatio = width / height
program = None
window = None

count = 0


def init():
    global start_time
    global fps_counter
    global Fbo
    global program
    global t

    fps_counter = 0
    start_time = time.time()

    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow("Opengl Window In Python")

    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    GL.glEnable(GL.GL_BLEND)
    glDisable(GL_CULL_FACE)
    Fbo = FrameBuffer(50, 50)

    glEnable(GL_TEXTURE_2D)

    glutDisplayFunc(render)
    glutIdleFunc(render)

    program = initShaders("/shader/vertex-shader.glsl", "/shader/fragment-shader.glsl")
    glUseProgram(program)

    t = ImagePlane("/res/images/body_05.png", program)

    glBindBuffer(GL_ARRAY_BUFFER, t.vBuffer)
    glBufferData(GL_ARRAY_BUFFER, flatten(t.vertexArray).nbytes, flatten(t.vertexArray), GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, t.cBuffer)
    glBufferData(GL_ARRAY_BUFFER, flatten(t.coordArray).nbytes, flatten(t.coordArray), GL_STATIC_DRAW)

    glVertexAttribPointer(1, 2, GL_FLOAT, False, 0, None)
    glEnableVertexAttribArray(1)

    glutMainLoop()


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
    global program
    global t

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.3, 0.3, 0.0, 1.0)

    loc = glGetUniformLocation(program, "tex_diffuse")
    slot = t.texture.slot
    glUniform1i(loc, slot)

    # rot = t.get_rotation()
    # t.set_rotation([rot[0]+0.001,rot[1]+0,rot[2]+0])

    trans = flatten(t.getTransform())
    persp  =flatten(perspective(90, 1, 0 , 100))
    glUniformMatrix4fv(glGetUniformLocation(program, "projection"), 1, False, persp)
    # glUniformMatrix4fv(glGetUniformLocation(program, "obj_transform"), 1, False, trans)

    glDrawArrays(GL_TRIANGLES, 0, len(t.vertexArray))
    glDrawArrays(GL_TRIANGLES, 0, len(t.vertexArray))

    glFlush()
    fps_update()

    # global t
    # bind(t.texture)

    # glBindBuffer(GL_ARRAY_BUFFER, t.vBuffer)
    # glDrawArrays(GL_TRIANGLES, 0, 3*len(t.vertexArray))


init()
