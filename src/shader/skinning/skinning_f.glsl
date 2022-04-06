#version 330
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable

out vec4 color;

uniform int debug;

in vec3 normals;
in vec3 pos;


void main() {
    // store the fragment position vector in the first gbuffer texture

    vec3 light = vec3(0, 1, 2);
    vec3 dir = light - pos;
    float dist = dir.length();
    float d = -dot(normalize(normals), normalize(dir));
    float ret = 0;

    if(d>0){
       ret = d*(5/(dist*dist));
    }
    if(debug == 1){
        color = vec4(ret+0.5,0,ret+0.5, 1);
    }
    if(debug == 0){
        color = vec4(ret,ret,ret, 1);
    }

}



