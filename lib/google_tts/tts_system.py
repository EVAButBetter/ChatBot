import os
import time
from gtts import gTTS


class TextToSpeechSystem:
    """
    convert the text to .wav then to base64 file

    """

    def __init__(self):
        pass

    def text_to_speech(self, text, lang="en"):
        # return base64 audio file
        OUTPUT_DIR = "../../data/audio/"
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        tts = gTTS(text, lang=lang)
        FILE_DIR = str(time.time()) + ".wav"
        tts.save(OUTPUT_DIR + FILE_DIR)



test = TextToSpeechSystem()
test.text_to_speech(text="how are you")
