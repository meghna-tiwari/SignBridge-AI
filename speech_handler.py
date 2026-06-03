import pyttsx3
import threading

class SpeechEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 1.0)
        
    def _speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def speak_now(self, text):
        """Runs speech in a separate thread to prevent blocking the camera"""
        threading.Thread(target=self._speak, args=(text,), daemon=True).start()


voice = SpeechEngine()