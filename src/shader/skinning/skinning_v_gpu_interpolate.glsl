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
uniform int rowLength;

int[2] getPreviousAndNextFrames(){
    int previousFrameID = int(floor(timestamp));
    int nextFrameID = int(ceil(timestamp));
    if (previousFrameID == 0 && previousFrameID == nextFrameID){
        nextFrameID = 1;
    }
    int[2] frames = {previousFrameID, nextFrameID};
    return frames;
}
float calculateProgression(int keyframe0, int keyframe1){
    float totalTime = keyframe1 - keyframe0;
    float currentTime = timestamp - keyframe0;

    if (totalTime == 0) return 0;
    else return currentTime / totalTime;

}
vec3 get_scale(mat4 m){
    mat4 d= transpose(m);
    float sx = vec3(d[0][0], d[1][0], d[0][2]).length();
    float sy = vec3(d[0][1], d[1][1], d[2][1]).length();
    float sz = vec3(d[2][0], d[2][1], d[2][2]).length();
    return vec3(sx, sy, sz);
}
vec4 slerp(vec4 a, vec4 b, float weight, bool allowFlip){
    float cosAngle = dot(a, b);
    float c1, c2, sinAngle, angle;
    // Linear interpolation for close orientations
    if ((1.0 - abs(cosAngle)) < 0.01){
        c1 = 1.0 - weight;
        c2 = weight;
    }

    else{
        // Spherical interpolation
        angle = acos(abs(cosAngle));
        sinAngle = sin(angle);
        c1 = (sin(angle * (1.0 - weight)) / sinAngle);
        c2 = (sin(angle * weight) / sinAngle);
    }
    // Use the shortest path
    if (allowFlip && (cosAngle < 0.0)){
        c1 = -c1;
    }


    vec4 ret = vec4(0);
    ret[0] = c1 * a[0] + c2 * b[0];
    ret[1] = c1 * a[1] + c2 * b[1];
    ret[2] = c1 * a[2] + c2 * b[2];
    ret[3] = c1 * a[3] + c2 * b[3];

    return ret;
}
vec4 conjungture(vec4 q){
     return vec4(-q[0], -q[1], -q[2], q[3]);
}
float magnitude(vec4 q){
    return sqrt(pow(q[0], 2) +pow(q[1], 2) + pow(q[2], 2) + pow(q[3], 2));
}
vec4 inverse(vec4 q){
    vec4 qk = conjungture(q);
    return qk / magnitude(q);
}
vec4 power(vec4 q, float t){
    for(int i =0;i<4;i++){
       q[i] = pow(q[i], t);
    }
    return q;
}
vec4 matrix_to_quaternion(mat4 n){
    mat4 m = transpose(n);
    float trace = m[0][0] + m[1][1] + m[2][2];
    float qw ,qx ,qy ,qz, S, S1;
    if (trace > 0){
        S = 0.5 / sqrt(trace + 1.0);
        qw = 0.25 / S;
        qx = (m[2][1] - m[1][2]) * S;
        qy = (m[0][2] - m[2][0]) * S;
        qz = (m[1][0] - m[0][1]) * S;
    }
    else if (m[0][0] > m[1][1] && m[0][0] > m[2][2]){
        S = 2.0 * sqrt(1.0 + m[0][0] - m[1][1] - m[2][2]);
        S1 = 1 / S;
        qw = (m[2][1] - m[1][2]) * S1;
        qx = 0.25 * S;
        qy = (m[0][1] + m[1][0]) * S1;
        qz = (m[0][1] - m[2][0]) * S1;
    }

    else if( m[1][1] > m[2][2]){
        S = sqrt(1.0 + m[1][1] - m[0][0] - m[2][2]) * 2.0;
        S1 = 1 / S;
        qw = (m[0][2] - m[2][0]) * S1;
        qx = (m[0][1] + m[1][0]) * S1;
        qy = 0.25 * S;
        qz = (m[1][2] + m[2][1]) * S1 ;
    }
    else{
        S = sqrt(1.0 + m[2][2] - m[0][0] - m[1][1]) * 2;
        S1 = 1 / S;
        qw = (m[1][0] - m[0][1]) * S1;
        qx = (m[0][2] + m[2][0]) * S1;
        qy = (m[1][2] + m[2][1]) * S1;
        qz = 0.25 * S;
    }
    return vec4(qx, qy, qz, qw);
}
mat4 quaternion_to_matrix(vec4 q){
    float sqw, sqx,sqy,sqz, invs, denom;
    float m00, m11 ,m22,m10,m01,m02,m20,m21,m12,tmp1,tmp2;
    sqw = q[0] * q[0];
    sqx = q[1] * q[1];
    sqy = q[2] * q[2];
    sqz = q[3] * q[3];

    denom = (sqx + sqy + sqz + sqw);
    if(denom == 0){
          denom = 1;
    }
    invs = 1 / denom;
    m00 = (sqx - sqy - sqz + sqw) * invs;
    m11 = (-sqx + sqy - sqz + sqw) * invs;
    m22 = (-sqx - sqy + sqz + sqw) * invs;
    tmp1 = q[0] * q[1];
    tmp2 = q[2] * q[3];
    m10 = 2.0 * (tmp1 + tmp2) * invs;
    m01 = 2.0 * (tmp1 - tmp2) * invs;
    tmp1 = q[0] * q[2];
    tmp2 = q[1] * q[3];
    m20 = 2.0 * (tmp1 - tmp2) * invs;
    m02 = 2.0 * (tmp1 + tmp2) * invs;
    tmp1 = q[1] * q[2];
    tmp2 = q[0] * q[3];
    m21 = 2.0 * (tmp1 + tmp2) * invs;
    m12 = 2.0 * (tmp1 - tmp2) * invs;

    mat4 m = mat4(vec4(m00, m10, m20, 0),
                  vec4(m01, m11, m21, 0),
                  vec4(m02, m12, m22, 0),
                  vec4(0, 0, 0, 1));

    return m;
}
vec4 mult_quat_with_quat(vec4 q1, vec4 q2){
    vec4 ret;

    ret[0] = q1[3] * q2[0] + q1[0] * q2[3] + q1[1] * q2[2] - q1[2] * q2[1];  // i
    ret[1] = q1[3] * q2[1] - q1[0] * q2[2] + q1[1] * q2[3] + q1[2] * q2[0];  // j
    ret[2] = q1[3] * q2[2] + q1[0] * q2[1] - q1[1] * q2[0] + q1[2] * q2[3];  // k
    ret[3] = q1[3] * q2[3] - q1[0] * q2[0] - q1[1] * q2[1] - q1[2] * q2[2];  // 1
    return ret;
}
mat4 interpolate(mat4 prevTransfrom, mat4 nexTransform, float progression){

    vec3 trans = prevTransfrom[3].xyz;
    vec3 trans2 = nexTransform[3].xyz;
    mat4 t = mat4(1.0);
    vec3 finalpos = trans * (1 - progression) + trans2 * progression;
    t[3] = vec4(finalpos, 1);
    mat4 r = mat4(0.0);

    vec4 quat1 = matrix_to_quaternion(prevTransfrom);
    vec4 quat2 = matrix_to_quaternion(nexTransform);
    vec4 quat3 = slerp(quat1, quat2, progression, true);

    r = quaternion_to_matrix(quat3);
    float det = determinant(r);
    //r /= sqrt(det);
    return t*r;

}

mat4 calculateCurrentAnimationPose(int jointID){
    int[] frames = getPreviousAndNextFrames();
    float progression = calculateProgression(frames[0], frames[1]);

    mat4 trans0 = K.transforms[rowLength*frames[0]+jointID];
    mat4 trans1 = K.transforms[rowLength*frames[0]+jointID];

    return interpolate(trans0, trans1, progression);
}

void main(){
    vec4 poos = vec4(a_Position, 1.0);

    mat4 pv_mat = projection*v_matrix;
    vec4 totalLocalPos = vec4(0.0);
    vec3 totalNormal = vec3(0.0);

    if(skinned==1){
        for(int i =0;i<MAX_WEIGHTS;i++){
            float weight = in_weights[i];
            int jointID = int(in_joint_indices[i]);
            mat4 trans = calculateCurrentAnimationPose(jointID);
            float det = determinant(trans);
            vec3 localPos = (trans/det * poos).xyz;
            weight = weight*det;
            totalLocalPos += vec4(localPos*weight, weight);
        }
        pos = totalLocalPos.xyz;
        normals = inNormal;
        gl_Position = projection*v_matrix*totalLocalPos;
    }
    else{
        pos = (obj_transform*poos).xyz;
        normals = inNormal;
        gl_Position = pv_mat*obj_transform*poos;
    }
}
