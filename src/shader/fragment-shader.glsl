#version 330 core
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable


struct Material
{
    sampler2D diffuse;
    sampler2D specular;
    float     shininess;
};


struct Light
{
    vec3 position;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;

    float constant;
    float linear;
    float quadratic;
};


//in vec2 TexCoord;
//
//uniform Light test;
//uniform use_tex_diffuse;

in vec2 OutTexCoords;
layout(location = 4) uniform sampler2D tex_diffuse;


void main() {
    //vec3 light = test.position;
    //float distance = length(light - FragPos);
    //float attenuation = 1.0f/(1+0*distance+40*(distance*distance));
    //vec3 ret = vec3(1, 0, 0);
    //ret = ret*attenuation;
    //if(use_tex_diffuse){
    //    gl_FragColor = FragColor = texture(tex_diffuse, TexCoord);
    //}
    //else{
    //     gl_FragColor = vec4( 1, 0.5, 0, 1 );
    //}

    vec4 texColor = texture2D(tex_diffuse, OutTexCoords);

    gl_FragColor = texColor;
}


