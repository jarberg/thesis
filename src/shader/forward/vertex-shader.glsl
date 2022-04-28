#version 430
precision mediump float;

in vec3 a_Position;
in vec3 inNormal;
in vec2 InTexCoords;


uniform mat4 projection;
uniform mat4 obj_transform;
uniform mat3 normal_matrix;
uniform mat4 v_matrix;
uniform int lightnum;

out vec2 OutTexCoords;
out vec3 a_pos;
out vec3 normal;

void main() {
    vec4 poos = vec4(a_Position,1);
    a_pos = vec3(obj_transform*poos);
    normal = normal_matrix*inNormal;
    OutTexCoords = InTexCoords;
    gl_Position = projection*v_matrix*obj_transform*poos;
}
