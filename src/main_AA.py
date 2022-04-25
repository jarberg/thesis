import time

from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image, ImageOps

from opengl_interfacing.camera import Camera
from opengl_interfacing.framebuffer import FrameBuffer_Tex_MS
from opengl_interfacing.initshader import initShaders
from opengl_interfacing.renderer import Renderer
from utils.objects import ImagePlane, Cube
from utils.scene import Scene

width, height = 400, 400
aspectRatio = width / height
deferred_program = None
postProgram = None
window = None
count = 0

global renderer
global t2
global blit
global target


def update_persp_event(w, h):
    global renderer, post, currScene
    glViewport(0, 0, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    cam = currScene.get_current_camera()
    cam.update_pMatrix()
    post.resize(w,  h)

def init():
    global start_time, program
    global fps_counter
    global post
    global deferred_program
    global postProgram
    global t
    global t2
    global renderer
    global blit
    global target
    global quad


    global currScene


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

    post = FrameBuffer_Tex_MS(width, height, 0)

    program = initShaders("/shader/vertex-shader.glsl", "/shader/fragment-shader.glsl")
    postProgram = initShaders("/shader/antiAlias/aa_v_shader.glsl", "/shader/antiAlias/aa_f_shader.glsl")

    glUseProgram(program)
    global cam
    cam = Camera()
    t = ImagePlane("/res/images/body_05.png")
    t.set_position([0.5, 0, -1])
    t.set_scale([-1, 1, 1])
    t.set_rotation([-45, 0, 0])
    t2 = ImagePlane("/res/images/box.png")
    t2.set_position([-0.5, 0, -1])
    t2.set_rotation([45, 0, 0])

    cube = Cube()
    cube.material.tex_diffuse_b = False
    cube.set_position([1, -1, 0])
    cube.set_scale([0.5,0.5,0.5])

    currScene = Scene()
    currScene.add_entities([t, cube, t2])
    currScene.inputMan.set_plusminus_callback(set_samples)
    renderer = Renderer(currScene)

    glutDisplayFunc(render)
    glutIdleFunc(render)
    glutMainLoop()

def set_samples(samples):
    global post
    post.set_samples(samples)
    post.resize()



def fps_update():
    global fps_counter
    global start_time
    global time_per_frame
    tim = (time.time() - start_time)
    if (time.time() - start_time) > 1 and fps_counter*tim != 0:
        time_per_frame = 1 / fps_counter * tim
        #("FPS: ", fps_counter / (time.time() - start_time))
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
    global quad, gsamples

    post.bind()

    clear_framebuffer()
    glUseProgram(program)
    renderer.draw()



    post.unbind()
    renderer.postDraw(postProgram, post.texture, post)
    glFlush()
    fps_update()

init()
