<div align="center">

```
███████╗██╗ ██████╗ ███╗   ██╗██████╗ ██████╗ ██╗██████╗  ██████╗ ███████╗
██╔════╝██║██╔════╝ ████╗  ██║██╔══██╗██╔══██╗██║██╔══██╗██╔════╝ ██╔════╝
███████╗██║██║  ███╗██╔██╗ ██║██████╔╝██████╔╝██║██║  ██║██║  ███╗█████╗  
╚════██║██║██║   ██║██║╚██╗██║██╔══██╗██╔══██╗██║██║  ██║██║   ██║██╔══╝  
███████║██║╚██████╔╝██║ ╚████║██████╔╝██║  ██║██║██████╔╝╚██████╔╝███████╗
╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝  ╚═════╝ ╚══════╝
                              AI  P R O  
```

#  SignBridge AI Pro

### *Real-Time Sign Language to Speech Converter*

> **Bridging the communication gap between the deaf/mute community and the hearing world one sign at a time.**

---

![Python](https://img.shields.io/badge/Python-3.9+-00FFCC?style=for-the-badge&logo=python&logoColor=black)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-00FFCC?style=for-the-badge&logo=streamlit&logoColor=black)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-0088FF?style=for-the-badge&logo=opencv&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML_Model-00D4AA?style=for-the-badge&logo=scikit-learn&logoColor=black)

</div>

---

## 📌 Table of Contents

- [The Problem We Solved](#-the-problem-we-solved)
- [What SignBridge Does](#-what-signbridge-does)
- [Live Demo Flow](#-live-demo-flow)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Training Data](#-training-data--model)
- [Installation](#-installation)
- [How to Run](#-how-to-run)
- [Challenges & Difficulties](#-challenges--difficulties)
- [Future Scope](#-future-scope)
- [Potential & Impact](#-potential--impact)

---

## 😔 The Problem We Solved

> *Imagine being in a hospital, urgently needing help — but you cannot speak and the doctor doesn't understand sign language.*

**466 million people** worldwide live with disabling hearing loss. Sign language is their primary mode of communication — yet the vast majority of the hearing world cannot understand it.

The existing solutions are broken:

| Problem | Reality |
|---|---|
| 🚫 Human Interpreters | Cost $100–$150/hour, not available 24/7 |
| 🚫 No Real-Time Solution 
| 🚫 Social Isolation | Deaf/mute individuals cut off from everyday conversation |

**SignBridge AI Pro solves this with just a webcam.** No special hardware. No interpreter needed.

---

## What SignBridge Does

SignBridge AI Pro is a **real-time, AI-powered sign language translator** that:

- 📷 **Reads your hand signs** through any standard webcam
- 🧠 **Predicts the letter** using a trained Machine Learning model
- 📝 **Builds sentences** automatically from detected letters
- 🔊 **Speaks the sentence** aloud using Text-to-Speech
- ✋ **Supports gesture controls** — delete, speak, and more, all hands-free
- 💡 **Smart word recognition** — auto-converts `W I T H` → `WITH`

---

## 🎬 Live Demo Flow

```
You sign a letter
       ↓
Webcam captures frame (30fps)
       ↓
cvzone detects hand landmarks (21 points × 3 axes = 63 values per hand)
       ↓
126 wrist-relative 3D features extracted
       ↓
scikit-learn ML model predicts sign + confidence score
       ↓
Stability check: same sign held for 8+ frames AND 0.8s cooldown
       ↓
Letter added to sentence → Word Map collapses spelling to word
       ↓
SPEAK gesture / button → browser's Web Speech API via JavaScript will make it speak 🔊
```

---

## 🛠️ Tech Stack

| Technology | Role | Why We Used It |
|---|---|---|
| **Python 3.9+** | Core language | Ecosystem support for ML and CV |
| **Streamlit** | Web UI framework | Rapid UI with real-time loop support |
| **OpenCV (cv2)** | Webcam + frame processing | Industry standard for computer vision |
| **cvzone** | Hand detection wrapper | MediaPipe-based, supports 2 hands, 21 landmarks each |
| **MediaPipe** | Underlying hand tracking | Google's hand landmark model |
| **scikit-learn** | ML model training & inference | Reliable classifier with `predict_proba` support |
| **joblib** | Model serialization | Fast loading of trained `.pkl` model |
| **NumPy** | Feature array processing | argmax, array ops for landmark data |
| **time** | Cooldown logic | Prevents duplicate/rapid-fire letter capture |
| **javascript** | Text-to-Speech with male/female voice support

---

## 📁 Project Structure

```
signbridge-ai-pro/
│
├── app.py                  ← Main Streamlit application & UI
├── hand_logic.py           ← Hand detection, feature extraction, ML inference
├── speech_handler.py       ← Text-to-Speech conversion (Male/Female voice)
├── sign_model.pkl          ← Trained scikit-learn classifier
├── data_collection.py      ← Script used to collect training landmarks
├── train_model.py          ← Model training script
├── requirements.txt        ← All dependencies
└── README.md               ← You are here
```

### File Breakdown

#### `app.py` — The Brain of the UI
- Streamlit-based dark neon web interface
- Two-column layout: webcam feed (left) + detector controls (right)
- Session state management for sentence, timing, and last character
- `while True` real-time camera loop
- Buttons: 🔊 Speak, 🗑️ Clear, ⌫ Delete
- CSS injection for custom dark/cyan theme
- Smart word learning via `WORD_MAP` dictionary

#### `hand_logic.py` — The Detection Engine
- `HandDetector` from cvzone (up to 2 hands simultaneously)
- Extracts 126 wrist-relative 3D landmark features
- Loads `sign_model.pkl` via joblib
- `LABEL_MAP` for mapping model classes → custom actions (`DEL`, `SPEAK`)
- Confidence filter: predictions below 20% are rejected as `"Nothing"`
- Draws bounding box + label on output frame

#### `speech_handler.py` — The Voice
- Converts built sentence to spoken audio
- Supports Male and Female voice selection
- Triggered by button click or `SPEAK` gesture

#### `sign_model.pkl` — The Trained Model
- scikit-learn classifier trained on 8000+ landmark samples
- Takes 126 features → outputs predicted sign class + probability
- Loaded once at startup for fast real-time inference

<B>Unfortunately due to it's larger size it is not added in the repo </B>

---

## 🧠 Training Data & Model

### Dataset
- **Total Samples Collected:** 8,000+ landmark collections
- **Features per Sample:** 126 (21 landmarks × 3 axes × 2 hands, wrist-normalized)
- **Collection Method:** Custom `data_collection.py` script — live webcam-based capture using cvzone HandDetector
- **Data Format:** Wrist-relative XYZ coordinates for each of the 21 hand landmarks per hand
- **Normalization:** All coordinates subtracted from wrist position (landmark 0) for position-invariant features

### Why Wrist-Relative Features?
Raw pixel coordinates change depending on where your hand is on screen. By subtracting the wrist position from every landmark, the model learns the **shape** of the sign not the position. This makes detection robust regardless of where the hand appears in the frame.

### Model Selection — The Hard Choice
Choosing the right model was one of the key decisions:

| Model Tried | Result |
|---|---|
| Decision Tree | Fast but low accuracy on similar signs |
| KNN | Good accuracy but slow at inference |
| Random Forest | Better generalization, more robust |
| **Final: Gradient Boosting / SVM / RF** | Best balance of speed + accuracy |

The final model was selected based on cross-validation performance and real-world testing — because a sign language model that works in a notebook but fails on a live webcam is useless.

### Confidence Filtering
Any prediction with confidence below **20%** is rejected and treated as `"Nothing"`. This prevents garbage output when no hand is visible or the hand is partially in frame.

---

## 💻 Installation

### Prerequisites
- Python 3.9 or higher
- Webcam (built-in or external)
- Windows / macOS / Linux

### Step 1 — Clone the Repository
```bash
git clone https://github.com/yourusername/signbridge-ai-pro.git
cd signbridge-ai-pro
```

### Step 2 — Create a Virtual Environment
```bash
# Create environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

> ⚠️ **IMPORTANT:** Always use a virtual environment. This project has strict dependency version requirements that conflict with system-level packages. (We learned this the hard way — see [Challenges](#-challenges--difficulties))

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### `requirements.txt`
```
streamlit
opencv-python
cvzone
mediapipe
scikit-learn
joblib
numpy
```

> ⚠️ **Note on MediaPipe:** Use `mediapipe==0.10.x`. Newer versions have breaking changes with cvzone. If you hit errors, pin it: `pip install mediapipe==0.10.9`

---

## ▶️ How to Run

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Usage
1. Allow webcam access when prompted
2. Show your hand sign in front of the camera
3. Hold the sign steady — letter auto-captures after 8 frames
4. Watch your sentence build in real-time
5. Press **🔊 Speak** or use the SPEAK gesture to hear it out loud
6. Press **⌫ Delete** to remove the last letter
7. Press **🗑️ Clear** to reset the sentence

---

## 🔥 Challenges & Difficulties

This project looked straightforward on paper. In reality, it was a battle on multiple fronts.

---

### 1. 📦 Dependency Hell — The Biggest Nightmare

This was by far the most painful part of the project.

```
ERROR: pip's dependency resolver does not currently take into account
all the packages that are installed...
```

The core conflict: **MediaPipe**, **cvzone**, **OpenCV**, and **scikit-learn** all have overlapping transitive dependencies that fight each other — especially across Python versions.

Specific issues encountered:
- `mediapipe` requires specific versions of `opencv-python` — installing the wrong one silently breaks hand detection
- `cvzone` wraps `mediapipe` but lags behind its releases — newer `mediapipe` versions broke cvzone's `HandDetector`
- `pyttsx3` behaves differently on Windows vs Linux — required different audio backends
- Running `pip install` globally corrupted the system Python environment twice
- **Solution:** Strict virtual environments + pinned versions in `requirements.txt`

> 💡 **Lesson:** For any ML + CV project, always isolate your environment first. Not after the first error. Before writing a single line of code.

---

### 2. 🧠 Model Selection — Which Classifier Actually Works?

Training a model on collected data is easy. Training one that **generalizes to real-world signing** is not.

Challenges faced:
- Similar-looking signs (like `A`, `S`, `E` in ASL) were being confused by simpler models
- Decision Trees overfit on training data but failed on live webcam
- KNN was accurate but too slow for real-time 30fps inference
- Training environment (Jupyter Notebook / Google Colab) produced models that behaved differently when loaded in the Streamlit app
- Hyperparameter tuning required multiple rounds of re-collection + retraining

> 💡 **Lesson:** Always validate your model on live webcam data — not just a test split. A 95% accuracy on a CSV means nothing if it fails on real hands.

---

### 3. 🖥️ Training in Different Environments

The model was trained in one environment (Colab / local Jupyter) and deployed in another (Streamlit app). This caused:

- `sklearn` version mismatches — model saved in one version, loaded in another → `InconsistentVersionWarning` or silent failures
- Feature array shape mismatches between training script and `hand_logic.py`
- Random Forest models trained on GPU-enabled Colab failed to load correctly on CPU-only local machines

> 💡 **Solution:** Standardize on one Python + sklearn version across training and deployment. Save the version metadata alongside the model.

---

### 4. ⚡ Real-Time Stability — Preventing Garbage Input

Raw detection is noisy. Without stability logic:
- A single frame of misdetection adds a wrong letter
- Holding a sign floods the sentence with duplicates

**Solution implemented:**
- 8-frame stability check before accepting a letter
- 0.8 second cooldown between captures
- Duplicate consecutive letter prevention via `last_added_char`

---

### 5. 🎨 Streamlit Limitations

Streamlit wasn't designed for real-time video loops. Challenges:
- Default header and toolbar couldn't be hidden without CSS injection hacks
- `while True` loop in Streamlit doesn't play well with reruns
- Session state had to be carefully managed to prevent state loss on interaction

---

## 🚀 Future Scope

SignBridge AI Pro is just the beginning. Here's where this can go:

### Short Term
- [ ] **More signs** — extend beyond alphabet to full ASL/ISL vocabulary (numbers, common phrases)
- [ ] **Two-hand sign support** — improve accuracy for signs that require both hands
- [ ] **Confidence threshold control** — let users adjust sensitivity via UI slider
- [ ] **Sign history panel** — show last 10 detected signs with confidence scores
- [ ] **Export sentence** — save built sentences to a text file

### Medium Term
- [ ] **Deep Learning model** — replace scikit-learn with a CNN or LSTM for better accuracy on complex signs
- [ ] **ISL Support** — add Indian Sign Language dataset (currently most datasets are ASL-based)
- [ ] **Mobile version** — port to a mobile-friendly interface using camera API
- [ ] **Word suggestions** — autocomplete partially spelled words
- [ ] **Multi-language TTS** — speak output in Hindi, Spanish, French, etc.

### Long Term
- [ ] **Sentence-level sign recognition** — recognize full phrases/sentences as single gestures, not just letter-by-letter
- [ ] **Reverse mode** — text/speech → animated sign language avatar for two-way communication
- [ ] **Browser extension** — live sign language subtitles for video calls (Zoom, Meet)
- [ ] **Edge deployment** — run entirely on Raspberry Pi for offline portable use
- [ ] **Wearable integration** — pair with smart gloves for higher precision in low-light conditions

---

## 🌍 Potential & Impact

### Who Benefits
| User Group | Use Case |
|---|---|
| Deaf/mute individuals | Communicate with anyone, anywhere |
| Hospitals & clinics | Emergency communication without interpreters |
| Schools & universities | Inclusive education environments |
| Customer service | Serve deaf customers without specialized staff |
| Family members | Communicate with deaf relatives without learning sign language |

### Why This Matters
- **Zero hardware cost** — works on any laptop or PC with a webcam
- **Offline capable** — no internet dependency for detection or speech
- **Scalable** — the architecture can handle new signs with just more training data
- **Accessible** — runs in a browser tab, no app install required

### By the Numbers
- 🌐 **466M+** people with disabling hearing loss globally
- 📊 **8,000+** landmark samples in training dataset
- ⚡ **~30fps** real-time detection speed
- 🎯 **126** features per prediction (21 landmarks × 3D × 2 hands)
- 🔊 **2** voice options (Male / Female TTS)
- 📁 **4** core project files

---

## 🤝 Contributing

Contributions are welcome! If you want to:
- Add new signs to the dataset
- Improve model accuracy
- Add a new language for TTS
- Fix bugs

Please open an issue or submit a pull request.

---


**Built with 🤟 to break communication barriers.**

*"The ones who are crazy enough to think they can change the world are the ones who do."*

---

⭐ **Star this repo if SignBridge helped you or inspired you!** ⭐

</div>
