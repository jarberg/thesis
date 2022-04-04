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

uniform mat4 jointTransforms[MAX_JOINTS];
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
    vec4 totalNormal = vec4(0.0);

    if(skinned==1){

        for(int i =0;i<MAX_WEIGHTS;i++){
            float weight = in_weights[i];
            int jointID = int(in_joint_indices[i]);
            mat4 trans = jointTransforms[jointID];
            float det = determinant(trans);
            vec3 localPos = (trans/determinant(trans) * poos).xyz;
            totalLocalPos += vec4(localPos*weight, 1);

            vec4 worldNormal = (trans/det) * vec4(inNormal, weight);
            totalNormal += worldNormal * weight;
        }

        vec4 test1 = vec4(vec3(jointTransforms[int(in_joint_indices[1])]/determinant(jointTransforms[int(in_joint_indices[1])]) * poos), 1);
        //vec4 test2 = vec4(vec3(jointTransforms[87]/determinant(jointTransforms[87]) * poos),1);

        gl_Position = pv_mat*test1;
        normals = inNormal;
        pos = (pv_mat*(totalLocalPos)).xyz;
        //gl_Position = pv_mat*poos;//pv_mat* totalLocalPos;

    }
    else{
        normals = inNormal;
        pos = (pv_mat*obj_transform*poos).xyz;
        gl_Position = pv_mat*obj_transform*poos;
    }
}


