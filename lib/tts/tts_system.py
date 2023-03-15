import io
import os
import time
import librosa
import base64
import requests
from gtts import gTTS

class TextToSpeechSystem:
    """
    convert the text to .wav then to a blob file

    """

    def __init__(self, OUTPUT_DIR):
        super(TextToSpeechSystem).__init__()
        self.OUTPUT_DIR = OUTPUT_DIR
            
    async def text_to_speech(self, text, lang="en"):
        """_summary_

        Args:
            text (string): sentence
            lang (str, optional): _description_. Defaults to "en".

        Returns:
            blob: blob file
        """
        
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)
        tts = gTTS(text, lang=lang)
        FILE_DIR = str(time.time()) + ".wav"
        tts.save(self.OUTPUT_DIR + FILE_DIR)
        blob = self.blob_encoder(self.OUTPUT_DIR + FILE_DIR)
        duration = self.get_duration_mp3_and_wav(self.OUTPUT_DIR + FILE_DIR)
        return blob, duration
        
    def blob_encoder(self, filedir):
        """_summary_

        Args:
            filedir (string): file dir

        Returns:
            blob: blob file
        """
        with open(filedir, 'rb') as f:
            wav_data = f.read()
        # wav_b64 = base64.b64encode(wav_data).decode('utf-8')

        bytes_io = io.BytesIO(wav_data)
        blob = bytes_io.getvalue()
        return blob
    
    def get_duration_mp3_and_wav(self, file_path):
     duration = librosa.get_duration(path=file_path)
     return duration

