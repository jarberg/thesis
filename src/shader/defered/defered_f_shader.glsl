#version 330
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable

layout (location = 0) out vec4 gPosition;
layout (location = 1) out vec4 gNormal;
layout (location = 2) out vec4 gAlbedoSpec;
layout (location = 6) uniform int tex_diffuse_b;

in vec2 TexCoords;
in vec4 g_pos;
in vec3 Normal;

uniform sampler2D tex_diffuse;
uniform sampler2D texture_specular1;

void main() {
    // store the fragment position vector in the first gbuffer texture
    gPosition = g_pos;
    // also store the per-fragment normals into the gbuffer
    gNormal = vec4(normalize(Normal), 1);
    // and the diffuse per-fragment color
    gAlbedoSpec = texture2D(tex_diffuse, TexCoords);
    // store specular intensity in gAlbedoSpec's alpha component
    gAlbedoSpec.a = 1;//texture2D(texture_specular1, TexCoords).r;

}
