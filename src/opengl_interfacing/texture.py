import os

import numpy
from OpenGL import GL
from OpenGL.GL import GL_TEXTURE_2D, GL_UNSIGNED_BYTE, GL_REPEAT, GL_TEXTURE_WRAP_S, \
    GL_TEXTURE_WRAP_T, GL_TEXTURE_MIN_FILTER, GL_RGB, GL_NEAREST, GL_TEXTURE_MAG_FILTER, \
    GL_CLAMP_TO_EDGE, GL_RGBA, glGenTextures, \
    GL_LINEAR_MIPMAP_NEAREST, GL_TEXTURE_2D_MULTISAMPLE, glTexImage2DMultisample, glBindTexture, GL_DEPTH_COMPONENT, \
    glTexParameteri, GL_TEXTURE_COMPARE_FUNC, GL_LEQUAL, GL_NONE, GL_TEXTURE_COMPARE_MODE
from OpenGL.GL.framebufferobjects import glGenerateMipmap
from PIL import Image

from utils import constants
from opengl_interfacing.utils import get_opengl_format
from utils.objectUtils import  is_mipmapable


class Texture_Manager:
    _instance = None
    txtDict = {}
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance




    def _register(self, path, tex):
        self.txtDict[path] = tex

    def _unregister(self):
        pass

def createNewTexture(path):

    root = constants.ROOT_DIR
    wholepath = os.path.abspath(root + path).replace("\\", "/")
    im = Image.open(fp=wholepath)
    im_data = numpy.array(im.getdata())

    image_format = get_opengl_format(im.format)

    im_mipmap = is_mipmapable(im.size[0], im.size[1])
    tex = Texture(size=[im.size[0], im.size[1]], data=im_data, mipmap=im_mipmap, format=image_format)

    return tex

class Texture:

    def __init__(self, size=None, data=None, mipmap=False, repeat=False, format=GL_RGBA, dataType=GL_UNSIGNED_BYTE, secondFormat=None):

        self.mipmap = mipmap
        self.repeat = repeat
        self.genMipmap = False
        self.dataType = dataType
        self.texType = GL_TEXTURE_2D
        self.format = format
        self.secondFormat = secondFormat or format
        self.slot = glGenTextures(1)
        GL.glActiveTexture(GL.GL_TEXTURE0 + self.slot)
        GL.glBindTexture(GL_TEXTURE_2D, self.slot)


        self.width = size[0]
        self.height = size[1]

        GL.glTexImage2D(self.texType, 0, self.secondFormat, self.width, self.height, 0, self.format, self.dataType, data)

        bind(self)


class Texture_depth:

    def __init__(self, size=None, data=None, mipmap=False, repeat=False):

        self.mipmap = mipmap
        self.repeat = repeat
        self.genMipmap = False
        self.texType = GL_TEXTURE_2D
        self.slot = glGenTextures(1)
        GL.glActiveTexture(GL.GL_TEXTURE0 + self.slot)
        GL.glBindTexture(GL_TEXTURE_2D, self.slot)

        if size:
            self.width = size[0]
            self.height = size[1]

        if data is None and size:
            GL.glTexImage2D(self.texType, 0, GL_DEPTH_COMPONENT, self.width, self.height, 0, GL_DEPTH_COMPONENT,
                            GL_UNSIGNED_BYTE, None)
        else:
            GL.glTexImage2D(self.texType, 0, GL_DEPTH_COMPONENT, self.width, self.height, 0, GL_DEPTH_COMPONENT,
                            GL_UNSIGNED_BYTE, data)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_FUNC, GL_LEQUAL)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_MODE, GL_NONE)


class Texture2dMS:

    def __init__(self, size, samples, mipmap=False, format=GL_RGB, repeat=False):
        self.mipmap = mipmap
        self.samples = samples
        self.repeat = repeat
        self.format = format
        self.genMipmap = False
        self.texType = GL_TEXTURE_2D_MULTISAMPLE
        self.slot = glGenTextures(1)
        GL.glActiveTexture(GL.GL_TEXTURE0 + self.slot)
        glBindTexture(self.texType, self.slot)

        self.width = size[0]
        self.height = size[1]
        glTexImage2DMultisample(GL_TEXTURE_2D_MULTISAMPLE, self.samples, self.format, self.width, self.height, True)

        bind(self)


def bind(txt):
    GL.glActiveTexture(GL.GL_TEXTURE0 + txt.slot)
    GL.glBindTexture(txt.texType, txt.slot)

    if txt.mipmap:
        if not txt.genMipmap:
            glGenerateMipmap(txt.texType)
            txt.genMipmap = True
        GL.glTexParameteri(txt.texType, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        GL.glTexParameteri(txt.texType, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
    else:
        if txt.texType != GL_TEXTURE_2D_MULTISAMPLE:
            GL.glTexParameteri(txt.texType, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            GL.glTexParameteri(txt.texType, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    if txt.repeat:
        GL.glTexParameteri(txt.texType, GL_TEXTURE_WRAP_S, GL_REPEAT)
        GL.glTexParameteri(txt.texType, GL_TEXTURE_WRAP_T, GL_REPEAT)
    else:
        if txt.texType != GL_TEXTURE_2D_MULTISAMPLE:
            GL.glTexParameteri(txt.texType, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            GL.glTexParameteri(txt.texType, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
