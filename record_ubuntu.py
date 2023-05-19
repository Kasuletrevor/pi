import pyaudio
import wave
import librosa

class RecordAudio:
    def record(self, rate, channels, width, recordSeconds, fileName):
        # Initialize PyAudio
        pyaud = pyaudio.PyAudio()

        # Chunk size
        CHUNK = 1024
        
        # Record settings
        stream = pyaud.open(
            rate=rate,
            format=pyaud.get_format_from_width(width),
            channels=channels,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        print("Recording audio...")
        
        frames = []
        for i in range(0, int(rate / CHUNK * recordSeconds)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        print("Done recording, now saving file...")
        
        stream.stop_stream()
        stream.close()
        pyaud.terminate()

        wf = wave.open(fileName, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(pyaud.get_sample_size(pyaud.get_format_from_width(width)))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        print("Done recording and file being saved.")

        # Load audio file and extract MFCCs
        audio, sr = librosa.load(fileName, sr=rate, mono=True)
        mfccs = librosa.feature.mfcc(audio, sr=sr, n_mfcc=13)

        # Print the shape of MFCCs
        print("MFCCs shape:", mfccs.shape)

        # Play recorded audio
        print("Playing recorded audio...")
        self.play_audio(fileName)

        print("Audio playback completed!")

    def play_audio(self, fileName):
        # Open the audio file
        wf = wave.open(fileName, 'rb')

        # Initialize PyAudio
        pyaud = pyaudio.PyAudio()

        # Open the stream
        stream = pyaud.open(
            format=pyaud.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )

        # Read data in chunks and play
        CHUNK = 1024
        data = wf.readframes(CHUNK)
        while data:
            stream.write(data)
            data = wf.readframes(CHUNK)

        # Close the stream and PyAudio
        stream.stop_stream()
        stream.close()
        pyaud.terminate()

# Print start of test
print("Audio Recording and MFCCs Test")

# Test of audio recording and playback
recordAudio = RecordAudio()

# Audio Settings
RATE = 16000
CHANNELS = 1
WIDTH = 1
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "recorded_audio.wav"
ITERATIONS = 10

# Run record audio and playback for 10 iterations
for i in range(ITERATIONS):
    print(f"Iteration {i+1}")
    recordAudio.record(RATE, CHANNELS, WIDTH, RECORD_SECONDS, WAVE_OUTPUT_FILENAME)

print("Recording and playback completed!")

