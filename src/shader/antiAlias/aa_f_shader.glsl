#version 330 core


in vec2 OutTexCoords;

//notice the sampler
uniform sampler2DMS screencapture;
uniform int viewport_width;
uniform int viewport_height;
uniform int samples;

void main(){

    ivec2 up = ivec2(0,1);
    ivec2 down = ivec2(0,-1);
    ivec2 left = ivec2(1,0);
    ivec2 right = ivec2(-1,0);
    ivec2 coords = ivec2(OutTexCoords[0],OutTexCoords[1]);
    ivec2 vpCoords = ivec2(OutTexCoords[0]*viewport_width, OutTexCoords[1]*viewport_height);
    ivec2 screensize = ivec2(viewport_height,  viewport_width);

    vec4 final_res = vec4(0);
    vec4 blur = vec4(0);
    for(int i =0;i<samples;i++){
        vec4 local_sample = texelFetch(screencapture, vpCoords, i);
        final_res+=local_sample;


    }

    gl_FragColor = final_res/samples;
}