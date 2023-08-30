import sounddevice as sd
import numpy as np

# Get a list of available audio devices
devices = sd.query_devices()

# Iterate over each device
for device in devices:
    print("Playing sound on device:", device['name'])

    # Set the desired device for output
    sd.default.device = device['name']
    print(sd.default.samplerate)

    # Generate a 10-second 440Hz sine wave signal
    duration = 10  # seconds
    frequency = 440  # Hz
    t = np.linspace(0, duration, int(duration * sd.default.samplerate), endpoint=False)
    signal = np.sin(2 * np.pi * frequency * t)

    # Play the generated signal
    sd.play(signal, samplerate=sd.default.samplerate)
    sd.wait()  # Wait for sound to finish playing on the current device

    print("Sound playback completed.")
