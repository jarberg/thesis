import OpenGL.GL as GL
from OpenGL.GL import GL_FRAMEBUFFER, glBindRenderbuffer, GL_RENDERBUFFER, GL_DEPTH_ATTACHMENT, glRenderbufferStorage, \
    glFramebufferRenderbuffer, GL_FRAMEBUFFER_COMPLETE, GL_VIEWPORT, glGenFramebuffers, glGenRenderbuffers, \
    glClearColor, glClear, GL_COLOR_BUFFER_BIT, \
    GL_DEPTH_BUFFER_BIT, glFlush, GL_DRAW_FRAMEBUFFER, glFramebufferTexture, GL_COLOR_ATTACHMENT0, glDrawBuffer, \
    glFramebufferTexture2D, GL_TEXTURE_2D, GL_TEXTURE_2D_MULTISAMPLE, GL_READ_FRAMEBUFFER, glBlitFramebuffer, \
    GL_NEAREST, GL_COLOR_ATTACHMENT1, GL_FRONT
from OpenGL.GL import glBindFramebuffer

from opengl_interfacing import texture
from opengl_interfacing.texture import Texture_Manager


class FrameBuffer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bound = False

        self.framebuffer = glGenFramebuffers(1)

        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)

        self.texture = Texture_Manager().createNewTexture(size=[width, height])
        glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,  self.texture.slot, 0)

        #self.renderbuffer = glGenRenderbuffers(1)
        #glBindRenderbuffer(GL_RENDERBUFFER, self.renderbuffer)
        #glRenderbufferStorage(GL_RENDERBUFFER, GL.GL_DEPTH_COMPONENT16, width, height)
        #glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.renderbuffer)


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
            else:
                raise Exception("Framebuffer creation failed to undefined error: {}".format(status))

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        #glBindRenderbuffer(GL_RENDERBUFFER, 0)

    def bind(self):
        if self.bound:
            return
        currentViewport = GL.glGetIntegerv(GL_VIEWPORT)
        self.unbindWidth = currentViewport[2]
        self.unbindHeight = currentViewport[3]
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.texture.slot, 0)
        texture.bind(self.texture)

        GL.glViewport(0, 0, self.width, self.height)

        glClearColor(0.0, 1.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.bound = True


    def unbind(self):
        if not self.bound:
            return
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)
        GL.glViewport(0, 0, self.unbindWidth, self.unbindHeight)
        self.bound = False

        glClearColor(0.3, 0.0, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glFlush()


class FrameBuffer_blit_MS:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.framebuffer = glGenFramebuffers(1)

        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)

        GL.glDrawBuffers(2, [GL_COLOR_ATTACHMENT0, GL_COLOR_ATTACHMENT1])


        self.texture = texture.Texture([width, height])
        GL.glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.texture.slot, 0)

        self.texture2 = texture.Texture([width, height])
        GL.glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT1, GL_TEXTURE_2D,  self.texture2.slot, 0)


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
            else:
                raise Exception("Framebuffer creation failed to undefined error: {}".format(status))

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        self.bound = False


    def bind(self):
        if self.bound:
            return
        currentViewport = GL.glGetIntegerv(GL_VIEWPORT)

        self.unbindWidth = currentViewport[2]
        self.unbindHeight = currentViewport[3]

        glBindFramebuffer(GL_READ_FRAMEBUFFER, self.framebuffer)
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)

        #texture.bind(self.texture)


        GL.glViewport(0, 0, self.width, self.height)

        glClearColor(0.0, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.bound = True


    def unbind(self):
        if not self.bound:
            return
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)
        GL.glViewport(0, 0, self.unbindWidth, self.unbindHeight)
        self.bound = False

        glClearColor(0.3, 0.0, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glFlush()


class FrameBuffer_target_MS:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.framebuffer = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
        GL.glDrawBuffers(2, [GL_COLOR_ATTACHMENT0, GL_COLOR_ATTACHMENT1])

        #renderbuffer0
        self.RenderBufferHandle0 = glGenRenderbuffers(1)
        GL.glBindRenderbuffer(GL_RENDERBUFFER, self.RenderBufferHandle0)
        GL.glRenderbufferStorageMultisample(GL_RENDERBUFFER, 8, GL.GL_RGBA16, width, height)
        GL.glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, self.RenderBufferHandle0)

        ##renderbuffer1
        #self.RenderBufferHandle1 = glGenRenderbuffers(1)
        #GL.glBindRenderbuffer(GL_RENDERBUFFER, self.RenderBufferHandle1)
        #GL.glRenderbufferStorageMultisample(GL_RENDERBUFFER, 8, GL.GL_RGBA16, width, height)
        #GL.glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT1, GL_RENDERBUFFER, self.RenderBufferHandle1)

        ##depth renderbuffer
        #self.DepthBufferHandle = glGenRenderbuffers(1)
        #GL.glBindRenderbuffer(GL_RENDERBUFFER, self.DepthBufferHandle)
        #GL.glRenderbufferStorageMultisample(GL_RENDERBUFFER, 8, GL.GL_DEPTH_COMPONENT24, width, height)
        #GL.glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.DepthBufferHandle)


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
            else:
                raise Exception("Framebuffer creation failed to undefined error: {}".format(status))

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        self.bound = False


    def bind(self):
        if self.bound:
            return
        currentViewport = GL.glGetIntegerv(GL_VIEWPORT)

        self.unbindWidth = currentViewport[2]
        self.unbindHeight = currentViewport[3]

        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)

        GL.glViewport(0, 0, self.width, self.height)

        glClearColor(0.0, 0.3, 0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.bound = True


    def unbind(self):
        if not self.bound:
            return
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)
        GL.glViewport(0, 0, self.unbindWidth, self.unbindHeight)
        self.bound = False

        glClearColor(0.3, 0.0, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glFlush()


class FrameBuffer_Tex_MS:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.framebuffer = glGenFramebuffers(1)

        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)

        self.texture = texture.Texture2dMS([width, height])
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D_MULTISAMPLE, self.texture.slot, 0)

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
            else:
                raise Exception("Framebuffer creation failed to undefined error: {}".format(status))

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        self.bound = False


    def bind(self):
        if self.bound:
            return
        currentViewport = GL.glGetIntegerv(GL_VIEWPORT)

        self.unbindWidth = currentViewport[2]
        self.unbindHeight = currentViewport[3]

        glBindFramebuffer(GL_READ_FRAMEBUFFER, self.framebuffer)
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, self.framebuffer)

        texture.bind(self.texture)

        GL.glViewport(0, 0, self.width, self.height)

        glBlitFramebuffer(0, 0, self.width, self.height, 0, 0, self.width, self.height, GL_COLOR_BUFFER_BIT, GL_NEAREST)

        glClearColor(0.0, 0.3, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.bound = True


    def unbind(self):
        if not self.bound:
            return
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)
        GL.glViewport(0, 0, self.unbindWidth, self.unbindHeight)
        self.bound = False

        glClearColor(0.3, 0.0, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glFlush()


def blit(source, target):
    GL.glBindFramebuffer(GL_READ_FRAMEBUFFER, source.framebuffer)
    GL.glBindFramebuffer(GL_DRAW_FRAMEBUFFER, target.framebuffer)

    GL.glReadBuffer(GL_COLOR_ATTACHMENT0)
    GL.glDrawBuffer(GL_COLOR_ATTACHMENT0)

    GL.glBlitFramebuffer(
        0, 0, source.width, source.height,
        0, 0, target.width, target.height,
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
