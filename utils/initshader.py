from OpenGL.GL import glCreateShader
from OpenGL.GL import glCreateProgram
from OpenGL.GL import glShaderSource
from OpenGL.GL import glCompileShader
from OpenGL.GL import glGetShaderInfoLog
from OpenGL.GL import glGetShaderiv
from OpenGL.GL import GL_COMPILE_STATUS
from OpenGL.GL import GL_VERTEX_SHADER
from OpenGL.GL import GL_FRAGMENT_SHADER
from OpenGL.GL import glAttachShader
from OpenGL.GL import glGetProgramiv
from OpenGL.GL import glGetProgramInfoLog
from OpenGL.GL import GL_LINK_STATUS
from OpenGL.GL import glLinkProgram


def loadFile(path):
    s = ""
    with open(path) as f:
        s = " ".join([l for l in f])
    return s

def _getShader(shaderName, type):
    shader = glCreateShader(type)
    shaderScript = loadFile(shaderName)

    if not shaderScript:
        print("Could not find shader source: "+shaderName)

    glShaderSource(shader, shaderScript)
    glCompileShader(shader)

    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        print(glGetShaderInfoLog(shader))
        return None

    return shader


def initShaders(vShaderName, fShaderName):
    program = glCreateProgram()
    vertexShader = _getShader(vShaderName, GL_VERTEX_SHADER)
    fragmentShader = _getShader(fShaderName, GL_FRAGMENT_SHADER)

    glAttachShader(program, vertexShader)
    glAttachShader(program, fragmentShader)

    glLinkProgram(program)
    linked = glGetProgramiv(program, GL_LINK_STATUS)

    if not linked:
        print(glGetProgramInfoLog(program))
        return None

    return program