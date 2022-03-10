#version 330
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable


layout(location = 0) in vec4 a_Position;
layout(location = 1) in vec2 InTexCoords;

out vec2 TexCoords;

void main() {
    TexCoords = InTexCoords;
    gl_Position = a_Position;
}
