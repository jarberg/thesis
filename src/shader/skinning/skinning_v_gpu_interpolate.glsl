#version 450 core
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable


const int MAX_JOINTS  = 20;
const int MAX_WEIGHTS = 3;

layout(location = 0) in vec4 a_Position;
layout(location = 1) in vec2 InTexCoords;
layout(location = 4) in vec3 inNormal;

layout(location = 1) uniform int skinned;
layout(location = 2) uniform mat4 projection;
layout(location = 3) uniform mat4 obj_transform;
layout(location = 4) uniform mat4 v_matrix;

in ivec3 in_joint_indices;
in vec3 in_weights;

struct Keyframe{
    int joint_num;
    mat4[MAX_JOINTS] transforms;
};

layout(std430, binding = 0) buffer test{
    mat4 variable_array[];
}T;


uniform mat4 jointTransforms[MAX_JOINTS];

out vec2 TexCoords;

uniform int anim_length;
uniform float timestamp;


//int[] getPreviousAndNextFrames(animTime){
//    previousFrameID = int(floor(animTime));
//    nextFrameID = int(ceil(animTime));
//    if(previousFrameID == 0 && previousFrameID == nextFrameID){
//        nextFrameID = 1;
//    }
//    frames = getNextAndPreviousKeyFrames(previousFrameID, nextFrameID);
//    return frames;
//}


//float calculateProgression(self, timestamp1, timestamp2, animTime){
//    totalTime = timestamp2 - timestamp1;
//    currentTime = animTime - timestamp1;
//
//    if (totalTime == 0){
//        return 0;
//    }
//    else{
//        return currentTime / totalTime;
//    }
//
//}


void main() {
    vec4 poos = vec4(a_Position.xyz, 1.0);
    mat4 pv_mat = projection*v_matrix;
    if(skinned==1){
        
        //int[] frame_id = getPreviousAndNextFrames(timestamp);
        //float progression = calculateProgression(frame_id[0], frame_id[1], timestamp);

        vec4 totalLocalPos = vec4(0.0,0.0,0.1,0);
        vec4 totalNormal = vec4(0.0);
        mat4 trans;
        float weight;
        int jointID;
        for(int i =0;i<MAX_WEIGHTS;i++){
            jointID = in_joint_indices[i];
            trans = jointTransforms[i];
            weight = in_weights[i];
            if (weight==0) {
                continue;
            }
            if(jointID < 0 ||weight< 0){
                break;
            }
            vec4 localPos = trans * poos;
            totalLocalPos = localPos * weight;

            vec4 worldNormal = trans * vec4(inNormal, 1.0);
            totalNormal += worldNormal * weight;
        }
        TexCoords = InTexCoords;
        gl_Position = pv_mat*totalLocalPos;
    }
    else{
        TexCoords = InTexCoords;
        gl_Position = projection*v_matrix*T.variable_array[0]*a_Position;
    }
}

