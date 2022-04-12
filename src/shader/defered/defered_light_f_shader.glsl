#version 330


uniform sampler2D pos;
uniform sampler2D norm;
uniform sampler2D albedo;

in vec2 TexCoords;

out vec4 fragCol;

void main() {
    //fragCol = texture2D(norm, TexCoords)*texture2D(pos, TexCoords)*texture2D(albedo, TexCoords);
    vec3 light = vec3(0, 1, 0);
    vec3 dir = light - texture2D(pos, TexCoords).xyz;
    float dist = dir.length();
    float d = -dot(normalize(texture2D(norm, TexCoords).xyz), normalize(dir));
    float ret = 0;

    if(d>0){
       ret = d*(5/(dist*dist));
    }

    fragCol = texture2D(albedo, TexCoords);
}
