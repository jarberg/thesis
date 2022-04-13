import time

from OpenGL import GL
from OpenGL.GLUT import glutInit, GLUT_RGBA, GLUT_DEPTH, GLUT_WINDOW_WIDTH, GLUT_WINDOW_HEIGHT
from OpenGL.GLUT import glutInitDisplayMode, glutInitWindowSize, glutInitWindowPosition, glutCreateWindow, \
    glutReshapeFunc, glutDisplayFunc, glutIdleFunc, glutMainLoop, glutGet
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_DEPTH_TEST, glEnable, glDisable, GL_CULL_FACE, glFlush, glViewport
from OpenGL.raw.GL.VERSION.GL_2_0 import glUseProgram

from opengl_interfacing.framebuffer import G_Buffer, clear_framebuffer, blit_to_default
from opengl_interfacing.initshader import initShaders
from opengl_interfacing.renderer import Renderer
from opengl_interfacing.texture import createNewTexture
from utils.objects import Cube, Plane
from utils.scene import Scene

width, height = 200, 200
aspectRatio = width / height
program = None
postProgram = None
window = None

global renderer


def update_persp_event(w, h):
    global renderer, buffer, currScene
    glViewport(0, 0, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    currScene.get_current_camera().update_pMatrix()
    buffer.resize(w, h)

    clear_framebuffer([0,0,1,1])


def set_up_scene_entities(scene):

    p = Plane()
    p.set_position([2, 0, 0.5])
    p.set_rotation([0, 0, 90])
    p.set_scale([1000, 1000, 1000])
    cube = Cube()
    cube.set_position([0,0.5,0])
    cube.material.set_tex_diffuse(createNewTexture("/res/images/box.png"))

    cube2 = Cube()
    cube2.set_position([0, 0.5, 1])
    scene.add_entities([cube, p])


def init():
    global start_time
    global fps_counter

    global renderer, program, lightProgram, buffer, currScene

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
    glUseProgram(program)


    buffer = G_Buffer([width, height])

    currScene = Scene()

    set_up_scene_entities(currScene)

    renderer = Renderer(currScene)

    glutMainLoop()


def fps_update():
    global fps_counter
    global start_time
    global time_per_frame
    tim = (time.time() - start_time)

    if tim != 0:
        time_per_frame = tim
        print("FPS: ", 1 / tim)


def render():
    global renderer, buffer, program, lightProgram, cube, bbj, joint, joint2, start_time, cam
    start_time = time.time()

    buffer.bind()
    glUseProgram(program)
    renderer.draw()
    buffer.unbind()


    glUseProgram(lightProgram)
    renderer.light_draw(buffer)

    glFlush()

    fps_update()


init()
