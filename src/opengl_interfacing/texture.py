from OpenGL import GL
from OpenGL.GL import GL_TEXTURE_2D, GL_UNSIGNED_BYTE, GL_REPEAT, GL_TEXTURE_WRAP_S, \
    GL_TEXTURE_WRAP_T, GL_TEXTURE_MIN_FILTER, GL_LINEAR, GL_RGB, GL_NEAREST, GL_TEXTURE_MAG_FILTER, \
    GL_NEAREST_MIPMAP_LINEAR, GL_CLAMP_TO_EDGE, GL_COLOR_ATTACHMENT0, GL_FRAMEBUFFER, GL_RGB8, GL_RGBA, glGenTextures, \
    GL_LINEAR_MIPMAP_NEAREST
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

    def __init__(self, size=None, data=None, mipmap=False, repeat=False, framebuffer = None):

        self.mipmap = mipmap
        self.repeat = repeat
        self.genMipmap = False

        self.slot = glGenTextures(1)
        GL.glActiveTexture(GL.GL_TEXTURE0 + self.slot)
        GL.glBindTexture(GL_TEXTURE_2D, self.slot)

        if size:
            self.width = size[0]
            self.height = size[1]

        if not data is not None and size:
            GL.glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width, self.height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
            GL.glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, self.slot, 0)
        else:
            GL.glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

        bind(self)



def bind(txt):
    GL.glActiveTexture(GL.GL_TEXTURE0 + txt.slot)
    GL.glBindTexture(GL_TEXTURE_2D, txt.slot)

    if txt.mipmap:
        if not txt.genMipmap:
            glGenerateMipmap(GL_TEXTURE_2D)
            txt.genMipmap = True
        GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
    else:
        GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    if txt.repeat:
        GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    else:
        GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
