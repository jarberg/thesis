#version 330 core
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


varying in vec3 FragPos;
uniform Light test;

void main() {
    vec3 light = test.position;

    float distance = length(light - FragPos);
    float attenuation = 1.0f/(1+0*distance+40*(distance*distance));
    vec3 ret = vec3(1, 0, 0);
    ret = ret*attenuation;
    gl_FragColor = vec4( ret, 1 );
}


