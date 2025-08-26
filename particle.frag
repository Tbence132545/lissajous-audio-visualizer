#version 330

in float v_particleID;
out vec4 fragColor;
uniform float u_amplitude;

void main(){
    // Make particles circular
    float dist = distance(gl_PointCoord, vec2(0.5));
    if (dist > 0.5) discard;
    float alpha = 1.0 - smoothstep(0.45, 0.5, dist);

    // Unique value per particle
    float uid = mod(v_particleID, 1000.0)/1000.0;

    // Pink to purple gradient
    vec3 color = mix(vec3(1.0,0.2,0.8), vec3(0.6,0.0,1.0), uid);

    // Pulse brightness with music
    color += vec3(u_amplitude);

    fragColor = vec4(color, alpha);
}
