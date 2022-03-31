#version 330
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable

layout (location = 0) out vec4 color;

in vec2 TexCoords;
uniform sampler2D tex_diffuse;

void main() {
    // store the fragment position vector in the first gbuffer texture
    color = texture2D(tex_diffuse, TexCoords);
}



