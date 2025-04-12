# 🎶 Music Emotion Recognition with Unity Animation

This project uses real-time microphone input to classify the emotion of music and animates a Mixamo character in Unity based on the predicted emotion. The classifier was trained on a custom dataset created from Spotify playlists.

---

## ⬇️ Download the Project

You can download the complete project (Unity + Python + dataset) as a ZIP file here:  
📦 **[Download Project ZIP](https://drive.google.com/drive/folders/19CEmJ9JOHoZgU61ov-vQijAaCaYoqfAT?usp=drive_link)**

> ⚠️ **Note**: Make sure to extract the ZIP file before running the project.

---

## 📁 Project Structure

### Python
- `emotionPredictor.py` — Main script: records audio, extracts features, predicts emotion, and sends the result to Unity.
- `Create_Data.ipynb` — Script to extract features from `.mp3` files and generate the training dataset.
- `extractFeatures.py` — Functions for audio feature extraction.
- `TrainModels.ipynb` — Jupyter notebook to train and save the ML model.
- `data/features_full_v7.csv` — Final dataset created from Spotify playlists.
- `requirements.txt` — Python dependencies.
- `.venv` — Pre-configured virtual environment (included in the zip).

### Unity
- `Demo419_v8` — Unity project that receives emotion predictions and animates accordingly.
- `Assets/animationStateController.cs` - C# script that runs a TCP server to receive emotion data from the Python script.

---

## ▶️ How to Run the Project

### 1. Unity Setup
1. Download Unity: [https://unity.com/download](https://unity.com/download)
2. Open Unity Hub → **Add** → Select the `Demo419_v8` folder.
3. Once the project loads, click the **Play** button to start the scene.
4. In the Unity editor, make sure to switch to the Game tab to view the character animation.
5. Unity must be running *before* you launch the Python script.
6. Make sure Unity is the active window — animations won’t render otherwise.

### 2. Python Setup

The project includes a pre-configured `.venv` virtual environment that uses Python 3.10.16.

1. **Activate the virtual environment**:
```bash
source .venv/bin/activate
```
2. **If activation fails, install dependencies manually** (make sure you're using Python 3.10):
```bash
pip install -r requirements.txt
```
3. **Run the emotion prediction script**:
```bash
python emotionPredictor.py
```
4. **To stop the program, press `Ctrl+C` to raise a `KeyboardInterrupt`**

## 🧠 Machine Learning Model

- The custom dataset was generated using `Create_Data.ipynb`, which extracted audio features from `.mp3` files downloaded from emotion-tagged Spotify playlists.
- Feature extraction was performed using helper functions in `extractFeatures.py`.
- The dataset is saved as `data/features_full_v7.csv` and used to train a classifier in `TrainModel.ipynb`.
- The trained model is loaded in `emotionPredictor.py` to make real-time predictions.

Emotions supported:
- 😠 Angry  
- 🕺 Pumped-Up  
- 😢 Sad  
- 🧘 Relaxing

---

## 🎯 Self-Evaluation

Compared to the original project proposal, we have made solid progress on several key goals while making some simplifications due to time and technical constraints.



✅ **Accomplished:**
- Built a custom dataset from Spotify music using feature extraction with `librosa`.
- Successfully trained a music emotion classifier capable of distinguishing between 4 emotion categories: sad, relaxing, fearful, and pumped up.
- Built a real-time pipeline that records music from a microphone, predicts its emotional tone, and sends the result to Unity.
- Integrated a Mixamo character into Unity that responds with different animations depending on the predicted emotion.
- Demonstrated end-to-end interaction between audio input and Unity animation in real time.


⚠️ **Notes and Limitations:**
- While we proposed using LSTMs to capture the temporal nature of music, we opted for a simpler ML model due to dataset constraints and complexity of real-time LSTM integration. This is an area for future work.
- Facial expressions were not implemented; we focused on full-body animations using Mixamo.
- Music Emotion Recognition (MER) is an ongoing and complex research problem. Challenges include subjectivity in emotion labeling, cultural variance in emotional interpretation, and distinguishing musical emotions (e.g., nostalgia, bittersweetness) from basic emotions.
- Our model achieved ~60% test accuracy on the custom dataset. Performance in real-time scenarios may vary depending on background noise and audio quality.
- We initially collected 200 music samples from 4 Spotify playlists, each corresponding to one emotion category: sad, relaxing, fearful, and pump up. Each playlist contained 50 songs. However, 10 files were corrupted or unreadable during feature extraction, resulting in a final dataset of 190 usable samples.
- The emotional categories were simplified compared to the original proposal’s arousal-valence approach for feasibility.

---

## 📌 Tips

- There is a short (~5s) initial delay before the animation starts.
- If Unity is not running, the Python script will fail to establish a socket connection and the program will not run.
- Keep Unity as the focused window — otherwise animations won't play.

---

## 🎥 Demo Video

This demo video showcases the complete project in action. The video shows Unity 3D running with the character animation linked to the predicted emotions. Spotify is open to display the current song being played, but the audio input is taken through the microphone, with the music being played from a phone (indicated at the bottom right of the Spotify window). The Python program is actively running (in the terminal window at the bottom left), extracting features from the microphone input and predicting the emotion, which is then sent to Unity for animation.


You can view a demo of the project here: [Demo Video](https://youtu.be/CcbkvOnXi0Q)