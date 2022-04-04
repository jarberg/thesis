#version 430 core
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable


const int MAX_JOINTS  = 200;
const int MAX_WEIGHTS = 4;

layout(location = 0) in vec4 a_Position;
layout(location = 1) in vec2 InTexCoords;
layout(location = 3) in vec4 in_weights;
layout(location = 4) in vec3 inNormal;

layout(location = 1) uniform int skinned;
layout(location = 2) uniform mat4 projection;
layout(location = 3) uniform mat4 obj_transform;
layout(location = 4) uniform mat4 v_matrix;

in ivec4 in_joint_indices;

uniform mat4 jointTransforms[MAX_JOINTS];
uniform float timestamp;
out vec2 TexCoords;
out vec3 normals;
out vec3 pos;
uniform float det0;
uniform float det1;

void main(){
    vec4 poos = vec4(a_Position.xyz, 1.0);
    mat4 pv_mat = projection*v_matrix;
    if(skinned==1){
        vec4 totalLocalPos = vec4(0.0,0.0,0.0,1);
        vec4 totalNormal = vec4(0.0);
        mat4 trans;
        float weight;
        int jointID;
        float det;
        for(int i =0;i<MAX_WEIGHTS;i++){
            weight = in_weights[i];
            if(weight < 0){
                continue;
            }
            jointID = in_joint_indices[i];
            trans = jointTransforms[jointID];
            det = determinant(trans);
            vec3 localPos = (trans * a_Position).xyz;
            totalLocalPos = vec4(localPos*1 ,1);

            vec4 worldNormal = trans * vec4(inNormal, weight);
            totalNormal += worldNormal * weight;
        }

        TexCoords = InTexCoords;
        normals = inNormal;
        pos = (pv_mat*(totalLocalPos)).xyz;
        gl_Position = pv_mat* totalLocalPos;

    }
    else{
        TexCoords = InTexCoords;
        normals = inNormal;
        pos = (pv_mat*obj_transform*a_Position).xyz;
        gl_Position = pv_mat*obj_transform*a_Position;
    }
}


