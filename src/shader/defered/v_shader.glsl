#version 430 core
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable

layout(location = 0) in vec3 a_Position;
layout(location = 1) in vec2 InTexCoords;
layout(location = 4) in vec3 inNormal;

layout(location = 2) uniform mat4 projection;
layout(location = 3) uniform mat4 obj_transform;
layout(location = 4) uniform mat4 v_matrix;
layout(location = 5) uniform mat3 normal_matrix;

out vec2 TexCoords;
out vec3 g_pos;
out vec3 Normal;

void main() {
    mat4 pv_mat = projection*v_matrix;

    g_pos = (obj_transform*vec4(a_Position,1)).xyz;
    Normal = normal_matrix*inNormal;
    TexCoords = InTexCoords;
    gl_Position = pv_mat*obj_transform*vec4(a_Position,1);
}
