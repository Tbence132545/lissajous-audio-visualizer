import numpy as np
import sounddevice as sd
import moderngl
import moderngl_window as mglw
import sys

DEVICE_ID = 18  # 'CABLE Output (VB-Audio Virtual Cable)'
current_amplitude = 0.0

# Detect sample rate
try:
    device_info = sd.query_devices(DEVICE_ID, 'input')
    SAMPLE_RATE = int(device_info['default_samplerate'])
    print(f"Device '{device_info['name']}' found at {SAMPLE_RATE} Hz")
except Exception as e:
    print(f"Error querying device {DEVICE_ID}: {e}")
    sys.exit(1)

# Audio callback
def audio_callback(indata, frames, time, status):
    global current_amplitude
    if status:
        print(status, file=sys.stderr)
    rms = np.sqrt(np.mean(indata**2))
    current_amplitude = rms

# Audio stream
try:
    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        device=DEVICE_ID,
        channels=2,
        dtype='float32',
        callback=audio_callback,
        latency='low',
    )
    stream.start()
    print("Audio stream started successfully.")
except Exception as e:
    print(e)
    sys.exit(1)

# ModernGL class 
class AudioLissajousLines(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Audio Lissajous Lines"
    window_size = (800, 600)
    resource_dir = '.'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ctx.enable(moderngl.PROGRAM_POINT_SIZE)
        self.time = 0.0

        self.NUM_PARTICLES_MAX = 200 # max particles
        self.NUM_PARTICLES_BASE = 50  # base particles

        # Particle parameters
        self.particles = np.zeros(self.NUM_PARTICLES_MAX, dtype=[('a','f4'),('b','f4'),('delta','f4'),('t','f4')])
        self.particles['a'] = np.random.uniform(1, 5, self.NUM_PARTICLES_MAX)
        self.particles['b'] = np.random.uniform(1, 5, self.NUM_PARTICLES_MAX)
        self.particles['delta'] = np.random.uniform(0, 2 * np.pi, self.NUM_PARTICLES_MAX)
        self.particles['t'] = np.random.uniform(0, 2 * np.pi, self.NUM_PARTICLES_MAX)

        self.prev_positions = np.zeros((self.NUM_PARTICLES_MAX, 2), dtype='f4')
        self.line_buffer = self.ctx.buffer(reserve=self.NUM_PARTICLES_MAX * 2 * 3 * 4)

        # Line shader
        self.line_program = self.ctx.program(
            vertex_shader="""
            #version 330
            in vec2 in_pos;
            in float in_uid;
            out float v_uid;
            void main() {
                gl_Position = vec4(in_pos*2.0-1.0, 0.0, 1.0);
                v_uid = in_uid;
            }
            """,
            fragment_shader="""
            #version 330
            in float v_uid;
            uniform float u_amplitude;
            out vec4 fragColor;
            void main() {
                vec3 color = mix(vec3(1.0,0.2,0.8), vec3(0.6,0.0,1.0), v_uid);
                color += vec3(u_amplitude);
                fragColor = vec4(color, 1.0);
            }
            """
        )

        self.vao = self.ctx.vertex_array(
            self.line_program,
            [(self.line_buffer, '2f 1f', 'in_pos', 'in_uid')]
        )

        self.smoothed_amp = 0.0
        self.active_particles = self.NUM_PARTICLES_BASE  # smoothed particle count

    def on_render(self, time, frame_time):
        global current_amplitude
        threshold = 0.005
        amp = max(0.0, current_amplitude - threshold)
        alpha = 0.1
        self.smoothed_amp = (1 - alpha) * self.smoothed_amp + alpha * amp
        audio_gain = 300.0
        current_speed = self.smoothed_amp * audio_gain
        self.time += frame_time * current_speed

        # compute target number of active particles based on amplitude
        amp_scaled = min(1.0, self.smoothed_amp * 10.0) ** 0.3  # lower exponent, more sensitive at low values
        target_particles = int(self.NUM_PARTICLES_BASE + amp_scaled * (self.NUM_PARTICLES_MAX - self.NUM_PARTICLES_BASE))


        # Smooth particle count change
        self.active_particles += (target_particles - self.active_particles) * 0.05
        NUM_ACTIVE = int(self.active_particles)

        vertices = np.zeros((NUM_ACTIVE*2, 3), dtype='f4')

        for i in range(NUM_ACTIVE):
            t = self.particles['t'][i] + self.time
            x = 0.5 + 0.5*np.sin(self.particles['a'][i]*t + self.particles['delta'][i])
            y = 0.5 + 0.5*np.sin(self.particles['b'][i]*t)
            uid = i / self.NUM_PARTICLES_MAX

            vertices[2*i] = [self.prev_positions[i,0], self.prev_positions[i,1], uid]
            vertices[2*i+1] = [x, y, uid]

            self.prev_positions[i] = [x, y]

        self.line_buffer.write(vertices.tobytes())

        # Render lines
        self.ctx.screen.use()
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE)
        self.line_program['u_amplitude'].value = 0.05 + self.smoothed_amp*0.5
        self.vao.render(mode=moderngl.LINES, vertices=NUM_ACTIVE*2)

if __name__ == "__main__":
    mglw.run_window_config(AudioLissajousLines)
