import streamlit as st
import cv2
import time

from hand_logic import process_frame
from speech_handler import speak

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="SignBridge AI Pro",
    page_icon="🤟",
    layout="wide"
)

# =====================================================
# WORD LEARNING
# =====================================================

WORD_MAP = {
    "W I T H": "WITH",
    "B Y": "BY",
    "M E G H N A": "MEGHNA",
    "I A M": "I AM",
    "T H A N K Y O U": "THANK YOU",
    "H E L L O": "HELLO",
    "S I G N B R I D G E": "SIGNBRIDGE"
}

def learn_words(text):

    result = text

    changed = True

    while changed:

        changed = False

        for spelling, word in WORD_MAP.items():

            if spelling in result:

                result = result.replace(
                    spelling,
                    word
                )

                changed = True

    return result

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

/* Hide Deploy Button */
[data-testid="stToolbar"]{
    visibility:hidden;
    height:0%;
    position:fixed;
}

/* Bigger Spinner */
.stSpinner > div{
    transform:scale(2);
}

/* Background */
.stApp{
    background:#050505;
    color:white;
}

/* Title */
.title{
    text-align:center;
    font-size:55px;
    font-weight:900;
    background:linear-gradient(
        45deg,
        #00ffcc,
        #0088ff
    );
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-top:-30px;
}

/* Current Letter */
.char-box{
    font-size:160px;
    text-align:center;
    color:#00ffcc;
    font-weight:900;
    margin:0;
    text-shadow:0px 0px 25px rgba(0,255,204,0.6);
}

/* Sentence */
.sentence-box{
    background:#111;
    border-radius:12px;
    padding:20px;
    font-size:32px;
    border-left:6px solid #00ffcc;
    min-height:90px;
}

/* Side Panel */
.panel{
    background:rgba(255,255,255,0.05);
    padding:20px;
    border-radius:15px;
    border:1px solid #333;
}

/* Metrics */
.metric{
    font-size:20px;
    text-align:center;
}

/* Status */
.status{
    font-size:22px;
    text-align:center;
    font-weight:bold;
}

</style>

<h1 class="title">
🤟 SIGNBRIDGE AI PRO
</h1>

""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================

if "sentence" not in st.session_state:
    st.session_state.sentence = ""

if "last_capture_time" not in st.session_state:
    st.session_state.last_capture_time = 0

if "last_added_char" not in st.session_state:
    st.session_state.last_added_char = ""

# =====================================================
# LAYOUT
# =====================================================

left, right = st.columns([1.8, 1])

# =====================================================
# LEFT
# =====================================================

with left:

    viewfinder = st.empty()

    st.markdown("### 📝 Sentence Builder")

    sentence_box = st.empty()

# =====================================================
# RIGHT
# =====================================================

with right:

    st.markdown(
        "<div class='panel'>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 style='text-align:center;'>LIVE SIGN DETECTOR</h3>",
        unsafe_allow_html=True
    )

    char_display = st.empty()

    confidence_display = st.empty()

    conf_bar = st.empty()

    status_display = st.empty()

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    voice_type = st.radio(
        "🗣️ Voice",
        ["Male", "Female"],
        horizontal=True
    )

    colA, colB = st.columns(2)

    with colA:

        speak_button = st.button(
            "🔊 Speak Sentence",
            use_container_width=True
        )

    with colB:

        clear_button = st.button(
            "🗑️ Clear",
            use_container_width=True
        )

# =====================================================
# BUTTONS
# =====================================================

if clear_button:

    st.session_state.sentence = ""

if speak_button:

    sentence = st.session_state.sentence.strip()

    if sentence:

        speak(
            sentence,
            voice_type
        )

# =====================================================
# CAMERA
# =====================================================

cap = cv2.VideoCapture(0)

last_char = ""
frames_held = 0

# =====================================================
# MAIN LOOP
# =====================================================

while True:

    success, frame = cap.read()

    if not success:

        st.error("Could not access webcam.")
        break

    output, current_char, score = process_frame(frame)

    # ------------------------------------------
    # STATUS
    # ------------------------------------------

    status = "🔴 Waiting for Sign"

    if current_char != "" and current_char != "Nothing":

        status = "🟢 Detecting"

        if current_char == last_char:

            frames_held += 1

        else:

            frames_held = 0
            last_char = current_char

        current_time = time.time()

        # --------------------------------------
        # Stable Detection + Cooldown
        # --------------------------------------

        if (
            frames_held >= 12
            and
            current_time -
            st.session_state.last_capture_time > 1.2
        ):

            if (
                current_char
                !=
                st.session_state.last_added_char
            ):

                st.session_state.sentence += (
                    current_char + " "
                )

                st.session_state.sentence = (
                    learn_words(
                        st.session_state.sentence
                    )
                )

                st.session_state.last_added_char = (
                    current_char
                )

                st.session_state.last_capture_time = (
                    current_time
                )

                frames_held = 0

    else:

        frames_held = 0

    # ------------------------------------------
    # UI UPDATE
    # ------------------------------------------

    viewfinder.image(
        output,
        channels="BGR",
        use_container_width=True
    )

    char_display.markdown(
        f"""
        <p class='char-box'>
        {current_char if current_char else "..."}
        </p>
        """,
        unsafe_allow_html=True
    )

    confidence_display.markdown(
        f"""
        <div class='metric'>
        Confidence: <b>{score*100:.1f}%</b>
        </div>
        """,
        unsafe_allow_html=True
    )

    conf_bar.progress(
        min(
            max(float(score), 0.0),
            1.0
        )
    )

    status_display.markdown(
        f"""
        <div class='status'>
        {status}
        </div>
        """,
        unsafe_allow_html=True
    )

    sentence_box.markdown(
        f"""
        <div class='sentence-box'>
        {st.session_state.sentence}
        </div>
        """,
        unsafe_allow_html=True
    )

# =====================================================
# CLEANUP
# =====================================================

cap.release()