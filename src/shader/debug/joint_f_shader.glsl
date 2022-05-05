#version 330
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable

layout (location = 0) out vec4 col;
void main() {
    col = vec4(1,0,0,1);
}
