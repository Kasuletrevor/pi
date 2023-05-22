import pyaudio
import wave
import librosa
import numpy as np

import tflite_runtime.interpreter as tflite

TF_LITE_MODEL_FILE_NAME = "tf_lite_model.tflite"
interpreter = tflite.Interpreter(model_path=TF_LITE_MODEL_FILE_NAME)

intents = ["alarm off", "alarm on", "camera off", "camera on", "door close", "door open", "fan decrease", "fan increase", "fan off", "fan on", "fridge off", "fridge on", "lights off", "lights on", "speaker decrease", "speaker increase", "speaker off", "speaker on", "tv off", "tv on"]

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
		signal = librosa.util.fix_length(audio, size=sr*4)
		mfcc_features = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=10,
											 n_fft=2048, fmin=100, hop_length=512)
		mfc = mfcc_features.T
		mfc = np.expand_dims(mfc, axis=-1)
		mfc = np.expand_dims(mfc, axis=0)
		print(mfc.shape)

		interpreter.allocate_tensors()
		input_details = interpreter.get_input_details()
		output_details = interpreter.get_output_details()
		print("Input Shape:", input_details[0]['shape'])
		print("Input Type:", input_details[0]['dtype'])
		print("Output Shape:", output_details[0]['shape'])
		print("Output Type:", output_details[0]['dtype'])

		interpreter.set_tensor(input_details[0]['index'], mfc)
		interpreter.invoke()
		tflite_model_predictions = interpreter.get_tensor(output_details[0]['index'])
		print("Prediction results shape:", tflite_model_predictions.shape)
		prediction_classes = np.argmax(tflite_model_predictions, axis=1)
		print(f"The prediction is class: {prediction_classes} and that is: {intents[int(prediction_classes)]}")

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
WIDTH = 2
RECORD_SECONDS = 4
WAVE_OUTPUT_FILENAME = "recorded_audio.wav"
ITERATIONS = 10

# Run record audio and playback for 10 iterations
for i in range(ITERATIONS):
	print(f"Iteration {i+1}")
	recordAudio.record(RATE, CHANNELS, WIDTH, RECORD_SECONDS, WAVE_OUTPUT_FILENAME)

print("Recording and playback completed!")

