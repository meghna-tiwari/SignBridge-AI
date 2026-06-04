import streamlit.components.v1 as components

def speak(text, gender="Female"):

    if not text:
        return

    text = text.replace("'", "\\'")

    voice_index = 2 if gender == "Female" else 1
    pitch = 1.5 if gender == "Female" else 1.0

    js_code = f"""
    <script>

    window.speechSynthesis.cancel();

    function speakNow() {{

        let msg = new SpeechSynthesisUtterance("{text}");

        let voices = window.speechSynthesis.getVoices();

        if (voices.length > {voice_index}) {{
            msg.voice = voices[{voice_index}];
        }}

        msg.rate = 0.5;
        msg.pitch = {pitch};
        msg.volume = 1.0;

        window.speechSynthesis.speak(msg);
    }}

    if (speechSynthesis.getVoices().length === 0) {{

        speechSynthesis.onvoiceschanged = speakNow;

    }} else {{

        speakNow();

    }}

    </script>
    """

    components.html(js_code, height=0)
