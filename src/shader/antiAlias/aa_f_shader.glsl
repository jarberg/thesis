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
    vpCoords.x = int(OutTexCoords.x*400);
    vpCoords.y = int(OutTexCoords.y*400);

    //do a simple average since this is just a demo
    vec4 sample1 = texelFetch(screencapture, vpCoords, 0);
    vec4 sample2 = texelFetch(screencapture, vpCoords, 1);
    vec4 sample3 = texelFetch(screencapture, vpCoords, 2);
    vec4 sample4 = texelFetch(screencapture, vpCoords, 3);
    vec4 sample5 = texelFetch(screencapture, vpCoords, 4);
    vec4 sample6 = texelFetch(screencapture, vpCoords, 5);
    vec4 sample7 = texelFetch(screencapture, vpCoords, 6);
    vec4 sample8 = texelFetch(screencapture, vpCoords, 7);
    vec4 sample9 = texelFetch(screencapture, vpCoords, 8);
    vec4 sample10 = texelFetch(screencapture, vpCoords, 9);
    vec4 sample11 = texelFetch(screencapture, vpCoords, 10);
    vec4 sample12 = texelFetch(screencapture, vpCoords, 11);

    gl_FragColor = (sample1 + sample2 + sample3 + sample4 + sample5 + sample6 + sample7 + sample8 + sample9 + sample10 + sample11) / 12.0f;
}