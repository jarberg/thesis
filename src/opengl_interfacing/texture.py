from OpenGL import GL
from OpenGL.GL import GL_TEXTURE_2D, GL_UNSIGNED_BYTE, GL_REPEAT, GL_TEXTURE_WRAP_S, \
    GL_TEXTURE_WRAP_T, GL_TEXTURE_MIN_FILTER, GL_LINEAR, GL_RGB, GL_NEAREST, GL_TEXTURE_MAG_FILTER, \
    GL_NEAREST_MIPMAP_LINEAR, GL_CLAMP_TO_EDGE, GL_COLOR_ATTACHMENT0, GL_FRAMEBUFFER, GL_RGB8, GL_RGBA, glGenTextures, \
    GL_LINEAR_MIPMAP_NEAREST, GL_TEXTURE_2D_MULTISAMPLE, glTexImage2DMultisample, glBindTexture, GL_DEPTH_COMPONENT, \
    glTexParameteri, GL_TEXTURE_COMPARE_FUNC, GL_LEQUAL, GL_NONE, GL_TEXTURE_COMPARE_MODE
from OpenGL.GL.framebufferobjects import glGenerateMipmap


class Texture_Manager:
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self):
        self.txtDict = {}
        self.usedSlots = []

    def createNewTexture(self, size=None, data=None, mipmap=False):
        return Texture(size=size, data=data, mipmap=mipmap)

    def _register(self):
        pass

    def _unregister(self):
        pass


class Texture:

    def __init__(self, size=None, data=None, mipmap=False, repeat=False):

        self.mipmap = mipmap
        self.repeat = repeat
        self.genMipmap = False
        self.texType = GL_TEXTURE_2D
        self.format = GL_RGBA
        self.slot = glGenTextures(1)
        GL.glActiveTexture(GL.GL_TEXTURE0 + self.slot)
        GL.glBindTexture(GL_TEXTURE_2D, self.slot)

        if size:
            self.width = size[0]
            self.height = size[1]

        if data is None and size:
            GL.glTexImage2D(self.texType, 0, self.format, self.width, self.height, 0, self.format, GL_UNSIGNED_BYTE, None)
        else:
            GL.glTexImage2D(self.texType, 0, self.format, self.width, self.height, 0, self.format, GL_UNSIGNED_BYTE, data)

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
            GL.glTexImage2D(self.texType, 0, GL_DEPTH_COMPONENT, self.width, self.height, 0, GL_DEPTH_COMPONENT, GL_UNSIGNED_BYTE, None)
        else:
            GL.glTexImage2D(self.texType, 0, GL_DEPTH_COMPONENT, self.width, self.height, 0, GL_DEPTH_COMPONENT, GL_UNSIGNED_BYTE, data)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_FUNC, GL_LEQUAL)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_MODE, GL_NONE)

class Texture2dMS:

    def __init__(self, size, mipmap=False, repeat=False):

        self.mipmap = mipmap
        self.repeat = repeat
        self.genMipmap = False
        self.texType = GL_TEXTURE_2D_MULTISAMPLE
        self.slot = glGenTextures(1)
        GL.glActiveTexture(GL.GL_TEXTURE0 + self.slot)
        glBindTexture(GL_TEXTURE_2D_MULTISAMPLE, self.slot)


        self.width = size[0]
        self.height = size[1]
        glTexImage2DMultisample(GL_TEXTURE_2D_MULTISAMPLE, 12, GL_RGBA, self.width,  self.height, True)

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
