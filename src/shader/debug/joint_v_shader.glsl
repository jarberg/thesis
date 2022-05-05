#version 330
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable

layout(location = 0) in vec4 a_Position;
layout(location = 1) in vec2 InTexCoords;

layout(location = 3) uniform mat4 obj_transform;
uniform mat4 projection;
uniform mat4 v_matrix;
out vec2 OutTexCoords;

void main() {

    OutTexCoords = InTexCoords;
    gl_Position = projection*v_matrix*obj_transform*a_Position;
}
