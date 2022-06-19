#version 430
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable

precision mediump float;
const int MAX_LIGHTS = 500;


float lambert(vec3 N, vec3 L){
  vec3 nrmN = normalize(N);
  vec3 nrmL = normalize(L);
  float result = dot(nrmN, nrmL);
  return max(result, 0.0);
}

float attenuation(vec3 light, vec3 pos){
    float dist = distance(pos,light);
    float inten = 100;
    float a = 1;
    float b = 50;
    float c = 1;
    return max((inten / (c+a*dist+b*dist*dist)-0.01), 0);
}
in vec3 a_pos;
in vec3 normal;
in vec2 OutTexCoords;

layout(std430, binding = 3) buffer lightBuffer{
    mat4 data_lightBuffer[];
};

layout(location = 4)uniform int lightnum;

uniform int tex_diffuse_b;
uniform sampler2D tex_diffuse;

out vec4 FragColor;


void main() {

    vec4 Albedo;
    if(tex_diffuse_b == 1){
        Albedo = texture2D(tex_diffuse, OutTexCoords);
    }
    else{
        Albedo = vec4(1,1,1,1);
    }
    vec3 FragPos = a_pos;
    vec3 Normal = normal;

    float attenu;
    float angle;
    vec3 lighting = vec3(0);

    for(int i=0; i<lightnum ;i++){
        vec3 light_pos = data_lightBuffer[i][3].xyz;
        vec3 lightDir = light_pos-FragPos;
        attenu = attenuation(light_pos, FragPos);
        angle = lambert(normalize(Normal), lightDir);
        lighting += Albedo.xyz*angle*attenu;
    }

    FragColor = vec4(lighting, 1);
}


