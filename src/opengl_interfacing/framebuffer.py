import OpenGL.GL as GL
from OpenGL.GL import GL_FRAMEBUFFER, glBindRenderbuffer, GL_RENDERBUFFER, GL_DEPTH_ATTACHMENT, GL_FRAMEBUFFER_COMPLETE, \
    GL_VIEWPORT, glGenFramebuffers, glGenRenderbuffers, \
    glClearColor, glClear, GL_COLOR_BUFFER_BIT, \
    GL_DEPTH_BUFFER_BIT, GL_DRAW_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, glFramebufferTexture2D, GL_READ_FRAMEBUFFER, \
    GL_NEAREST, GL_COLOR_ATTACHMENT1, GL_FRONT, GL_SAMPLES, GL_COLOR_ATTACHMENT2, glDrawBuffers, \
    GL_UNSIGNED_BYTE, glBindTexture, glTexImage2DMultisample, GL_TEXTURE_2D_MULTISAMPLE
from OpenGL.GL import glBindFramebuffer, GL_FRAMEBUFFER_INCOMPLETE_MULTISAMPLE
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_RGB
from OpenGL.raw.GL.VERSION.GL_1_4 import GL_DEPTH_COMPONENT32

from opengl_interfacing import texture
from opengl_interfacing.texture import Texture


class FrameBuffer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bound = False

        self.framebuffer = glGenFramebuffers(1)

        GL.glHint(GL_SAMPLES, 10)

        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)

        # depth renderbuffer
        self.renderbuffer = glGenRenderbuffers(1)
        GL.glBindRenderbuffer(GL_RENDERBUFFER, self.renderbuffer)
        GL.glRenderbufferStorage(GL_RENDERBUFFER, GL.GL_DEPTH_COMPONENT, width, height)
        GL.glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.renderbuffer)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)

        check_status()

    def bind(self):
        if self.bound:
            return

        currentViewport = GL.glGetIntegerv(GL_VIEWPORT)
        self.unbindWidth = currentViewport[2]
        self.unbindHeight = currentViewport[3]
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
        glBindRenderbuffer(GL_RENDERBUFFER, self.renderbuffer)

        GL.glViewport(0, 0, self.width, self.height)

        clear_framebuffer([0,0,0,0])

        self.bound = True

    def unbind(self):
        if not self.bound:
            return
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)
        GL.glViewport(0, 0, self.unbindWidth, self.unbindHeight)
        self.bound = False
        clear_framebuffer([0,0,0,0])


class G_Buffer:
    def __init__(self, size):

        self.width = size[0]
        self.height = size[1]
        self.bound = False

        self.framebuffer = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)

        self.position_tex = Texture(size=[self.width, self.height], format=GL_RGB)
        texture.bind(self.position_tex)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, self.position_tex.texType, self.position_tex.slot,
                               0)

        self.normal_tex = Texture(size=[self.width, self.height], format=GL_RGB)
        texture.bind(self.normal_tex)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT1, self.normal_tex.texType, self.normal_tex.slot, 0)

        self.albedo_tex = Texture(size=[self.width, self.height])
        texture.bind(self.albedo_tex)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT2, self.albedo_tex.texType, self.albedo_tex.slot, 0)

        # depth renderbuffer
        self.renderbuffer = glGenRenderbuffers(1)
        GL.glBindRenderbuffer(GL_RENDERBUFFER, self.renderbuffer)
        GL.glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT32, self.width, self.height)
        GL.glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.renderbuffer)

        glDrawBuffers(3, [GL_COLOR_ATTACHMENT0, GL_COLOR_ATTACHMENT1, GL_COLOR_ATTACHMENT2])

        check_status()

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)

    def bind(self):
        if self.bound:
            return
        currentViewport = GL.glGetIntegerv(GL_VIEWPORT)
        self.unbindWidth = currentViewport[2]
        self.unbindHeight = currentViewport[3]

        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
        glBindRenderbuffer(GL_RENDERBUFFER, self.renderbuffer)

        GL.glViewport(0, 0, self.width, self.height)

        clear_framebuffer([0,0,0,0])

        self.bound = True

    def unbind(self):
        if not self.bound:
            return
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)
        GL.glViewport(0, 0, self.unbindWidth, self.unbindHeight)

        self.bound = False

        clear_framebuffer([0,0,0,0])

    def resize(self, w=None, h=None):
        if w and h:
            self.width = w
            self.height = h
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)

        for tex in [self.albedo_tex, self.normal_tex, self.position_tex]:
            glBindTexture(tex.texType, tex.slot)
            GL.glTexImage2D(tex.texType, 0, tex.format, self.width, self.height, 0, tex.format, GL_UNSIGNED_BYTE, None)

        GL.glBindRenderbuffer(GL_RENDERBUFFER, self.renderbuffer)
        GL.glRenderbufferStorage(GL_RENDERBUFFER, GL.GL_DEPTH_COMPONENT, self.width, self.height)

        if not self.bound:
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            glBindRenderbuffer(GL_RENDERBUFFER, 0)


class FrameBuffer_Tex_MS:
    def __init__(self, width, height, samples=0):
        self.width = width
        self.height = height

        self.framebuffer = glGenFramebuffers(1)
        self.samples = samples
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)

        self.texture = texture.Texture2dMS([width, height], self.get_samples())
        texture.bind(self.texture)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, self.texture.texType, self.texture.slot, 0)

        self.renderbuffer = glGenRenderbuffers(1)
        GL.glBindRenderbuffer(GL_RENDERBUFFER, self.renderbuffer)
        GL.glRenderbufferStorageMultisample(GL_RENDERBUFFER, self.get_samples(), GL_DEPTH_COMPONENT32, self.width,
                                            self.height)
        GL.glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.renderbuffer)

        check_status()

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)
        self.bound = False

    def set_samples(self, samples):
        self.samples = max(self.samples+samples, 0)

    def get_samples(self):
        return pow(2, self.samples)

    def bind(self):
        if self.bound:
            return
        currentViewport = GL.glGetIntegerv(GL_VIEWPORT)

        self.unbindWidth = currentViewport[2]
        self.unbindHeight = currentViewport[3]

        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
        glBindRenderbuffer(GL_RENDERBUFFER, self.renderbuffer)

        GL.glViewport(0, 0, self.width, self.height)

        clear_framebuffer([0.0, 0.5, 0.0, 1.0])
        self.bound = True

    def unbind(self):
        if not self.bound:
            return
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)
        GL.glViewport(0, 0, self.unbindWidth, self.unbindHeight)
        clear_framebuffer([0.0, 0.5, 0.0, 1.0])
        self.bound = False

    def resize(self, w=None, h=None):
        if w and h:
            self.width = w
            self.height = h
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)

        GL.glActiveTexture(GL.GL_TEXTURE0 + self.texture.slot)
        GL.glBindTexture(self.texture.texType, self.texture.slot)

        glTexImage2DMultisample(GL_TEXTURE_2D_MULTISAMPLE, self.get_samples(), self.texture.format, self.width, self.height, True)

        GL.glBindRenderbuffer(GL_RENDERBUFFER, self.renderbuffer)
        GL.glRenderbufferStorageMultisample(GL_RENDERBUFFER, self.get_samples(), GL_DEPTH_COMPONENT32, self.width, self.height)



def check_status():
    status = GL.glCheckFramebufferStatus(GL_FRAMEBUFFER)

    if status != int(GL_FRAMEBUFFER_COMPLETE):
        # https://neslib.github.io/Ooogles.Net/html/0e1349ae-da69-6e5e-edd6-edd8523101f8.htm
        if status == int(GL.GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT):
            raise Exception("IncompleteAttachment: {}".format(status))
        elif status == int(GL.GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT):
            raise Exception("IncompleteAttachment: {}".format(status))
        elif status == int(GL.GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT):
            raise Exception("Missing attachment: {}".format(status))
        elif status == int(GL.GL_FRAMEBUFFER_UNSUPPORTED):
            raise Exception("Not supported: {}".format(status))
        elif status == int(GL_FRAMEBUFFER_INCOMPLETE_MULTISAMPLE):
            raise Exception("Incomplete multisample: {}".format(status))
        else:
            raise Exception("Framebuffer creation failed to undefined error: {}".format(status))


def blit_col_0(source, target):
    GL.glBindFramebuffer(GL_READ_FRAMEBUFFER, source.framebuffer)
    GL.glBindFramebuffer(GL_DRAW_FRAMEBUFFER, target)

    GL.glReadBuffer(GL_COLOR_ATTACHMENT0)
    GL.glDrawBuffer(GL_COLOR_ATTACHMENT0)

    GL.glBlitFramebuffer(
        0, 0, source.width, source.height,
        0, 0, source.width, source.width,
        GL_COLOR_BUFFER_BIT, GL_NEAREST)


def blit_to_default(source):
    GL.glBindFramebuffer(GL_READ_FRAMEBUFFER, source.framebuffer)
    GL.glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)

    GL.glReadBuffer(GL_COLOR_ATTACHMENT0)
    GL.glDrawBuffer(GL_FRONT)

    GL.glBlitFramebuffer(
        0, 0, source.width, source.height,
        0, 0, source.width, source.height,
        GL_COLOR_BUFFER_BIT, GL_NEAREST)

    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    glBindRenderbuffer(GL_RENDERBUFFER, 0)



def clear_framebuffer(color=None):
    if color is None:
        color = [0.0, 1.0, 1.0, 1.0]
    glClearColor(*color)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
