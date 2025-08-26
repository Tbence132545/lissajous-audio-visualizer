# Audio Lissajous Lines

A real-time audio-reactive visualization using Lissajous curves. This program listens to your system's audio output and generates a dynamic, colorful particle network that dances to the music.

https://github.com/user-attachments/assets/95f83ace-7095-47ca-8775-f8bd97f8835d

## Features

- **Real-time Audio Input**: Captures sound directly from your system using a virtual audio device.
- **Dynamic particle count, speed, and brightness**: The number of visible particles adjusts automatically based on the audio amplitude.
- **Smooth Animations**: Lissajous curves move and evolve fluidly in response to the music's rhythm and intensity.
- **Customizable Visuals**: Easily tweak particle counts, colors, and movement speed to create your own unique look.


##  Getting Started - WINDOWS

Follow these instructions to get the project running on your local machine.

### Prerequisites

-   Python 3.10 or newer.
-   A virtual audio device to capture system audio (e.g., [VB-Cable](https://vb-audio.com/Cable/) for Windows, [BlackHole](https://github.com/ExistentialAudio/BlackHole) for macOS, or PulseAudio loopback for Linux).

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/audio-lissajous-lines.git](https://github.com/your-username/audio-lissajous-lines.git)
    cd audio-lissajous-lines
    ```

2.  **Install the required Python packages:**
    Create a `requirements.txt` file with the following content:
    ```txt
    numpy
    sounddevice
    moderngl
    moderngl-window
    ```
    Then, install the dependencies using pip:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1.  **Configure Your Audio Device**
    First, find the ID of your virtual audio input device. You can list available devices with a simple script or check your system's audio settings.

    Open `main.py` and set the `DEVICE_ID` to match your input device.
    ```python
    # Example device ID
    DEVICE_ID = 18
    ```

2.  **Run the Visualization**
    Execute the main script to start the visualizer:
    ```sh
    python main.py
    ```
    Now, play some music on your computer! The visualization will react to any sound playing through your system's output (which is routed through your virtual audio device).


## How it Works

The visualization is generated through a few key steps:

1.  **Audio Capture**: The program continuously listens to the specified audio device and captures audio frames in real-time.
2.  **Amplitude Analysis**: For each frame, the Root Mean Square (RMS) amplitude is calculated. This value represents the "loudness" of the audio at that moment.
3.  **Particle Dynamics**: The RMS amplitude directly controls the number of active particles rendered on the screen. Louder sounds create more particles, while silence reduces them.
4.  **Lissajous Curves**: Each particle follows a parametric path defined by a Lissajous curve equation:
   
    $$
    x(t) = A \sin(a t + \delta), \quad y(t) = B \sin(b t)
    $$
    
6.  **Rendering**: The particle positions are sent to the GPU, where [ModernGL](https://github.com/moderngl/moderngl) efficiently renders them as a network of smooth, blended lines with vibrant color gradients.
