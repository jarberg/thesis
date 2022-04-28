import time

from opengl_interfacing.sceneObjects import Cube
from utils.scene import Scene

global debug, GPU
GPU = False
debug = False

from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLUT import *


from opengl_interfacing.framebuffer import clear_framebuffer
from utils.animationObject import init_geo_anim

from opengl_interfacing.initshader import initShaders
from opengl_interfacing.renderer import  Renderer
from utils.objectUtils import flatten_list, Matrix, flatten

width, height = 200, 200
aspectRatio = width / height
deferred_program = None
postProgram = None
window = None


def update_persp_event(w, h):
    global renderer, buffer, currScene
    cam = currScene.get_current_camera()
    glViewport(0, 0, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    cam.update_pMatrix()

    clear_framebuffer()



def set_up_scene_entities(scene):

    cube = Cube()
    cube.set_position([0, 1, 2])
    cube.set_scale([0.1, 0.1, 0.1])

    animator, animated, joint_list = init_geo_anim()
    animated.set_animator(animator)
    scene.add_animator(animator)
    scene.add_entities([cube, animated.model, animated])
    scene.add_joints(joint_list)


def init():
    global start_time
    global fps_counter

    global renderer, joint_list, deferred_program,time_per_frame, lightProgram, jointProgram, animator, currScene,test_ssbo

    time_per_frame = 0
    fps_counter = 0
    start_time = time.time()

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow("Opengl Window In Python")

    glutReshapeFunc(update_persp_event)
    GL.glLineWidth(2)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

    GL.glEnable(GL.GL_BLEND)
    glEnable(GL_DEPTH_TEST)

    #glDisable(GL_CULL_FACE)
    glutDisplayFunc(render)
    glutIdleFunc(render)

    program = initShaders("/shader/skinning/skinning_v_cpu_interpolate.glsl", "/shader/skinning/skinning_f.glsl")
    jointProgram = initShaders("/shader/debug/joint_v_shader.glsl", "/shader/debug/joint_f_shader.glsl")
    glUseProgram(program)


    currScene = Scene()
    set_up_scene_entities(currScene)

    renderer = Renderer(currScene=currScene)


    test_ssbo = glGenBuffers(1)
    glBindBuffer(GL_SHADER_STORAGE_BUFFER, test_ssbo)
    data = []

    animator = currScene.animators[0]

    for i in range(len(animator.animation.keyframes)):
        for j, joint in enumerate(animator.animation.keyframes[i].transforms):
            data.append(animator.animation.keyframes[i].transforms[joint])
    data = flatten_list(data)
    glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 4, test_ssbo)
    glBufferData(GL_SHADER_STORAGE_BUFFER, data.nbytes, data=data, usage=GL_STATIC_DRAW)
    glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)


    test3_ssbo = glGenBuffers(1)
    glBindBuffer(GL_SHADER_STORAGE_BUFFER, test3_ssbo)

    jointList = [-1, 0, 1, 2]

    data2 = flatten(jointList)
    glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 4, test3_ssbo)
    glBufferData(GL_SHADER_STORAGE_BUFFER, data2.nbytes, data=data2, usage=GL_STATIC_DRAW)
    glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)


    test2_ssbo = glGenBuffers(1)
    glBindBuffer(GL_SHADER_STORAGE_BUFFER, test2_ssbo)
    data2 = []
    for i in range(len(animator.animation.keyframes)):
        jointList = list(animator.animation.keyframes[i].transforms)
        for j, joint in enumerate(jointList):
            if j-1 >= 0:
                parentName = jointList[j-1]
                data2.append(animator.animation.keyframes[i].transforms[parentName])
            else:
                data2.append(Matrix())


    data2 = flatten_list(data2)
    glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 4, test2_ssbo)
    glBufferData(GL_SHADER_STORAGE_BUFFER, data2.nbytes, data=data2, usage=GL_STATIC_DRAW)
    glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)

    glutMainLoop()



def fps_update():
    global fps_counter
    global start_time
    global time_per_frame
    tim = (time.time() - start_time)

    if tim != 0:
        time_per_frame = tim
        #print("FPS: ", 1 / tim)


def render():
    global renderer, debugRender,anim,  GPU, buffer, deferred_program, lightProgram, start_time,  joint_list, currScene
    start_time = time.time()

    clear_framebuffer()
    glUseProgram(program)

    renderer.skinning_draw()

    if currScene.debug:
        renderer.debug_draw()
        glUseProgram(jointProgram)
        renderer.joint_draw()


    currScene.update(time_per_frame)

    glFlush()

    fps_update()

init()