from OpenGL.GL import glGenBuffers, glBindBuffer, glBufferData, GL_SHADER_STORAGE_BUFFER, glBindBufferBase
from OpenGL.GL import GL_ARRAY_BUFFER, GL_STATIC_DRAW

class Buffer:
    def __init__(self, buf_type=GL_ARRAY_BUFFER, usage=GL_STATIC_DRAW):
        self.slot = glGenBuffers(1)
        self.buffer_type = buf_type
        self.usage = usage

    def add_data(self, flat_data):
        self.bind()
        glBufferData(self.buffer_type, flat_data.nbytes, data=flat_data, usage=self.usage)

    def bind(self):
        glBindBuffer(self.buffer_type, self.slot)

    def unbind(self, unbindSlot=0):
        glBindBuffer(self.buffer_type, unbindSlot)


class AttributeBuffer(Buffer):
    def __init__(self, buf_type=GL_ARRAY_BUFFER, usage=GL_STATIC_DRAW):
        super().__init__(buf_type, usage)
        self.attributes = {}

    def bind(self, indice=None):
        super().bind()
        if indice is not None:
            glBufferData(self.buffer_type, indice.nbytes, indice, self.usage)


class ShaderStorageBufferObject(Buffer):

    def __init__(self, buf_type=GL_SHADER_STORAGE_BUFFER, bufferIndex=3, usage=GL_STATIC_DRAW):
        super().__init__(buf_type, usage)
        self.bufferIndex = bufferIndex

    def bind(self):
        super().bind()
        glBindBufferBase(self.buffer_type, self.bufferIndex, self.slot)

