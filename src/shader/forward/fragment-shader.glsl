#version 430
precision mediump float;

float lambert(vec3 N, vec3 L){
  vec3 nrmN = normalize(N);
  vec3 nrmL = normalize(L);
  float result = dot(nrmN, nrmL);
  return max(result, 0.0);
}

float attenuation(vec3 light, vec3 pos){
    float dist = distance(pos,light);
    float inten = 20;
    float a = 1;
    float b = 2;
    float c = 1;
    return max((1 / (c+a*dist+b*dist*dist)), 0);
}

in vec3 a_pos;
in vec3 normal;
in vec2 OutTexCoords;

layout(std430, binding = 3) buffer lightBuffer{
    vec4 data_SSBO[];
};

const int MAX_LIGHTS = 500;
uniform vec3 lights[MAX_LIGHTS];
uniform int lightnum;
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


    for(int i =0; i<lightnum ;i++){
        vec3 light = data_SSBO[i].xyz;
        vec3 lightDir = light-FragPos;
        attenu = attenuation(light, FragPos);
        angle = lambert(normalize(Normal), lightDir);
        lighting += Albedo.xyz*10*angle*attenu;
    }

    FragColor = vec4(lighting, 1);
}


