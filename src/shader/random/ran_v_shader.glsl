#version 330 core
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable

layout(location = 0) in vec4 a_Position;
layout(location = 1) in vec2 InTexCoords;

out vec2 OutTexCoords;

void main() {
   OutTexCoords = InTexCoords;
   gl_Position = a_Position;
}
