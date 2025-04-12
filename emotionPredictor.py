import sounddevice as sd
import numpy as np
import pickle
from extractFeatures import *
import socket
import pandas as pd

# Load the trained model and scaler
with open("SVM_model.pkl", "rb") as f:
    clf = pickle.load(f)

# Load the scaler
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Load the saved label encoder
with open('label_encoder.pkl', 'rb') as f:
    loaded_label_encoder = pickle.load(f)

# Create the reverse mapping
reverse_mapping = {idx: label for idx, label in enumerate(loaded_label_encoder.classes_)}

# Define the sampling rate and audio duration
sampling_rate = 22050  # 22.05 kHz (standard for audio processing)
duration = 5  # Duration of the audio segment to capture in seconds

# Function to record and predict (in real-time) the perceived emotion from microphone audio input in 5-second increments
# https://python-sounddevice.readthedocs.io/en/0.5.1/usage.html#recording
def predict_emotion():
    print("Recording...")
    # Record audio for the specified duration
    audio = sd.rec(int(sampling_rate * duration), samplerate=sampling_rate, channels=1, dtype='float32')
    sd.wait()  # Wait until recording is done

    # Extract features from the recorded audio
    features = extract_features(audio.flatten())

    # Scale the features using the saved scaler
    features_df = pd.DataFrame([features])  # Convert to DataFrame
    features_scaled = scaler.transform(features_df)

    # Predict the emotion: fearful, pumped up, relaxing, sad
    output = clf.predict(features_scaled)
    emotion = output[0]
    emotion_string = reverse_mapping.get(emotion, "unknown")
    print(f"Predicted Emotion: {emotion_string}")

    return emotion_string


# Setup Connection to UNITY 3D
# Adapted from: https://github.com/ConorZAM/Python-Unity-Socket
host, port = "127.0.0.1", 25001
# SOCK_STREAM means TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # Connect to the server and send the data
    sock.connect((host, port))
    # Continuously record and predict
    while True:
        predicted_emotion = predict_emotion().strip()
        # Send the emotion to Unity
        sock.sendall(predicted_emotion.encode("utf-8"))
finally:
    sock.close()
