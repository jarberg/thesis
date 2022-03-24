#version 330 core
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable


layout (std140) uniform Matrices{
    mat4 projection2;
    mat4 view;
};

const int MAX_JOINTS  = 20;
const int MAX_WEIGHTS = 3;



layout(location = 0) in vec4 a_Position;
layout(location = 1) in vec2 InTexCoords;
layout(location = 4) in vec3 inNormal;

layout(location = 1) uniform int skinned;
layout(location = 2) uniform mat4 projection;
layout(location = 3) uniform mat4 obj_transform;
layout(location = 5) uniform mat3 normal_matrix;

in ivec3 in_joint_indices;
in vec3 in_weights;



uniform mat4 jointTransforms[MAX_JOINTS];

out vec2 TexCoords;
out vec4 g_pos;
out vec3 Normal;

void main() {

    if(skinned==1){
        vec4 totalLocalPos = vec4(0.0);
        vec4 totalNormal = vec4(0.0);
        mat4 trans;
        float weight;
        for(int i =0;i<MAX_WEIGHTS;i++){
            trans = jointTransforms[in_joint_indices[i]];
            weight = in_weights[i];

            vec4 localPos = trans * vec4(a_Position.xyz, 1.0);
            totalLocalPos+= localPos*weight;
            vec4 worldNormal = trans * vec4(inNormal, 1.0);
            totalNormal += worldNormal * weight;

        }
        g_pos = projection*totalLocalPos;
        Normal = totalNormal.xyz;
        TexCoords = InTexCoords;
        gl_Position = projection*obj_transform*a_Position;
    }
    else{
        g_pos = obj_transform*a_Position;
        Normal = normal_matrix*inNormal;
        TexCoords = InTexCoords;
        gl_Position = projection*obj_transform*a_Position;
    }
}
