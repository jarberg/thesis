#version 330
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable

layout (location = 0) out vec4 gPosition;
layout (location = 1) out vec4 gNormal;
layout (location = 2) out vec4 gAlbedoSpec;


in vec2 TexCoords;
in vec3 g_pos;
in vec3 Normal;

uniform int tex_diffuse_b;
uniform sampler2D tex_diffuse;
uniform sampler2D texture_specular1;

void main() {
    // store the fragment position vector in the first gbuffer texture
    gPosition = vec4(g_pos,1);
    // also store the per-fragment normals into the gbuffer
    gNormal = vec4(normalize(Normal), 1);
    // and the diffuse per-fragment color
    if (tex_diffuse_b != 1){
        gAlbedoSpec = vec4(0.5,0.5,0.5,1);
    }
    else{
        gAlbedoSpec = texture2D(tex_diffuse, TexCoords);
        // store specular intensity in gAlbedoSpec's alpha component
        gAlbedoSpec.a = 1;
    }

}
