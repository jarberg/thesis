import os

from OpenGL.GL import glCreateShader, glCreateProgram, glShaderSource, glCompileShader, glGetShaderInfoLog, \
    glGetShaderiv, GL_COMPILE_STATUS, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, glAttachShader, \
    glGetProgramiv, glGetProgramInfoLog, GL_LINK_STATUS, glLinkProgram, GL_GEOMETRY_SHADER

from utils import constants


def loadFile(path):
    s = ""
    with open(os.path.abspath(constants.ROOT_DIR + path).replace("\\", "/")) as f:
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


def initShaders(vShaderName=None, fShaderName=None, gShaderName=None):
    program = glCreateProgram()

    if vShaderName:
        vertexShader = _getShader(vShaderName, GL_VERTEX_SHADER)
        glAttachShader(program, vertexShader)

    if gShaderName:
        geometryShader = _getShader(fShaderName, GL_GEOMETRY_SHADER)
        glAttachShader(program, geometryShader)

    if fShaderName:
        fragmentShader = _getShader(fShaderName, GL_FRAGMENT_SHADER)
        glAttachShader(program, fragmentShader)


    glLinkProgram(program)
    linked = glGetProgramiv(program, GL_LINK_STATUS)

    if not linked:
        print(glGetProgramInfoLog(program))
        return None

    return program

