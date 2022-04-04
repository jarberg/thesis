#version 330
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable

layout(location = 0) in vec4 a_Position;

layout(location = 2) uniform mat4 projection;
layout(location = 3) uniform mat4 obj_transform;
layout(location = 4) uniform mat4 v_matrix;



void main() {
 gl_Position = projection*v_matrix*obj_transform*a_Position;
}
