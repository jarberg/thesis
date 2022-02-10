from OpenGL.GL import *
from OpenGL.GLUT import *

from src.utils.initshader import initShaders
from src.utils.objectUtils import *
from src.utils.objects import *

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

    program = initShaders("src/shader/vertex-shader.glsl", "src/shader/aa_f_shader.glsl")#"src/shader/fragment-shader.glsl")
    glUseProgram(program)
    glutMainLoop()

init()

t = Transform()
t.m = t.m*(Matrix(n=4)*0.01)
t.get_scale()
look_at(Vector([1,1,1]), Vector([0,0,0]), Vector([0,1,0]))

t.m = rotate([20.1111111111112161111111111, 35.000000000010060000001, 19.9999999])
print([degrees(x) for x in t.get_rotation()])

t.get_rotation()

