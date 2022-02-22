#version 120

varying out vec3 FragPos;
void main() {
    FragPos = vec3(gl_Vertex[0],gl_Vertex[1],gl_Vertex[2]);
    gl_Position = gl_Vertex;
}