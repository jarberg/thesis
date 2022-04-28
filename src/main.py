import math

from OpenGL.GLUT import glutInit, GLUT_RGBA, GLUT_DEPTH
from OpenGL.GLUT import glutInitDisplayMode, glutInitWindowSize, glutInitWindowPosition, glutCreateWindow, \
    glutReshapeFunc, glutDisplayFunc, glutIdleFunc, glutMainLoop

from opengl_interfacing.buffer import ShaderStorageBufferObject
from opengl_interfacing.renderer import Renderer
from opengl_interfacing.sceneObjects import Plane, Cube
from opengl_interfacing.texture import createNewTexture
from utils.objects import Transform, PointLight, Attenuation
from utils.scene import Scene

width, height = 1200, 1200
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

    glutReshapeFunc(renderer.resize)
    glutDisplayFunc(renderer.forward)
    glutIdleFunc(renderer.forward)

    set_up_scene_entities(currScene, renderer)

    reset_test_file()
    renderer.resize(width, height)

    glutMainLoop()



def reset_test_file():
    file2 = open(r"test_{}.txt".format(height), "w+")
    file2.close()


def set_up_scene_entities(scene, renderer):
    p = Plane()
    p.set_rotation([0, 0, 90])
    p.set_scale([1000, 1000, 1000])

    cubelist = cubes(0)
    cubelist.append(p)

    scene.add_entities(cubelist)
    lightlist = lights(100)

    renderer.lightAmount = 0
    scene.add_lights(lightlist)

    ssbo = ShaderStorageBufferObject(bufferIndex=3)
    ssbo.add_data(lightlist)

    cam = scene.get_current_camera()
    cam.radius = 800
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
