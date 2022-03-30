#version 400 core
#extension GL_ARB_explicit_uniform_location : enable
#extension GL_ARB_explicit_attrib_location : enable

#define PI 3.14159265
out vec4 FragColor;

in vec2 OutTexCoords;

uniform vec2 vectors[4*4];



float rand(vec2 c){
	return fract(sin(dot(c.xy ,vec2(12.9898,78.233))) * 43758.5453);
}

float noise(vec2 p, float freq ){
	float unit = 800/freq;
	vec2 ij = floor(p/unit);
	vec2 xy = mod(p,unit)/unit;
	xy = 3.*xy*xy-2.*xy*xy*xy;
	//xy = .5*(1.-cos(PI*xy));
	float a = rand((ij+vec2(0.,0.)));
	float b = rand((ij+vec2(1.,0.)));
	float c = rand((ij+vec2(0.,1.)));
	float d = rand((ij+vec2(1.,1.)));
	float x1 = mix(a, b, xy.x);
	float x2 = mix(c, d, xy.x);
	return mix(x1, x2, xy.y);
}

float pNoise(vec2 p, int res){
	float persistance = .5;
	float n = 1.;
	float normK = 1.;
	float f = 100.;
	float amp = 4.;
	int iCount = 0;
	for (int i = 0; i<50; i++){
		n+=amp*noise(p, f);
		f*=2.;
		normK+=amp;
		amp*=persistance;
		if (iCount == res) break;
		iCount++;
	}
	float nf = n/normK;
	return nf*nf*nf*nf;
}


vec2 start_end(vec2 _input){



    return vec2(1,1);
}

vec3 random3(vec3 c) {
	float j = 4096.0*sin(dot(c,vec3(17.0, 59.4, 15.0)));
	vec3 r;
	r.z = fract(512.0*j);
	j *= .125;
	r.x = fract(512.0*j);
	j *= .125;
	r.y = fract(512.0*j);
	return r-0.5;
}

/* skew constants for 3d simplex functions */
const float F3 =  0.3333333;
const float G3 =  0.1666667;

/* 3d simplex noise */
float simplex3d(vec3 p) {
	 /* 1. find current tetrahedron T and it's four vertices */
	 /* s, s+i1, s+i2, s+1.0 - absolute skewed (integer) coordinates of T vertices */
	 /* x, x1, x2, x3 - unskewed coordinates of p relative to each of T vertices*/

	 /* calculate s and x */
	 vec3 s = floor(p + dot(p, vec3(F3)));
	 vec3 x = p - s + dot(s, vec3(G3));

	 /* calculate i1 and i2 */
	 vec3 e = step(vec3(0.0), x - x.yzx);
	 vec3 i1 = e*(1.0 - e.zxy);
	 vec3 i2 = 1.0 - e.zxy*(1.0 - e);

	 /* x1, x2, x3 */
	 vec3 x1 = x - i1 + G3;
	 vec3 x2 = x - i2 + 2.0*G3;
	 vec3 x3 = x - 1.0 + 3.0*G3;

	 /* 2. find four surflets and store them in d */
	 vec4 w, d;

	 /* calculate surflet weights */
	 w.x = dot(x, x);
	 w.y = dot(x1, x1);
	 w.z = dot(x2, x2);
	 w.w = dot(x3, x3);

	 /* w fades from 0.6 at the center of the surflet to 0.0 at the margin */
	 w = max(0.7 - w, 0.0);

	 /* calculate surflet components */
	 d.x = dot(random3(s), x);
	 d.y = dot(random3(s + i1), x1);
	 d.z = dot(random3(s + i2), x2);
	 d.w = dot(random3(s + 1.0), x3);

	 /* multiply d by w^4 */
	 w *= w;
	 w *= w;
	 d *= w;

	 /* 3. return the sum of the four surflets */
	 return dot(d, vec4(52.0));
}

/* const matrices for 3d rotation */
const mat3 rot1 = mat3(-0.37, 0.36, 0.85,-0.14,-0.93, 0.34,0.92, 0.01,0.4);
const mat3 rot2 = mat3(-0.55,-0.39, 0.74, 0.33,-0.91,-0.24,0.77, 0.12,0.63);
const mat3 rot3 = mat3(-0.71, 0.52,-0.47,-0.08,-0.72,-0.68,-0.7,-0.45,0.56);

/* directional artifacts can be reduced by rotating each octave */
float simplex3d_fractal(vec3 m) {
    return   0.5333333*simplex3d(m*rot1)
			+0.2666667*simplex3d(2.0*m*rot2)
			+0.1333333*simplex3d(4.0*m*rot3)
			+0.0666667*simplex3d(8.0*m);
}

uniform float timeI;

void main() {



    // gradient
    //FragColor = vec4(vec3(0+gl_FragCoord.y/800),1);

    //perlin noise
    //float res = pNoise(gl_FragCoord.xy, 1);

    //animated noise
    vec2 p = gl_FragCoord.xy/800;
	vec3 p3 = vec3(p, timeI*0.025);

	float value;

	if (p.x <= 0.5) {
		value = simplex3d(p3*100);
	} else {
		value = simplex3d_fractal(p3*8.0+8.0);
	}
	//value = simplex3d_fractal(p3*8.0+8.0);
	value = 0.5 + 0.5*value;
	//value *= smoothstep(0.0, 0.1, (p.x)); // hello, iq :)
	//value *= smoothstep(1.0, 0.9, (p.x));
	//value *= smoothstep(0.0, 0.1, (p.y));
	//value *= smoothstep(1.0, 0.9, (p.y));

    vec3 res = vec3(value);

    FragColor = vec4(res ,1);
}

