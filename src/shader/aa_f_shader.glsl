#version 330 core


in vec2 OutTexCoords;

//notice the sampler
uniform sampler2DMS screencapture;
uniform int viewport_width;
uniform int viewport_height;

void main(){

    ivec2 up = ivec2(0,1);
    ivec2 down = ivec2(0,-1);
    ivec2 left = ivec2(1,0);
    ivec2 right = ivec2(-1,0);

    ivec2 vpCoords = ivec2(0, 0);
    vpCoords.x = int(OutTexCoords.x*800);
    vpCoords.y = int(OutTexCoords.y*800);
    //do a simple average since this is just a demo
    vec4 origin = texelFetch(screencapture, vpCoords, 0);
    vec4 sample1 = texelFetch(screencapture, vpCoords+up, 0);
    vec4 sample2 = texelFetch(screencapture, vpCoords+down, 0);
    vec4 sample3 = texelFetch(screencapture, vpCoords+left, 0);
    vec4 sample4 = texelFetch(screencapture, vpCoords+right, 0);

    gl_FragColor = (origin+sample1 + sample2 + sample3 + sample4) / 5.0f;
}