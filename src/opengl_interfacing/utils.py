from OpenGL.GL import glVertexAttribPointer, glBindBuffer, GL_ARRAY_BUFFER, glEnableVertexAttribArray, GL_RGB, GL_RGBA, \
    glGetUniformLocation, glUniform1i, glPixelStorei, GL_PACK_ALIGNMENT, glBindFramebuffer, GL_READ_FRAMEBUFFER, \
    glReadPixels, glGetIntegerv, GL_CURRENT_PROGRAM, glGetAttribLocation, GL_INT, glVertexAttribIPointer, GL_FLOAT, \
    glBindVertexArray
from OpenGL.raw.GLUT import glutGet, GLUT_WINDOW_WIDTH, GLUT_WINDOW_HEIGHT


def get_aspect_ratio():
    return get_window_width() / get_window_height()


def get_window_width():
    return glutGet(GLUT_WINDOW_WIDTH)


def get_window_height():
    return glutGet(GLUT_WINDOW_HEIGHT)


def get_opengl_format(format):
    if format == "JPEG":
        return GL_RGB
    elif format == "PNG":
        return GL_RGBA
    else:
        return GL_RGB


def initAttributeVariable(a_attribute, buffer, size, var_type, offset=0, step=0):
    glBindBuffer(GL_ARRAY_BUFFER, buffer)
    glVertexAttribPointer(a_attribute, size, var_type, True, offset, step)
    glEnableVertexAttribArray(a_attribute)



def bind_vertex_attribute(buffer, name, data=None, data_len=3, data_type=GL_FLOAT, offset=0, VAO=None):
    if VAO:
        glBindVertexArray(VAO)
    buffer.bind()
    buffer.add_data(data)
    attributeSlot = get_attribute_location(name)
    if attributeSlot >= 0:
        if data_type == GL_INT:
            glVertexAttribIPointer(attributeSlot, data_len, data_type, offset, None)
        elif data_type == GL_FLOAT:
            glVertexAttribPointer(attributeSlot, data_len, data_type, False, offset, None)

        glEnableVertexAttribArray(attributeSlot)
        buffer.attributes[name] = attributeSlot


def get_attribute_location(name):
    program = glGetIntegerv(GL_CURRENT_PROGRAM)
    return glGetAttribLocation(program, name)


def lightsplusminus(lightCounter, renderer):
    lightCounter+=0.001
    #lightcount = max(lightCounter, 0)
    res = int(len(renderer.currScene.light_list) * lightCounter)#min(max(4 * (lightcount + 1) * (lightcount + 1), 0), len(renderer.currScene.lights))
    renderer.lightAmount = 10

    return lightCounter