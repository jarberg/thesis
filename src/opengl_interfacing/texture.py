from OpenGL import GL
from OpenGL.GL import GL_TEXTURE_2D, GL_UNSIGNED_BYTE, GL_REPEAT, GL_TEXTURE_WRAP_S, \
    GL_TEXTURE_WRAP_T, GL_TEXTURE_MIN_FILTER, GL_LINEAR, GL_RGB, GL_NEAREST, GL_TEXTURE_MAG_FILTER, \
    GL_NEAREST_MIPMAP_LINEAR
from OpenGL.GL.framebufferobjects import glGenerateMipmap


class Texture:

    def __init__(self, slot, data=None, mipmap=True, flip=False):
        self.texture = 1
        self.textureSlot = slot
        GL.glCreateTextures(GL_TEXTURE_2D, 1, self.texture)
        GL.glBindTexture(GL_TEXTURE_2D, self.texture)
        GL.glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, GL_RGB, GL_UNSIGNED_BYTE, data)

        if mipmap:
            glGenerateMipmap(GL_TEXTURE_2D)
            GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST_MIPMAP_LINEAR)
            GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        else:
            GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        if flip:
            GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, False)

    def bind(self):
        GL.glActiveTexture(GL.GL_TEXTURE0 + self.textureSlot)
        GL.glBindTexture(GL_TEXTURE_2D, self.texture)
        GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        GL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
