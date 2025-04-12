import librosa
import numpy as np

# Source: https://librosa.org/doc/latest/index.html

# The extractFeatures.py contains functions to extract key audio features from music tracks to support the music emotion recognition project. 
# These features are intended to reflect various musical characteristics and are similar to the types of audio analysis Spotify might use to describe tracks.
# These featues are available for songs through the Spotify API.
# Features available for extraction include:
#   - dancability
#   - energy
#   - key
#   - speechiness
#   - acousticness
#   - instrumentalness
#   - liveness
#   - valence
#   - time signature

# Danceability is typically defined as how suitable a track is for dancing which depends on the tempo, rhythmic stability, and periodicity of the audio. 
# We can approximate this by analyzing the rhythmic components. We'll use the tempo and beat frames to compute this.
def compute_danceability(audio, sr):
    onset_env = librosa.onset.onset_strength(y=audio, sr=sr)
    return np.std(onset_env)

# Energy is a measure of the loudness or intensity of the signal. It can be computed using the root mean square energy (RMS).
def compute_energy(audio):
    return np.mean(librosa.feature.rms(y=audio))

# Key refers to the musical key of the track. 
# It can be determined using chroma features, which represent the 12 different pitch classes (C, C#, D, D#, etc.).
def compute_key(audio, sr):
    chroma = librosa.feature.chroma_cqt(y=audio, sr=sr)
    chroma_mean = chroma.mean(axis=1)
    key = np.argmax(chroma_mean)  # Get the most dominant chroma bin
    return key

# Speechiness can be approximated by the spectral centroid, which represents the "brightness" of the sound.
def compute_speechiness(audio, sr):
    zero_crossings = np.mean(librosa.feature.zero_crossing_rate(y=audio))
    spectral_contrast = np.mean(librosa.feature.spectral_contrast(y=audio, sr=sr))
    return zero_crossings * spectral_contrast

# Acousticness can be approximated by looking at the spectral bandwidth (narrower bandwidth often indicates acoustic sounds).
def compute_acousticness(audio):
    spectral_flatness = np.mean(librosa.feature.spectral_flatness(y=audio))
    return 1 - spectral_flatness  # Inverse of flatness

# Instrumentalness is often determined by the presence of vocals. This can be approximated by examining the spectral content.
def compute_instrumentalness(audio):
    harmonics, percussives = librosa.effects.hpss(audio)
    return np.mean(harmonics) / (np.mean(percussives) + 1e-6)

# Liveness can be approximated by analyzing the reverberation or the spectral flatness of the signal.
def compute_liveness(audio, sr):
    spectral_flatness = librosa.feature.spectral_flatness(y=audio)
    liveness = np.mean(spectral_flatness)  # Taking the average
    return liveness

# Valence measures the musical positivity or negativity. Approximated using the spectral features to classify the mood.
def compute_valence(audio, sr):
    brightness = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))
    return (brightness / np.max(brightness)) if np.max(brightness) > 0 else 0

# Tempo is the speed of the track, usually measured in beats per minute (BPM). Extracted using librosa's beat tracking function.
def compute_time_signature(audio, sr):
    onset_env = librosa.onset.onset_strength(y=audio, sr=sr)
    tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sr, onset_envelope=onset_env)
    return len(beat_frames) / (len(audio) / sr / 60)

def extract_features(audio, sr=22050):
    return {
        "danceability": compute_danceability(audio, sr),
        "energy": compute_energy(audio),
        "key": compute_key(audio, sr),
        "speechiness": compute_speechiness(audio, sr),
        "acousticness": compute_acousticness(audio),
        "instrumentalness": compute_instrumentalness(audio),
        "liveness": compute_liveness(audio, sr),
        "valence": compute_valence(audio, sr),
        "time_signature": compute_time_signature(audio, sr)
    }