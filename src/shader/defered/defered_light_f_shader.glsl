#version 330


uniform sampler2D pos;
uniform sampler2D norm;
uniform sampler2D albedo;

in vec2 TexCoords;
uniform vec3 viewPos;
struct Light {
    vec3 Position;
    vec3 Color;
};
const int MAX_LIGHTS = 2000;
uniform Light lights[MAX_LIGHTS];


out vec4 fragCol;

float lambert(vec3 N, vec3 L)
{
  vec3 nrmN = normalize(N);
  vec3 nrmL = normalize(L);
  float result = dot(nrmN, nrmL);
  return max(result, 0.0);
}

float inverseSquare(vec3 lightDir){
    float dist = lightDir.length();


    return max(1/(dist*dist*dist)-0.00001, 0);
}

void main()
{
    // retrieve data from G-buffer
    vec3 FragPos = texture(pos, TexCoords).rgb;
    vec3 Normal = texture(norm, TexCoords).rgb;
    vec3 Albedo = texture(albedo, TexCoords).rgb;
    float Specular = texture(albedo, TexCoords).a;

    vec3 light = vec3(0,2,0);

    // then calculate lighting as usual
    vec3 lighting = Albedo * 0.1; // hard-coded ambient component
    vec3 viewDir = normalize(viewPos - FragPos);

    // diffuse
    vec3 lightDir = normalize(light  - FragPos);
    vec3 diffuse = max(dot(Normal, lightDir), 0.0) * Albedo ;
    lighting += diffuse;

    float attenuation = inverseSquare(light  - FragPos);
    float lightintensity = 50*attenuation;
    float angle = lambert(normalize(Normal), lightDir);


    fragCol = vec4(Albedo*angle*lightintensity, 1);
}