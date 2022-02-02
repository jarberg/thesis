from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo
from OpenGL.GL import shaders

from utils.initshader import initShaders


width, height = 800, 800
aspectRatio = width/height


program = None
window = None

def render():
    try:

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.0, 0.0, 1.0, 1.0)
        #glLoadIdentity()
        #glutSwapBuffers()  # important for double buffering
        glutWireTeapot(0.5)
        glFlush()

    except Exception as e:
        print(e)

def init():

    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow("Opengl Window In Python")

    glutDisplayFunc(render)
    glutIdleFunc(render)

    program = initShaders("shader/vertex-shader.glsl", "shader/fragment-shader.glsl")
    glUseProgram(program)
    glutMainLoop()


init()