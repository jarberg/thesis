#version 330
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable

layout (location = 0) out vec4 gPosition;
layout (location = 1) out vec4 gNormal;
layout (location = 2) out vec4 gAlbedoSpec;

in vec2 TexCoords;
in vec4 g_pos;
in vec3 Normal;

uniform sampler2D texture_diffuse1;
uniform sampler2D texture_specular1;


void main() {
    // store the fragment position vector in the first gbuffer texture
    gPosition = g_pos;
    // also store the per-fragment normals into the gbuffer
    gNormal = vec4(normalize(Normal), 1);
    // and the diffuse per-fragment color
    gAlbedoSpec.rgb = texture2D(texture_diffuse1, TexCoords).rgb;
    // store specular intensity in gAlbedoSpec's alpha component
    gAlbedoSpec.a = texture2D(texture_specular1, TexCoords).r;
}
