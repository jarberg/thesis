from OpenGL.GL import glGenBuffers, glBindBuffer, glBufferData, GL_SHADER_STORAGE_BUFFER, glBindBufferBase
from OpenGL.raw.GL.VERSION.GL_1_5 import GL_ARRAY_BUFFER, GL_STATIC_DRAW

from utils.objectUtils import flatten_list


class AttributeBuffer:
    def __init__(self, buf_type=GL_ARRAY_BUFFER, usage=GL_STATIC_DRAW):
        self.slot = glGenBuffers(1)
        self.buffer_type = buf_type
        self.usage = usage
        self.attributes = {}

    def bind(self, indice=None):
        glBindBuffer(self.buffer_type, self.slot)
        if indice is not None:
            glBufferData(self.buffer_type, indice.nbytes, indice, self.usage)

    def add_data(self, data):
        glBufferData(self.buffer_type, data.nbytes, data, self.usage)


class ShaderStorageBufferObject:

    def __init__(self, buf_type=GL_SHADER_STORAGE_BUFFER, bufferIndex=3,usage=GL_STATIC_DRAW):
        self.slot = glGenBuffers(1)
        self.buffer_type = buf_type
        self.usage = usage
        self.bufferIndex = bufferIndex

    def bind(self):
        glBindBuffer(self.buffer_type, self.slot)
        glBindBufferBase(self.buffer_type, self.bufferIndex, self.slot)

    def unbind(self, unbindSlot=0):
        glBindBuffer(self.buffer_type, unbindSlot)

    def add_data(self, indata):
        data = flatten_list(indata)
        self.bind()
        glBufferData(self.buffer_type, data.nbytes, data=data, usage=self.usage)
        self.unbind()

