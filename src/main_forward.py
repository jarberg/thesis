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
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_DEPTH_TEST, glEnable, glDisable, GL_CULL_FACE, glFlush, glViewport
from OpenGL.raw.GL.VERSION.GL_2_0 import glUseProgram
from PIL import Image, ImageOps

from opengl_interfacing.framebuffer import G_Buffer, clear_framebuffer
from opengl_interfacing.initshader import initShaders
from opengl_interfacing.renderer import Renderer
from opengl_interfacing.sceneObjects import Plane, Cube
from opengl_interfacing.texture import createNewTexture
from utils.objectUtils import flatten

from utils.scene import Scene

width, height = 400, 400
aspectRatio = width / height
deferred_program = None
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


    cubelist = cubes(20)
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
    a = min( (math.sqrt(amount/2)*4+1), 7)
    for i in range(-amount, amount+1):
        for j in range(-amount, amount+1):
            c = Cube()
            c.set_position([i*a, 0.5, j*a])
            c.material.set_tex_diffuse(tex)
            cubelist.append(c)
    return cubelist

def lights(amount):
    lightlist = []
    a = min( (math.sqrt(amount/2)*4+1), 7)
    for i in range(-amount, amount+1):
        for j in range(-amount, amount+1):
            c = [i*a, 2, j*a, 1]
            lightlist.append(c)
    return lightlist


def init():
    global start_time, fps_counter, counter, lightcount,lightssob
    global renderer, deferred_program, lightProgram, forward_program, buffer, currScene, av_start_time, height
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
    GL.glLineWidth(1)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

    GL.glEnable(GL.GL_BLEND)
    glEnable(GL_DEPTH_TEST)

    glDisable(GL_CULL_FACE)
    glutDisplayFunc(render)
    glutIdleFunc(render)

    forward_program = initShaders("/shader/forward/vertex-shader.glsl", "/shader/forward/fragment-shader.glsl")


    glUseProgram(forward_program)

    buffer = G_Buffer([width, height])

    currScene = Scene()

    set_up_scene_entities(currScene)
    renderer = Renderer(currScene, [width, height])

    lightssob = glGenBuffers(1)

    glBindBuffer(GL_SHADER_STORAGE_BUFFER, lightssob)
    glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 3, lightssob)

    glUseProgram(forward_program)
    light = lights(100)
    data = flatten(light)

    glBufferData(GL_SHADER_STORAGE_BUFFER, data.nbytes, data=data, usage=GL_STATIC_DRAW)
    glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)

    #lightsplusminus(0)
    currScene.inputMan.set_plusminus_callback(lightsplusminus)

    cam = currScene.get_current_camera()
    cam.radius = 400
    cam.updateHorizontal(0)
    cam.updateVertical(89.375)

    file2 = open(r"test_{}.txt".format(height), "w+")
    glutMainLoop()

def lightsplusminus(num):
    global lightcount,lightssob, forward_program
    lightcount += num
    lightcount = max(lightcount, 0)


    slot2 = glGetUniformLocation(forward_program, "lightnum")
    glUniform1i(slot2, 4*(lightcount+1)*(lightcount+1))


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

            #print("FPS: ",   counter/(time.time() - av_start_time))
            counter = 0

            av_start_time = time.time()
            lightsplusminus(1)
        time_per_frame = tim
        #print("FPS: ", 1 / tim)
    start_time = time.time()


def render():
    global renderer

    clear_framebuffer()
    renderer.draw()

    glFlush()

    fps_update()


init()
