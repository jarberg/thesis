import time

from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image, ImageOps

from opengl_interfacing.framebuffer import FrameBuffer_Tex_MS, blit_to_default
from opengl_interfacing.initshader import initShaders
from opengl_interfacing.renderer import ImagePlane, Renderer, Plane, Cube
from utils.objectUtils import flatten, perspective

width, height = 400, 400
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
    renderer.persp = flatten(perspective(90, glutGet(GLUT_WINDOW_WIDTH) / glutGet(GLUT_WINDOW_HEIGHT), 0.1, 100))


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
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)

    glutInitWindowSize(width, height)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow("Opengl Window In Python")

    glutReshapeFunc(update_persp_event)

    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    GL.glEnable(GL.GL_BLEND)

    glEnable(GL_DEPTH_TEST)
    glDepthRange(0.1, 100)

    glEnable(GL_MULTISAMPLE)

    post = FrameBuffer_Tex_MS(width, height)
    #glHint(GL_MULTISAMPLE_FILTER_HINT_NV, GL_NICEST)

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

    cube = Cube()
    cube.set_position([1, -1, -4])
    renderer = Renderer([t, cube, t2])

    #post.bind()

    glutDisplayFunc(render)
    glutIdleFunc(render)
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
    tim = (time.time() - start_time)
    if (time.time() - start_time) > 1 and fps_counter*tim != 0:
        time_per_frame = 1 / fps_counter * tim
        print("FPS: ", fps_counter / (time.time() - start_time))
        fps_counter = 0
        start_time = time.time()

    fps_counter += 1

def clear_framebuffer():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.3, 0.1, 0.0, 1.0)



def render():
    global program
    global postProgram
    global renderer
    global post
    global quad

    post.bind()
    clear_framebuffer()
    glUseProgram(program)
    renderer.draw()
    renderer.postDraw([quad], postProgram, post.texture)
    blit_to_default(post)

    glFlush()
    fps_update()


init()
