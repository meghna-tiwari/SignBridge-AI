import streamlit as st
import streamlit.components.v1 as components
import cv2
import os
from hand_logic import process_frame


st.set_page_config(page_title="SignBridge AI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {
        background-color: #0b0e14;
        overflow: hidden;
    }
    .main-title {
        text-align: center; 
        color: white; 
        font-family: 'Segoe UI', sans-serif;
        margin-top: -60px;
        letter-spacing: 2px;
    }
    .result-card {
        background: linear-gradient(145deg, #161920, #0e1117);
        border: 2px solid #00ffcc;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        box-shadow: 0px 0px 25px rgba(0, 255, 204, 0.15);
        margin-top: 20px;
    }
    .char-text {
        font-family: 'Segoe UI', sans-serif;
        font-size: 160px;
        font-weight: 800;
        color: #00ffcc;
        margin: 0;
        text-shadow: 0 0 20px rgba(0, 255, 204, 0.4);
    }
    .stImage > img {
        border-radius: 20px;
        border: 1px solid #333;
        max-height: 72vh;
    }
    </style>
    <h2 class="main-title">SIGNBRIDGE <span style="color:#00ffcc;">AI</span></h2>
""", unsafe_allow_html=True)


def speak_now(text):
    if text:
        components.html(f"""
            <script>
            window.speechSynthesis.cancel(); // Clear queue
            var msg = new SpeechSynthesisUtterance('{text}');
            msg.rate = 1.1;
            msg.pitch = 1.0;
            window.speechSynthesis.speak(msg);
            </script>
        """, height=0)


col1, col2 = st.columns([1.7, 1])

with col1:
    viewfinder = st.empty()

with col2:
    result_container = st.empty()
    st.write("---")
    st.markdown("### ⚙️ System Controls")
    run = st.toggle("Active Recognition", value=True)
    st.caption("Tip: If sound doesn't play, toggle the switch OFF then ON once.")


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

last_spoken_char = ""
current_stable_char = ""
stability_counter = 0

while run:
    success, frame = cap.read()
    if not success: break

    
    processed_img, detected_char = process_frame(frame)

    
    if detected_char != "":
        if detected_char == current_stable_char:
            stability_counter += 1
        else:
            current_stable_char = detected_char
            stability_counter = 0
        
       
        if stability_counter == 3:
            if current_stable_char != last_spoken_char:
                speak_now(current_stable_char)
                last_spoken_char = current_stable_char
    else:
        stability_counter = 0
        current_stable_char = ""

    
    viewfinder.image(processed_img, channels="BGR", use_container_width=True)
    
    result_container.markdown(f"""
        <div class="result-card">
            <p style="color: #666; letter-spacing: 2px; margin-bottom:0;">DETECTED SIGN</p>
            <p class="char-text">{detected_char if detected_char else "..."}</p>
        </div>
    """, unsafe_allow_html=True)

cap.release()