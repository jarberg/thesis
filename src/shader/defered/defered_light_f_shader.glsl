#version 450
const int CUBE_SIZE = 5;
const int MAX_LIGHTS = 500;

struct Light {
    vec3 Position;
    vec3 Color;
};

struct Cube {
    int length;
    int[10] lightIDs;
};

int[3] squash_pos(vec3 pos){
    int x,y,z =0;

    if (pos[0] > 0) x = int( floor(pos[0] / CUBE_SIZE));
    else x = int(ceil(pos[0] / CUBE_SIZE));

    if (pos[1] > 0)  y = int(floor(pos[1] / CUBE_SIZE));
    else  y = int(ceil(pos[1] / CUBE_SIZE));

    if (pos[2] > 0) z = int(floor(pos[2] / CUBE_SIZE));
    else z = int(ceil(pos[2] / CUBE_SIZE));

    int[3] res = {x, y, z};

    return res ;
}


float lambert(vec3 N, vec3 L){
  vec3 nrmN = normalize(N);
  vec3 nrmL = normalize(L);
  float result = dot(nrmN, nrmL);
  return max(result, 0.0);
}

float attenuation(vec3 light, vec3 pos){
    float dist = distance(pos,light);
    float inten = 50;
    float a = 1;
    float b = 50;
    float c = 1;
    return max((inten / (c+a*dist+b*dist*dist)-0.01), 0);
}

layout(std430, binding = 3) buffer lightBuffer{
    vec4 data_lightBuffer[];
};


layout(std430, binding = 5) buffer cubeBuffer{
    Cube data_cubeBuffer[10][10][10];
};

uniform Cube cubes[2][2][2];

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
        vec3 light = data_lightBuffer[i].xyz;
        vec3 lightDir = light-FragPos;
        attenu = attenuation(light, FragPos);
        angle = lambert(normalize(Normal), lightDir);
        lighting += 10*angle*attenu;
    }

    vec3 light =vec3(0,3,0);
    vec3 lightDir = light-FragPos;
    attenu = attenuation(light, FragPos);
    angle = lambert(normalize(Normal), lightDir);
    lighting += 10*angle*attenu;

    fragCol = vec4(Albedo*lighting, 1);
}