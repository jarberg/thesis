import OpenGL.GL as GL
from OpenGL.GL import glCreateFramebuffers
from OpenGL.GL import GL_FRAMEBUFFER, glCreateRenderbuffers, glBindRenderbuffer, GL_RENDERBUFFER, GL_DEPTH_COMPONENT16, \
    GL_DEPTH_ATTACHMENT, glCreateTextures, GL_TEXTURE_2D, GL_RGBA, GL_UNSIGNED_BYTE, GL_REPEAT, GL_TEXTURE_WRAP_S, \
    GL_TEXTURE_WRAP_T, glRenderbufferStorage, glFramebufferRenderbuffer, glBindTextures, GL_COLOR_ATTACHMENT0, \
    GL_FRAMEBUFFER_COMPLETE, GL_VIEWPORT, GL_TEXTURE_MIN_FILTER, GL_LINEAR, glNamedRenderbufferStorage, \
    GL_DEPTH_COMPONENT32, glBindTexture, GLuint, glGenTextures, GL_RGB, GL_NEAREST, GL_DEPTH_COMPONENT, \
    GL_TEXTURE_MAG_FILTER, glGenFramebuffers, glGenRenderbuffers, glClearColor, glClear, GL_COLOR_BUFFER_BIT, \
    GL_DEPTH_BUFFER_BIT, glPopAttrib, glFlush
from OpenGL.GL import glBindFramebuffer


class FrameBuffer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bound = False

        self.framebuffer = glGenFramebuffers(1)
        print(self.framebuffer)
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        GL.glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width, self.height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        self.renderbuffer = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.renderbuffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL.GL_DEPTH_COMPONENT16, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.renderbuffer)

        GL.glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, self.texture, 0)

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
        glBindRenderbuffer(GL_RENDERBUFFER, 0)

    def bind(self, textureSlot):
        if self.bound:
            return
        currentViewport = GL.glGetIntegerv(GL_VIEWPORT)
        self.unbindWidth = currentViewport[2]
        self.unbindHeight = currentViewport[3]
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
        glBindRenderbuffer(GL_RENDERBUFFER, self.renderbuffer)
        self.bindTexture(textureSlot)

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

        glClearColor(1.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glFlush()



    def bindTexture(self, textureSlot):
        GL.glActiveTexture(GL.GL_TEXTURE0 + textureSlot)
        GL.glBindTexture(GL_TEXTURE_2D, self.texture)
        GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
