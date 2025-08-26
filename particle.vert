#version 330

in float in_a;
in float in_b;
in float in_delta;
in float in_t;

// Pass unique ID to fragment shader
out float v_particleID;

uniform float u_amplitude;
uniform float u_time;

void main(){
    v_particleID = float(gl_VertexID);

    float t = in_t + u_time;
    float x = 0.5 + 0.5*sin(in_a*t + in_delta);
    float y = 0.5 + 0.5*sin(in_b*t);
    gl_Position = vec4(x*2.0-1.0, y*2.0-1.0, 0.0, 1.0);

    gl_PointSize = 5.0 + u_amplitude * 50.0;
}
