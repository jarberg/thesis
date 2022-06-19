#version 430 core
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable

layout(location = 0) in vec3 a_Position;
layout(location = 4) in vec3 inNormal;

layout(location = 2) uniform mat4 projection;
layout(location = 4) uniform mat4 v_matrix;

uniform int light_id;

layout(std430, binding = 3) buffer lightBuffer{
    mat4 data_lightBuffer[];
};
out vec3 vertexPos;


void main() {
    mat4 pv_mat = projection*v_matrix;

    gl_Position = pv_mat*data_lightBuffer[light_id]*vec4(a_Position,1);
    vertexPos = (data_lightBuffer[light_id]*vec4(a_Position,1)).xyz;

}
