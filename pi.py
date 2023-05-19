import pyaudio
import wave
import subprocess

class RecordAudio:
    def record(self, rate, channels, width, recordSeconds, fileName):
        # Initialize PyAudio
        pyaud = pyaudio.PyAudio()
        
        # Record settings
        stream = pyaud.open(
            rate=rate,
            format=pyaud.get_format_from_width(width),
            channels=channels,
            input=True,
            input_device_index=2,  # Update with the correct device index
        )

        # Print start of recording
        print("Recording audio")

        # Get audio data and save as frame buffer
        frames = []
        for _ in range(0, int(rate * recordSeconds / width)):
            data = stream.read(width)
            frames.append(data)

        # Close the recording stream
        stream.stop_stream()
        stream.close()
        pyaud.terminate()

        # Print end of recording
        print("Done recording, now saving file...")

        # Save recorded audio as a WAV file
        wf = wave.open(fileName, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(pyaud.get_sample_size(pyaud.get_format_from_width(width)))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        print("Done recording and file saved.")
    
    def playAudio(self, fileName):
        # Play audio using aplay
        subprocess.run(["aplay", "-D", "plughw:2", fileName])

# Create an instance of the RecordAudio class
recordAudio = RecordAudio()

# Audio settings
RATE = 16000
CHANNELS = 1  # Mono
WIDTH = 2  # 2 bytes per sample
RECORD_SECONDS = 3

# Repeat the recording and playing 20 times
for i in range(1, 21):
    print(f"Recording and playing #{i}")
    WAVE_OUTPUT_FILENAME = f"recorded_audio_{i}.wav"

    # Record audio for 3 seconds
    recordAudio.record(RATE, CHANNELS, WIDTH, RECORD_SECONDS, WAVE_OUTPUT_FILENAME)

    # Play the recorded audio through output on card 2
    recordAudio.playAudio(WAVE_OUTPUT_FILENAME)

