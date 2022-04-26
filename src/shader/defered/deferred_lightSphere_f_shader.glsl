#version 430 core
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable


layout(std430, binding = 3) buffer lightBuffer{
    mat4 data_lightBuffer[];
};

in vec3 vertexPos;
flat in int instanceID;
flat in mat4 inverseProjView;

uniform sampler2D geoPosRender;
uniform sampler2D geoNormRender;

uniform int width;
uniform int height;

out vec4 outColor;
float attenuation(vec3 light, vec3 pos){
    float dist = distance(pos,light);
    float inten = 50;
    float a = 1;
    float b = 50;
    float c = 1;
    return max((inten / (c+a*dist+b*dist*dist)-0.01), 0);
}
void main() {
    float ret = 0;
    vec2 coords = vec2(gl_FragCoord.x/width, gl_FragCoord.y/height);

    vec3 FragPos = texture(geoPosRender, coords).xyz;
    vec3 FragNorm = texture(geoNormRender, coords).xyz;

    float atten = attenuation(data_lightBuffer[instanceID][3].xyz, FragPos);
    vec3 dir = data_lightBuffer[instanceID][3].xyz - FragPos;
    float angle = max(dot(FragNorm, dir), 0);

    float res = max(angle*atten, 0);
    outColor = vec4(res,res,res,1);
}
