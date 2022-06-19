import math
import sys

from OpenGL.GLUT import glutInit, GLUT_RGBA, GLUT_DEPTH
from OpenGL.GLUT import glutInitDisplayMode, glutInitWindowSize, glutInitWindowPosition, glutCreateWindow, \
    glutReshapeFunc, glutDisplayFunc, glutIdleFunc, glutMainLoop
from OpenGL.raw.GL.VERSION.GL_1_0 import glDepthFunc, GL_LESS, GL_DEPTH_TEST, glEnable
from OpenGL.raw.GL.VERSION.GL_2_0 import glUseProgram

from opengl_interfacing.buffer import ShaderStorageBufferObject
from opengl_interfacing.renderer import Renderer, set_window_properties
from opengl_interfacing.sceneObjects import Plane, Cube
from opengl_interfacing.texture import createNewTexture

from utils.objectUtils import flatten_list
from utils.objects import Transform, PointLight, Attenuation
from utils.scene import Scene

width, height = 400, 400
aspectRatio = width / height
window = None

global renderer

def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

def print_render_type(enum):
    if enum ==0:
        print("Forward rendering")
    if enum ==1:
        print("deferred rendering")
    if enum ==2:
        print("deferred rendering with light volumes")
    if enum ==3:
        print("deferred rendering with batched light volumes")

def init(*args, **kwargs):
    global width, height, aspectRatio
    argdict = Convert(args[0])
    render_type = int(argdict.get("-render", 2))
    cubes = int(argdict.get("-cubes", 0))
    lights = int(argdict.get("-lights", 10))

    resolution = int(argdict.get("-res", 400))

    print_render_type(render_type)

    width, height = resolution, resolution
    aspectRatio = width / height

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow("Opengl Window In Python")

    currScene = Scene()
    renderer = Renderer(currScene, [width, height])
    set_render_type(renderer, render_type)

    glutReshapeFunc(renderer.resize)

    set_up_scene_entities(currScene, renderer, boxes=cubes, lightsnum=lights)

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

    elif type==3:
        glutDisplayFunc(renderer.deferred_lightPass_instance_render)
        glutIdleFunc(renderer.deferred_lightPass_instance_render)
        glUseProgram(renderer.deferred_program)

    renderer.add_renderObjectUtils()
    set_window_properties(width, height)


def reset_test_file():
    file2 = open(r"test_{}.txt".format(height), "w+")
    file2.close()


def set_up_scene_entities(scene, renderer, boxes=0, lightsnum=1):
    p = Plane()
    p.set_rotation([0, 0, 90])
    p.set_scale([10000, 10000, 10000])

    cubelist = cubes(boxes)
    cubelist.append(p)

    scene.add_entities(cubelist)
    lightlist = lights(lightsnum)

    scene.add_lights(lightlist)
    renderer.lightAmount = len(lightlist)

    ssbo = ShaderStorageBufferObject(bufferIndex=3)
    ssbo.add_data(flatten_list(lightlist))
    ssbo.bind()

    cam = scene.get_current_camera()
    cam.radius = 10
    cam.set_position([0, 0, 0])
    cam.updateHorizontal(0)
    cam.updateVertical(50)


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


if __name__ == "__main__" :
    init(sys.argv[1:])
