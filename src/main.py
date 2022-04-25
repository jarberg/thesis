import math
import time

from OpenGL import GL
from OpenGL.GL import GL_PACK_ALIGNMENT, GL_READ_FRAMEBUFFER, glPixelStorei, \
    glReadPixels, GL_RGBA16F, GL_FLOAT, glGenBuffers, \
    GL_SHADER_STORAGE_BUFFER, glBindBuffer, glBindBufferBase, glBufferData, GL_STATIC_DRAW, glGetUniformLocation, \
    glUniform1i
from OpenGL.GLUT import glutInit, GLUT_RGBA, GLUT_DEPTH, GLUT_WINDOW_WIDTH, GLUT_WINDOW_HEIGHT
from OpenGL.GLUT import glutInitDisplayMode, glutInitWindowSize, glutInitWindowPosition, glutCreateWindow, \
    glutReshapeFunc, glutDisplayFunc, glutIdleFunc, glutMainLoop, glutGet
from OpenGL.raw.GL.VERSION.GL_1_0 import glFlush, glViewport
from OpenGL.raw.GL.VERSION.GL_2_0 import glUseProgram
from PIL import Image, ImageOps

from opengl_interfacing.framebuffer import clear_framebuffer
from opengl_interfacing.renderer import Renderer
from opengl_interfacing.texture import createNewTexture
from utils.objectUtils import flatten, flatten_list, get_pointLight_radius
from utils.objects import Cube, Plane, Transform, PointLight, Attenuation
from utils.scene import Scene

width, height = 1200, 1200
aspectRatio = width / height
deferred_program = None
postProgram = None
window = None

global renderer


def init():
    global start_time, fps_counter, counter, lightcount, lightssob
    global renderer, deferred_program, lightProgram, buffer, currScene, av_start_time, height
    counter = 0
    lightcount = 0
    start_time = time.time()
    av_start_time = start_time
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow("Opengl Window In Python")

    glutReshapeFunc(update_persp_event)

    glutDisplayFunc(render)
    glutIdleFunc(render)

    currScene = Scene()
    renderer = Renderer(currScene)
    glUseProgram(renderer.deferred_program)
    set_up_scene_entities(currScene)

    lightlist = lights(0)
    renderer.lightAmount = 1
    currScene.add_lights(lightlist)

    make_ssbo(lightlist, 3)

    currScene.inputMan.set_plusminus_callback(lightsplusminus)

    cam = currScene.get_current_camera()
    # cam.radius = 400
    # cam.updateHorizontal(0)
    # cam.updateVertical(89.375)

    file2 = open(r"test_{}.txt".format(height), "w+")
    file2.close()

    update_persp_event(width, height)
    glutMainLoop()


def update_persp_event(w, h):
    global renderer, currScene
    glViewport(0, 0, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    currScene.get_current_camera().update_pMatrix()
    renderer.resize(w, h)

    clear_framebuffer([0, 0, 0, 1])


def set_up_scene_entities(scene):
    p = Plane()
    p.set_rotation([0, 0, 90])
    p.set_scale([1000, 1000, 1000])
    cube = Cube()
    cube.set_position([0, 0.5, 0])

    cubelist = cubes(5)
    cubelist.append(p)

    cube2 = Cube()
    cube2.set_position([0, 0.5, 1])
    scene.add_entities(cubelist)


def save_current_framebuffer_as_png(bufferid):
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    GL.glBindFramebuffer(GL_READ_FRAMEBUFFER, bufferid)
    data = glReadPixels(0, 0, width, height, GL_RGBA16F, GL_FLOAT)
    image = Image.frombytes("RGBA", (width, height), data)
    image = ImageOps.flip(image)  # in my case image is flipped top-bottom for some reason
    image.save('glutout.png', 'PNG')


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

    light = PointLight(intensity=1, attenuation=Attenuation(const=1, linear=1, exp=3))

    r = light.radius
    a = min((math.sqrt(amount / 2) * 4 + 1), 7)
    a = math.sqrt(r)/2
    for i in range(-amount, amount + 1):
        for j in range(-amount, amount + 1):
            temp = Transform()
            temp.set_position([i * a, 2, j * a, 1])
            temp.set_scale([r, r, r])
            lightlist.append(temp)
    return lightlist


def make_ssbo(data_list, bufferIndex=3):
    global lightssob
    lightssob = glGenBuffers(1)

    glBindBuffer(GL_SHADER_STORAGE_BUFFER, lightssob)
    glBindBufferBase(GL_SHADER_STORAGE_BUFFER, bufferIndex, lightssob)

    data = flatten_list(data_list)

    glBufferData(GL_SHADER_STORAGE_BUFFER, data.nbytes, data=data, usage=GL_STATIC_DRAW)
    glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)


def lightsplusminus(num):
    global lightcount
    lightcount += num
    lightcount = max(lightcount, 0)
    res = min(max(4 * (lightcount + 1) * (lightcount + 1), 0), len(renderer.currScene.lights))
    renderer.lightAmount = res
    #slot2 = glGetUniformLocation(renderer.lightProgram, "lightnum")
    #glUniform1i(slot2, )


def fps_update():
    global fps_counter, av_start_time, start_time, time_per_frame, counter, lightcount, height

    tim = (time.time() - start_time)

    if tim != 0:
        counter += 1
        if (time.time() - av_start_time) > 1:
            if lightcount <=100:
               file2 = open(r"test_{}.txt".format(height), "a")
               txt = "{} \n".format(counter / (time.time() - av_start_time))
               txt = txt.replace(".", ",")
               file2.writelines(txt)
               file2.close()
            #lightsplusminus(1)
            #print("FPS: ",   counter/(time.time() - av_start_time))
            counter = 0

            av_start_time = time.time()

        time_per_frame = tim
        #print("FPS: ", 1 / tim)

    start_time = time.time()


def render():
    renderer.deferred_lightPass_render()

    glFlush()

    fps_update()


init()
