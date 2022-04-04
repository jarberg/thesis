import time

from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLUT import *


from opengl_interfacing.framebuffer import clear_framebuffer
from utils.Charlie import init_Charlie
from opengl_interfacing.camera import Camera
from opengl_interfacing.initshader import initShaders
from opengl_interfacing.renderer import ImagePlane, Renderer, Cube
from utils.objectUtils import Vector

width, height = 200, 200
aspectRatio = width / height
program = None
postProgram = None
window = None


def update_persp_event(w, h):
    global renderer, buffer, cam
    glViewport(0, 0, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    cam.update_pMatrix()
    # buffer.resize(w, h)

    clear_framebuffer()


def buttons(key, x, y):
    # print(key, x, y)
    if key == b'd':
        global debug
        debug = not debug

def on_click(button, state, x, y):
    global buttonPressed, cam, dragx_start, dragy_start, dragx_mid_start, dragy_mid_start
    buttonPressed = -1
    if button == 0:
        buttonPressed = 0
        if state == 0:
            dragx_start = x
            dragy_start = y
    elif (button == 1):
        buttonPressed = 1
        if state == 0:
            dragx_mid_start = x
            dragy_mid_start = y
    elif button == 3:
        cam.adjustDistance(-3)
    elif button == 4:
        cam.adjustDistance(3)
        # scrool backward


def mouseControl(mx, my):
    global cam, dragx_start, dragy_start, buttonPressed, dragy_mid_start, dragx_mid_start
    if buttonPressed == 0:
        ratio = glutGet(GLUT_WINDOW_WIDTH) / glutGet(GLUT_WINDOW_HEIGHT)

        deltax = ((mx - dragx_start) * ratio) / glutGet(GLUT_WINDOW_WIDTH)
        deltay = (my - dragy_start) / glutGet(GLUT_WINDOW_HEIGHT)

        cam.updateHorizontal(-deltax * 100)
        cam.updateVertical(-deltay * 100)

        dragx_start = mx
        dragy_start = my

    if buttonPressed == 1:
        ratio = glutGet(GLUT_WINDOW_WIDTH) / glutGet(GLUT_WINDOW_HEIGHT)
        deltax = ((mx - dragx_mid_start) * ratio) / glutGet(GLUT_WINDOW_WIDTH)
        deltay = (my - dragy_mid_start) / glutGet(GLUT_WINDOW_HEIGHT)
        campos = cam.get_position()

        camDirx = cam.ip_x_axis
        camDiry = cam.ip_y_axis

        diry = camDiry * deltay * -100

        dir = camDirx * deltax * 100
        pos = Vector(campos) + dir + diry

        newpos = [pos[0], pos[1], pos[2]]
        cam.set_position(newpos)

        dragx_mid_start = mx
        dragy_mid_start = my


def init():
    global start_time
    global fps_counter

    global renderer, cam, debug, joint_list, program, lightProgram, jointProgram, animator, time_per_frame

    debug = False

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

    GL.glEnable(GL.GL_BLEND)
    glEnable(GL_DEPTH_TEST)

    glDisable(GL_CULL_FACE)
    glutDisplayFunc(render)
    glutIdleFunc(render)

    program = initShaders("/shader/skinning/skinning_v_cpu_interpolate.glsl", "/shader/skinning/skinning_f.glsl")
    jointProgram = initShaders("/shader/debug/joint_v_shader.glsl", "/shader/debug/joint_f_shader.glsl")
    glUseProgram(program)

    cube = Cube()
    cube2 = Cube()
    t = ImagePlane("/res/images/box.png")
    t2 = ImagePlane("/res/images/box.png")
    cube.material.set_tex_diffuse(t.get_material().tex_diffuse)
    cube.set_position([1, 0, 0])

    glutKeyboardFunc(buttons)
    glutMotionFunc(mouseControl)
    glutMouseFunc(on_click)

    animator, animated, joint_list = init_Charlie()

    cam = Camera()
    renderer = Renderer(_obj=[cube, animated.model, animated])


    # te1 = Transform()
    # te2 = Transform()
    # te2.set_position([1, 0, 0])
    # data = flatten([flatten(te1.m), flatten(te2.m)], numpy.float32, )
    ## data = flatten(2, data_type=numpy.int8)
    ## data2= flatten(te1.m)
    # global test_ssbo
    # test_ssbo = glGenBuffers(1)
    # glBindBuffer(GL_SHADER_STORAGE_BUFFER, test_ssbo)
    ## glBufferSubData(GL_SHADER_STORAGE_BUFFER, 0, data.nbytes, data)
    ## glBufferSubData(GL_SHADER_STORAGE_BUFFER, data.nbytes, data2.nbytes, data2)
    #
    # glBufferData(GL_SHADER_STORAGE_BUFFER, data.nbytes, data=data, usage=GL_DYNAMIC_COPY)
    # glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 0, test_ssbo)
    #
    ## pog = glGetBufferSubData(GL_SHADER_STORAGE_BUFFER, 0, data.nbytes, None)
    #
    # glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)

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
    global renderer, animator, debug, buffer, program, lightProgram, cube, bbj, joint, joint2, start_time, cam, test_ssbo, joint_list
    start_time = time.time()

    clear_framebuffer()
    glUseProgram(program)
    renderer.draw(cam, animator)

    if debug:
        glUseProgram(jointProgram)
        renderer.joint_draw(joint_list, cam,  animator)

    animator.update(time_per_frame)
    glFlush()

    fps_update()


init()