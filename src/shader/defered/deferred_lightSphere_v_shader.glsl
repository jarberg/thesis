#version 430 core
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable

layout(location = 0) in vec3 a_Position;
layout(location = 4) in vec3 inNormal;

layout(location = 2) uniform mat4 projection;
layout(location = 4) uniform mat4 v_matrix;

layout(std430, binding = 3) buffer lightBuffer{
    mat4 data_lightBuffer[];
};
out vec3 vertexPos;
flat out int instanceID;
flat out mat4 inverseProjView ;


void main() {
    mat4 pv_mat = projection*v_matrix;

    gl_Position = pv_mat*data_lightBuffer[gl_InstanceID]*vec4(a_Position,1);
    instanceID = gl_InstanceID;
    vertexPos = (data_lightBuffer[gl_InstanceID]*vec4(a_Position,1)).xyz;
    inverseProjView = inverse(pv_mat);
}
