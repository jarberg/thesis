import math

from OpenGL.GLUT import glutInit, GLUT_RGBA, GLUT_DEPTH
from OpenGL.GLUT import glutInitDisplayMode, glutInitWindowSize, glutInitWindowPosition, glutCreateWindow, \
    glutReshapeFunc, glutDisplayFunc, glutIdleFunc, glutMainLoop
from OpenGL.raw.GL.VERSION.GL_1_0 import glDepthFunc, GL_LESS, GL_DEPTH_TEST, glEnable
from OpenGL.raw.GL.VERSION.GL_2_0 import glUseProgram

from opengl_interfacing.buffer import ShaderStorageBufferObject
from opengl_interfacing.renderer import Renderer, set_window_properties
from opengl_interfacing.sceneObjects import Plane, Cube
from opengl_interfacing.texture import createNewTexture
from utils.objects import Transform, PointLight, Attenuation
from utils.scene import Scene

width, height = 400, 400
aspectRatio = width / height
window = None

global renderer


def init():

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow("Opengl Window In Python")

    currScene = Scene()
    renderer = Renderer(currScene, [width, height])
    set_render_type(renderer, 1)

    glutReshapeFunc(renderer.resize)

    set_up_scene_entities(currScene, renderer, boxes=0, lightsnum=1)

    #reset_test_file()
    renderer.resize(width, height)

    glutMainLoop()


def set_render_type(renderer, type=0):
    if type==0:
        glutDisplayFunc(renderer.forward)
        glutIdleFunc(renderer.forward)
        glUseProgram(renderer.forwardProgram)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

    elif type==1:
        glutDisplayFunc(renderer.deferred_render)
        glutIdleFunc(renderer.deferred_render)
        glUseProgram(renderer.deferred_program)
    elif type==2:
        glutDisplayFunc(renderer.deferred_lightPass_render)
        glutIdleFunc(renderer.deferred_lightPass_render)
        glUseProgram(renderer.deferred_program)

    renderer.add_renderObjectUtils()
    set_window_properties(width, height)

def reset_test_file():
    file2 = open(r"test_{}.txt".format(height), "w+")
    file2.close()


def set_up_scene_entities(scene, renderer, boxes=0, lightsnum=1):
    p = Plane()
    p.set_rotation([0, 0, 90])
    p.set_scale([1000, 1000, 1000])

    cubelist = cubes(boxes)
    cubelist.append(p)

    scene.add_entities(cubelist)
    lightlist = lights(lightsnum)


    scene.add_lights(lightlist)
    renderer.lightAmount = len(lightlist)

    ssbo = ShaderStorageBufferObject(bufferIndex=3)
    ssbo.add_data(lightlist)

    cam = scene.get_current_camera()
    cam.radius = 20
    cam.updateHorizontal(0)
    cam.updateVertical(89.5)


def cubes(amount):
    cubelist = []
    tex = createNewTexture("/res/images/box.png")
    a = min((math.sqrt(amount / 2) * 4 + 1), 7)
    for i in range(-amount, amount + 1):
        for j in range(-amount, amount + 1):
            c = Cube()
            c.set_position([i * a, 0.5, j * a])
            c.material.set_tex_diffuse(tex)
            cubelist.append(c)
    return cubelist


def lights(amount):
    lightlist = []

    light = PointLight(intensity=50, attenuation=Attenuation(const=1, linear=3, exp=50))

    r = light.radius
    a = min((math.sqrt(amount / 2) * 4 + 1), 7)

    for i in range(-amount, amount + 1):
        for j in range(-amount, amount + 1):
            temp = Transform()
            temp.set_position([i * a, 2, j * a, 1])
            temp.set_scale([r, r, r])
            lightlist.append(temp)
    return lightlist


init()
