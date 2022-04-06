#version 450 core
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable


const int MAX_JOINTS  = 200;
const int MAX_KEYFRAMES = 200;
const int MAX_WEIGHTS = 4;

layout(location = 0) in vec3 a_Position;
layout(location = 1) in vec2 InTexCoords;
layout(location = 2) in vec4 in_joint_indices;
layout(location = 3) in vec4 in_weights;
layout(location = 4) in vec3 inNormal;

uniform mat4 jointTransforms[MAX_JOINTS];
uniform int skinned;
uniform mat4 projection;
uniform mat4 obj_transform;
uniform mat4 v_matrix;


out vec3 normals;
out vec3 pos;


layout(std430, binding = 2) buffer keyframes{
    mat4[] transforms;
}K;


uniform float timestamp;


void main(){
    vec4 poos = vec4(a_Position, 1.0);
    mat4 pv_mat = projection*v_matrix;
    vec4 totalLocalPos = vec4(0.0);
    vec3 totalNormal = vec3(0.0);
    highp int frameint = int(timestamp);
    if(skinned==1){

        for(int i =0;i<MAX_WEIGHTS;i++){
            float weight = in_weights[i];
            int jointID = int(in_joint_indices[i]);
            mat4 trans = K.transforms[frameint+jointID];
            float det = determinant(trans);
            vec3 localPos = (trans/det * poos).xyz;
            weight=weight/det;
            totalLocalPos += vec4(localPos*weight, weight);

            mat3 trans2 = mat3(trans);
            float det2 = determinant(trans2);
            vec3 localnorm = trans2/det2 * inNormal;
            totalNormal += localnorm*weight;
        }
        pos = totalLocalPos.xyz;
        normals = totalNormal;
        gl_Position = projection*v_matrix*totalLocalPos;
    }
    else{
        pos = (obj_transform*poos).xyz;
        normals = inNormal;
        gl_Position = pv_mat*obj_transform*poos;
    }
}
