import streamlit as st
import cv2
import time

from hand_logic import process_frame
from speech_handler import speak

st.set_page_config(
    page_title="SignBridge AI Pro",
    page_icon="🤟",
    layout="wide"
)


WORD_MAP = {
    "M A D E": "MADE",
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



st.markdown("""
<style>

/* Hide Deploy Button */
[data-testid="stToolbar"]{
    visibility:hidden;
    height:0%;
    position:fixed;
}
header[data-testid="stHeader"] {
    display: none;
}
section[data-testid="stMain"] > div:first-child {
    padding-top: 0rem !important;
}

.block-container {
    padding-top: 0rem !important;
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
    font-size:44px;
    font-weight:900;
    background:linear-gradient(
        45deg,
        #00ffcc,
        #0088ff
    );
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-top:-200px;
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
    padding:12px;
    font-size:20px;
    border-left:6px solid #00ffcc;
    min-height:50px;
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
 SIGNBRIDGE AI PRO
</h1>

""", unsafe_allow_html=True)


if "sentence" not in st.session_state:
    st.session_state.sentence = ""

if "last_capture_time" not in st.session_state:
    st.session_state.last_capture_time = 0

if "last_added_char" not in st.session_state:
    st.session_state.last_added_char = ""

left, right = st.columns([1.5, 1])

with left:

    viewfinder = st.empty()

    st.markdown("### 📝 Sentence Builder")

    sentence_box = st.empty()




with right:

    

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
        ["Female", "Male"],
        horizontal=True
    )

    colA, colB, colC= st.columns(3)

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
    with colC:
        backspace_button = st.button("⌫ Delete", use_container_width=True)




if clear_button:

    st.session_state.sentence = ""

if backspace_button:
    st.session_state.sentence = st.session_state.sentence.rstrip()[:-1]

if speak_button:

    sentence = st.session_state.sentence.strip()

    if sentence:

        speak(
            sentence,
            voice_type
        )

        st.success(
            f"Speaking: {sentence}"
        )



cap = cv2.VideoCapture(0)

last_char = ""
frames_held = 0



while True:

    success, frame = cap.read()

    if not success:

        st.error("Could not access webcam.")
        break

    output, current_char, score = process_frame(frame)

    

    

    status = "🔴 Waiting for Sign"
    
    if current_char == "DEL":
        current_time = time.time()
        if current_time - st.session_state.last_capture_time > 1.0:
            st.session_state.sentence = st.session_state.sentence.rstrip()[:-1]
            st.session_state.last_capture_time = current_time

    elif current_char == "SPEAK":
        current_time = time.time()
        if current_time - st.session_state.last_capture_time > 2.0:
            sentence = st.session_state.sentence.strip()
            if sentence:
                speak(sentence, voice_type)
            st.session_state.last_capture_time = current_time

    if current_char not in ["", "Nothing", "DEL", "SPEAK"]:

        status = "🟢 Detecting"

        if current_char == last_char:

            frames_held += 1

        else:

            frames_held = 0
            last_char = current_char

        current_time = time.time()


        if (
            frames_held >= 8
            and
            current_time -
            st.session_state.last_capture_time > 0.8
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


    viewfinder.image(
        output,
        channels="BGR",
        use_container_width=400
    )

    char_display.markdown(
        f"""
        <p class='char-box'>
        {current_char if current_char else "..."}
        </p>
        """,
        unsafe_allow_html=True
    )

    confidence_color = "#00ff88"

    if score < 0.6:
        confidence_color = "#ffaa00"

    if score < 0.3:
        confidence_color = "#ff4444"

    confidence_display.markdown(
        f"""
        <div class='metric'>
        Confidence:
        <span style='color:{confidence_color};
        font-weight:bold'>
        {score*100:.1f}%
        </span>
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

cap.release()
