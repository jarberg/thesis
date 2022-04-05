#version 430 core
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable


const int MAX_JOINTS  = 200;
const int MAX_WEIGHTS = 4;

layout(location = 0) in vec3 a_Position;
layout(location = 1) in vec2 InTexCoords;
layout(location = 2) in vec4 in_joint_indices;
layout(location = 3) in vec4 in_weights;
layout(location = 4) in vec3 inNormal;

uniform mat4 jointTransforms[200];
uniform int skinned;
uniform mat4 projection;
uniform mat4 obj_transform;
uniform mat4 v_matrix;



out vec3 normals;
out vec3 pos;


void main(){
    vec4 poos = vec4(a_Position, 1.0);
    mat4 pv_mat = projection*v_matrix;
    vec4 totalLocalPos = vec4(0.0);
    vec3 totalNormal = vec3(0.0);

    if(skinned==1){
        for(int i =0;i<MAX_WEIGHTS;i++){
            float weight = in_weights[i];
            int jointID = int(in_joint_indices[i]);
            mat4 trans = jointTransforms[jointID];
            float det = determinant(trans);
            vec3 localPos = (trans * poos).xyz;
            totalLocalPos += vec4(localPos*weight, weight);
        }
        normals = inNormal;
        pos = (projection*v_matrix*(vec4(totalLocalPos.xyz, 1))).xyz;
        gl_Position = projection*v_matrix*totalLocalPos;
    }
    else{
        normals = inNormal;
        pos = (pv_mat*obj_transform*poos).xyz;
        gl_Position = pv_mat*obj_transform*poos;
    }
}


