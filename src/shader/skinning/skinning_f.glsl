#version 330
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable

out vec4 color;


in vec3 normals;
in vec3 pos;


void main() {
    // store the fragment position vector in the first gbuffer texture

    vec3 light = vec3(0, 0, -1);

    float dist = (light- pos).length();
    float d = dot(normalize(normals), normalize(light- pos));
    float ret = 0;

    ret = abs(d)*5 / (dist*dist);


    color = vec4(ret,ret,ret, 1);
}



