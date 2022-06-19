#version 430 core
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable

layout(std430, binding = 3) buffer lightBuffer{
    mat4 data_lightBuffer[];
};

in vec3 vertexPos;
flat in int instanceID;

uniform sampler2D geoPosRender;
uniform sampler2D geoColRender;
uniform sampler2D geoNormRender;

uniform int width;
uniform int height;

out vec4 outColor;

float attenuation(vec3 light, vec3 pos){
    float dist = distance(pos,light);
    float inten = 100;
    float a = 1;
    float b = 50;
    float c = 1;
    return inten / (c+a*dist+b*dist*dist);
}
float lambert(vec3 N, vec3 L){
  vec3 nrmN = normalize(N);
  vec3 nrmL = normalize(L);
  float result = dot(nrmN, nrmL);
  return max(result, 0.0);
}

void main() {
    mat4 transform = data_lightBuffer[instanceID];
    vec2 coords = vec2(gl_FragCoord.x/width, gl_FragCoord.y/height);

    vec3 FragPos = texture(geoPosRender, coords).xyz;
    vec3 FragAlbedo = texture(geoColRender, coords).xyz;
    vec3 FragNorm = texture(geoNormRender, coords).xyz;

    float atten = attenuation(transform[3].xyz, FragPos);
    vec3 dir = transform[3].xyz - FragPos;
    float angle = lambert(FragNorm, dir);

    float res = angle*atten;
    outColor = vec4(FragAlbedo*res,1);
}
