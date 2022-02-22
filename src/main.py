from OpenGL.GL import *
from OpenGL.GLUT import *

from src.utils.initshader import initShaders
from utils.objectUtils import *
from utils.objects import *

width, height = 800, 800
aspectRatio = width/height
program = None
window = None

def render():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0, 0.0, 1.0, 1.0)
    #glLoadIdentity()
    #glutSwapBuffers()  # important for double buffering
    glutSolidTeapot(0.5)
    glFlush()


def init():

    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow("Opengl Window In Python")

    glutDisplayFunc(render)
    glutIdleFunc(render)

    program = initShaders("src/shader/vertex-shader.glsl", "src/shader/fragment-shader.glsl")#"src/shader/fragment-shader.glsl")
    glUseProgram(program)
    glutMainLoop()

#init()

t = Transform()
t.m = t.m*(Matrix(n=4))

t.set_position([1, 2, 3])

print("pos ", t.get_position())
print("rot ", t.get_rotation())
print("sca ", t.get_scale(), "\n")

t.set_rotation([45, 45, 0])

print("pos ", t.get_position())
print("rot ", t.get_rotation())
print("sca ", t.get_scale(), "\n")

t.set_scale([3, 2, 1])

print("pos ", t.get_position())
print("rot ", t.get_rotation())
print("sca ", t.get_scale())
print(t.m.m)
