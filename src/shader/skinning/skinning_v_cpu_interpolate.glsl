#version 430 core
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable


const int MAX_JOINTS  = 20;
const int MAX_WEIGHTS = 3;

layout(location = 0) in vec4 a_Position;
layout(location = 1) in vec2 InTexCoords;
layout(location = 3) in vec3 in_weights;
layout(location = 4) in vec3 inNormal;

layout(location = 1) uniform int skinned;
layout(location = 2) uniform mat4 projection;
layout(location = 3) uniform mat4 obj_transform;
layout(location = 4) uniform mat4 v_matrix;

in ivec3 in_joint_indices;

uniform mat4 jointTransforms[MAX_JOINTS];
uniform float timestamp;
out vec2 TexCoords;

uniform float det0;
uniform float det1;

void main() {
    vec4 poos = vec4(a_Position.xyz, 1.0);
    mat4 pv_mat = projection*v_matrix;
    if(skinned==1){
        vec4 totalLocalPos = vec4(0.0,0.0,0.0,1);
        vec4 totalNormal = vec4(0.0);
        mat4 trans;
        float weight;
        int jointID;
        for(int i =0;i<MAX_WEIGHTS;i++){
            jointID = in_joint_indices[i];
            trans = jointTransforms[i];
            weight = in_weights[i];
            if(weight < 0){
                continue;
            }
            vec3 localPos = vec3(trans * a_Position);
            totalLocalPos += vec4(localPos*weight,weight);

            vec4 worldNormal = trans * vec4(inNormal, 1.0);
            totalNormal += worldNormal * weight;
        }
        vec4 test1 = vec4(vec3(jointTransforms[0]/sqrt(det0) * a_Position)*in_weights[0],in_weights[0]);
        vec4 test2 = vec4(vec3(jointTransforms[1]/sqrt(det1) * a_Position)*in_weights[1],in_weights[1]);
        TexCoords = InTexCoords;
        gl_Position = pv_mat*(test1+test2);
    }
    else{
        TexCoords = InTexCoords;
        gl_Position = pv_mat*obj_transform*a_Position;
    }
}


