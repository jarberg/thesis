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

in vec4 a_pos;
in vec2 OutTexCoords;
layout(location = 4) uniform sampler2D tex_diffuse;
layout(location = 6) uniform int tex_diffuse_b;

layout(location = 7) uniform sampler2D depthTexture;

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

    float frontDepth = texture(depthTexture, gl_FragCoord.xy).r;
    if (gl_FragCoord.z <= frontDepth) {
            //discard;
    }

    vec4 texColor = vec4(1,0,0,1);
    if(tex_diffuse_b==1){
        texColor = texture2D(tex_diffuse, OutTexCoords);
    }
    else{
        texColor = vec4(1,0,0,1);
    }
    gl_FragColor = texColor;
}


