from OpenGL.GLUT import glutKeyboardFunc, glutMotionFunc, glutMouseFunc, glutDisplayFunc
from OpenGL.raw.GLUT import glutGet, GLUT_WINDOW_WIDTH, GLUT_WINDOW_HEIGHT, glutIdleFunc
from OpenGL.GL import glUseProgram,glEnable,GL_DEPTH_TEST,glDepthFunc,GL_LESS
from opengl_interfacing.renderer import Renderer
from utils.objectUtils import Vector


class Input_manager:

    def __init__(self, currScene):
        self.buttonPressed = -1
        self.dragx_start = 0
        self.dragy_start = 0
        self.currScene = currScene
        self.renderer = None
        glutKeyboardFunc(self.buttons)
        glutMotionFunc(self.mouseControl)
        glutMouseFunc(self.on_click)


    def set_plusminus_callback(self, callback):
        self.plusminus = callback

    def change_render_method(self, callback):
        self.render_method = callback

    def buttons(self, key, x, y):

        currscene = self.currScene

        if key == b'd':
            currscene.set_debug()
        if key == b'g':
            currscene.set_GPU()
        if key == b'+':
            self.plusminus(1)
        if key == b'-':
            self.plusminus(-1)
        if key == b'p':
            self.currScene.play = not self.currScene.play
        if key == b'1':
            self.render_method(self.renderer, 0)
        if key == b'2':
            self.render_method(self.renderer, 1)
        if key == b'3':
            self.render_method(self.renderer, 2)
        if key == b'4':
            self.render_method(self.renderer, 3)

    def on_click(self, button, state, x, y):

        cam = self.currScene.get_current_camera()
        self.buttonPressed = -1
        if button == 0:
            self.buttonPressed = 0
            if state == 0:
                self.dragx_start = x
                self.dragy_start = y
        elif (button == 1):
            self.buttonPressed = 1
            if state == 0:
                self.dragx_start = x
                self.dragy_start = y
        elif button == 3:
            cam.adjustDistance(-1)
        elif button == 4:
            cam.adjustDistance(1)



    def mouseControl(self, mx, my):
        cam = self.currScene.get_current_camera()
        if self.buttonPressed == 0:
            ratio = glutGet(GLUT_WINDOW_WIDTH) / glutGet(GLUT_WINDOW_HEIGHT)

            deltax = ((mx - self.dragx_start) * ratio) / glutGet(GLUT_WINDOW_WIDTH)
            deltay = (my - self.dragy_start) / glutGet(GLUT_WINDOW_HEIGHT)

            cam.updateHorizontal(-deltax * 100)
            cam.updateVertical(-deltay * 100)

            self.dragx_start = mx
            self.dragy_start = my

        if self.buttonPressed == 1:
            ratio = glutGet(GLUT_WINDOW_WIDTH) / glutGet(GLUT_WINDOW_HEIGHT)
            deltax = ((mx - self.dragx_start) * ratio) / glutGet(GLUT_WINDOW_WIDTH)
            deltay = (my - self.dragy_start) / glutGet(GLUT_WINDOW_HEIGHT)
            campos = cam.get_position()

            camDirx = cam.ip_x_axis
            camDiry = cam.ip_y_axis

            diry = camDiry * deltay * -100

            dir = camDirx * deltax * 100
            pos = Vector(campos) + dir + diry

            newpos = [pos[0], pos[1], pos[2]]
            cam.set_position(newpos)

            self.dragx_start = mx
            self.dragy_start = my

