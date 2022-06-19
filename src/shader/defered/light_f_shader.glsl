#version 450
const int MAX_LIGHTS = 500;

struct Light {
    vec3 Position;
    vec3 Color;
};

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
    return inten / (c+a*dist+b*dist*dist);
}

layout(std430, binding = 3) buffer lightBuffer{
    mat4 data_lightBuffer[];
};

uniform sampler2D pos;
uniform sampler2D norm;
uniform sampler2D albedo;

in vec2 TexCoords;
uniform vec3 viewPos;
uniform int lightnum;
out vec4 fragCol;

void main(){
    // retrieve data from G-buffer
    vec3 FragPos = texture(pos, TexCoords).xyz;
    vec3 Normal = texture(norm, TexCoords).xyz;
    vec3 Albedo = texture(albedo, TexCoords).rgb;

    float attenu;
    float angle;
    vec3 lighting = vec3(0);

    for(int i =0; i<lightnum ;i++){
        vec3 light = data_lightBuffer[i][3].xyz;
        vec3 lightDir = light-FragPos;
        attenu = attenuation(light, FragPos);
        angle = lambert(Normal, lightDir);
        lighting += Albedo*angle*attenu;
    }

    fragCol = vec4(lighting, 1);
}