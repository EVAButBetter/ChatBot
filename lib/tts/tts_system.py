import io
import os
import time
import json
import base64
import librosa
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
        blob = tts.stream()
        # for i in blob:
        #     print("i",i)
        FILE_DIR = str(int(time.time())) + ".mp3"
        tts.save(self.OUTPUT_DIR + FILE_DIR)

        blob = self.blob_encoder(self.OUTPUT_DIR + FILE_DIR)
        blob = ''.join([chr(byte) for byte in blob])
        duration = self.get_duration_mp3_and_wav(self.OUTPUT_DIR + FILE_DIR)
        return blob, duration

    def blob_encoder(self, filedir):
        """_summary_

        Args:
            filedir (string): file dir

        Returns:
            blob: blob file
        """
        # Open the .wav file in read mode
        with open(filedir, 'rb') as f:
            wav_data = f.read()

        bytes_io = io.BytesIO(wav_data)
        blob = bytes_io.getvalue()
        return blob

    def get_duration_mp3_and_wav(self, file_path):
        # duration = librosa.get_duration(path=file_path)
        # return duration
        return 10


# # test
# tts = TextToSpeechSystem("../../data/audio/")
# blob, duration = tts.text_to_speech(
#     text="Could you give me the name and surname of the person?"
# )
# # a = {"test":1}
# # json_data = json.dumps(a)
# # print(json_data)
# # json_data["data"] = 123
# # print(json_data)
# print(type(blob))
# print(json.dumps(blob))
