import sounddevice as sd
import numpy as np
import time
import sys

# A simple script for checking if your setup works or not
#For main.py to run correctly, you have to install VB Cable and set it up as a listening device
# Please find out on which ID your 'CABLE Output' is located
DEVICE_ID = 18

volume_container = [0.0]

def audio_callback(indata, frames, time, status):
    """This callback gets called for each audio chunk."""
    if status:
        print(status, file=sys.stderr)
    # Calculate a simple volume metric (Root Mean Square)
    volume_rms = np.sqrt(np.mean(indata**2))
    volume_container[0] = volume_rms

def run_test():
    """Main function to run the diagnostic test."""
    try:
        
        device_info = sd.query_devices(DEVICE_ID, 'input')
        SAMPLE_RATE = int(device_info['default_samplerate'])
        print(f"Attempting to open device '{device_info['name']}' (ID: {DEVICE_ID}) at {SAMPLE_RATE} Hz")
        stream = sd.InputStream(
            device=DEVICE_ID,
            samplerate=SAMPLE_RATE,
            channels=2,
            callback=audio_callback,
            dtype='float32'
        )
        stream.start()
        print("Stream started. Now printing volume levels...")
        print("Please play some music on your computer now.")
        print("-" * 30)

        # Print the volume for 20 seconds 
        for i in range(200):
            # Create a simple visual bar based on the volume
            volume = volume_container[0]
            bar_length = int(volume * 300) # Scale the bar
            print(f"Volume: {volume:6.4f} |{'#' * bar_length:<50}|", end='\r')
            
            if i == 100:
                print("\n(Now try pausing or stopping the music...)\n", end='')

            time.sleep(0.1)

        print("\n" + "-" * 30)
        print("Test finished.")
        stream.stop()

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please double-check your DEVICE_ID and that your Windows sound output is set to 'CABLE Input'.")

if __name__ == "__main__":
    run_test()
