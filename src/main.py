import time

from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image, ImageOps

from opengl_interfacing.animator import Animator, Animation, KeyFrame
from opengl_interfacing.framebuffer import G_Buffer, blit_to_default
from opengl_interfacing.initshader import initShaders
from opengl_interfacing.renderer import ImagePlane, Renderer, Cube
from utils.objectUtils import flatten, perspective
from utils.objects import Joint, Animated_model

width, height = 200, 200
aspectRatio = width / height
program = None
postProgram = None
window = None

global renderer
global t2
global blit
global target
global count, cube, animator
count = 0


def update_persp_event(w, h):
    global renderer, buffer
    glViewport(0, 0, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    renderer.persp = flatten(perspective(90, glutGet(GLUT_WINDOW_WIDTH) / glutGet(GLUT_WINDOW_HEIGHT), 0.1, 100))
    #buffer.resize(w, h)
    clear_framebuffer()


def init():
    global start_time
    global fps_counter

    global renderer, cube, program, lightProgram, jointProgram, animator, time_per_frame
    global blit
    global target
    global buffer, bbj, joint, joint2
    time_per_frame = 0
    fps_counter = 0
    start_time = time.time()

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow("Opengl Window In Python")

    glutReshapeFunc(update_persp_event)
    GL.glLineWidth(1)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    GL.glEnable(GL.GL_CULL_FACE)
    GL.glEnable(GL.GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    #glDisable(GL_CULL_FACE)
    glutDisplayFunc(render)
    glutIdleFunc(render)

    program = initShaders("/shader/defered_v_shader.glsl", "/shader/defered_f_shader.glsl")
    lightProgram = initShaders("/shader/defered_light_v_shader.glsl", "/shader/defered_light_f_shader.glsl")
    jointProgram = initShaders("/shader/joint_v_shader.glsl", "/shader/joint_f_shader.glsl")
    glUseProgram(program)

    cube = Cube()
    cube.set_position([0.5, 0, -2])
    #cube.set_rotation([30, 0, 45])

    cube2 = Cube()
    cube2.set_position([-0.5, 0, -3])

    t = ImagePlane("/res/images/box.png")
    t.set_position([0.5, 0, -1])
    t.set_rotation([0, 135, 0])

    t2 = ImagePlane("/res/images/box.png")
    t2.set_position([-0.5, 0, -1])
    t2.set_rotation([0, -135, 0])

    buffer = G_Buffer([width, height])

    joint = Joint(1)
    joint2 = Joint(2, parent=joint)

    joint.set_bind_transform(joint)

    acube = Animated_model(cube, joint, 2)

    cube.material.set_tex_diffuse(t.get_material().tex_diffuse)

    animator = setup_test_anim([joint, joint2], acube)

    renderer = Renderer()
    renderer.objects = [acube, cube2]

    glutMainLoop()


def setup_test_anim(bones, model):
    bones[0].set_position([0, 0, -2])
    bones[0].set_rotation([0, 0, 0])
    key1 = KeyFrame({1: bones[0].getTransform(),
                     2: bones[1].getTransform()}, 0)

    bones[0].set_position([0, 0, -2])
    bones[1].set_rotation([0, 0, 90])
    key2 = KeyFrame({1: bones[0].getTransform(),
                     2: bones[1].getTransform()}, 1)

    bones[0].set_position([0, 0, -2])
    bones[1].set_rotation([0, 0, 180])
    key3 = KeyFrame({1: bones[0].getTransform(),
                     2: bones[1].getTransform()}, 2)

    bones[0].set_position([0, 0, -2])
    bones[1].set_rotation([0, 0, 270])
    key4 = KeyFrame({1: bones[0].getTransform(),
                     2: bones[1].getTransform()}, 3)

    bones[0].set_position([0, 0, -2])
    bones[1].set_rotation([0, 0, 0])
    key5 = KeyFrame({1: bones[0].getTransform(),
                     2: bones[1].getTransform()}, 4)

    anim = Animation([key1, key2, key3, key4, key5])

    animator = Animator(model=model, animation=anim)

    return animator


def save_current_framebuffer_as_png(bufferid):
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    GL.glBindFramebuffer(GL_READ_FRAMEBUFFER, bufferid)
    data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGBA", (width, height), data)
    image = ImageOps.flip(image)  # in my case image is flipped top-bottom for some reason
    image.save('glutout.png', 'PNG')
    GL.glBindFramebuffer(GL_FRAMEBUFFER, 0)


def fps_update():
    global fps_counter
    global start_time
    global time_per_frame
    tim = (time.time() - start_time)

    if tim != 0:
        time_per_frame = tim
        # print("FPS: ", 1 / tim)


def clear_framebuffer():
    glClearColor(0.0, 1.0, 1, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


def render():
    global renderer, buffer, program, lightProgram, cube, bbj, joint, joint2, animator, start_time
    start_time = time.time()

    buffer.bind()
    glUseProgram(program)
    renderer.draw(animator = animator)

    glUseProgram(jointProgram)
    renderer.joint_draw([joint, joint2])

    buffer.unbind()

    glUseProgram(lightProgram)
    renderer.light_draw(buffer)

    animator.update(time_per_frame)
    glFlush()

    fps_update()


init()
