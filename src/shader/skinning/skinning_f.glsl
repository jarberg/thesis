#version 330
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable

layout (location = 0) out vec4 color;

in vec2 TexCoords;
in vec3 normals;
in vec3 pos;
uniform sampler2D tex_diffuse;

void main() {
    // store the fragment position vector in the first gbuffer texture

    vec3 light = vec3(0, 1, -1);

    float dist = (light- pos).length();
    float d = dot(normalize(normals), normalize(light- pos));
    float ret = 0;

    if(d > 0){
        ret = d*5 / (dist*dist);
    }

    color = vec4(ret*texture2D(tex_diffuse, TexCoords).xyz, 1);
}



