from OpenGL.GL import glGenBuffers, glBindBuffer, glBufferData, glGetIntegerv, GL_CURRENT_PROGRAM, glGetAttribLocation, \
    glBindVertexArray, GL_INT, glVertexAttribIPointer, GL_FLOAT, glVertexAttribPointer, glEnableVertexAttribArray, \
    GL_SHADER_STORAGE_BUFFER, glBindBufferBase
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

    def get_attribute_location(self, name):
        program = glGetIntegerv(GL_CURRENT_PROGRAM)
        return glGetAttribLocation(program, name)

    def bind_vertex_attribute(self, name, data=None, data_len=3, data_type=GL_FLOAT, offset=0, VAO=None):
        if VAO:
            glBindVertexArray(VAO)
        self.bind()
        self.add_data(data)
        attributeSlot = self.get_attribute_location(name)
        if attributeSlot >= 0:
            if data_type == GL_INT:
                glVertexAttribIPointer(attributeSlot, data_len, data_type, offset, None)
            elif data_type == GL_FLOAT:
                glVertexAttribPointer(attributeSlot, data_len, data_type, False, offset, None)

            glEnableVertexAttribArray(attributeSlot)
            self.attributes[name] = attributeSlot


class ShaderStorageBufferObject:

    def __init__(self, buf_type=GL_SHADER_STORAGE_BUFFER, bufferIndex=3,usage=GL_STATIC_DRAW):
        self.slot = glGenBuffers(1)
        self.buffer_type = buf_type
        self.usage = usage
        self.bufferIndex = bufferIndex

    def bind(self):
        glBindBuffer(self.buffer_type, self.slot)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, self.bufferIndex, self.slot)

    def unbind(self, unbindSlot=0):
        glBindBuffer(self.buffer_type, unbindSlot)

    def add_data(self, indata):
        data = flatten_list(indata)
        self.bind()
        glBufferData(self.buffer_type, data.nbytes, data=data, usage=self.usage)
        self.unbind()


