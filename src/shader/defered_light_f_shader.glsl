#version 330
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable



uniform sampler2D pos;
uniform sampler2D norm;
uniform sampler2D albedo;

in vec2 TexCoords;

out vec4 fragCol;

void main() {
    fragCol = vec4(1,0,0,1);//texture2D(norm, TexCoords)*texture2D(pos, TexCoords);
}
