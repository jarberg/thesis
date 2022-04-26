from OpenGL.GL import glVertexAttribPointer, glBindBuffer, GL_ARRAY_BUFFER, glEnableVertexAttribArray, GL_RGB, GL_RGBA, \
    glGetUniformLocation, glUniform1i, glPixelStorei, GL_PACK_ALIGNMENT, glBindFramebuffer, GL_READ_FRAMEBUFFER, \
    glReadPixels
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


def lightsplusminus(num, renderer):
    num+=1
    lightcount = max(num, 0)
    res = min(max(4 * (lightcount + 1) * (lightcount + 1), 0), len(renderer.currScene.lights))
    renderer.lightAmount = res
    slot2 = glGetUniformLocation(renderer.lightProgram, "lightnum")
    if slot2 >0:
        glUniform1i(slot2, res)
