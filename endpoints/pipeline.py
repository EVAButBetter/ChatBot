from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import Request
import wave
import json

class Message(BaseModel):
    isReceived: bool
    type: str
    content: str


pipeline_router = APIRouter(
    prefix="/pipeline",
    tags=["pipeline"],
)


def load_audio_blob_test(audio_path):
    # Open the .wav file in read mode
    with wave.open(audio_path, 'rb') as audio_file:
        # Read the audio data and store it in a bytes object
        audio_data = audio_file.readframes(audio_file.getnframes())

        # Convert the bytes object to a blob
        audio_blob = bytes(audio_data)
    return str(audio_blob)


@pipeline_router.post("/")
async def get_msg(request: Request):
    data = await request.json()
    content = data["content"]
    content["isReceived"] = True
    content["message"] = "vv"
    return content


@pipeline_router.get("/test/request/{type}")
async def testEVARequest(type):
    if type == "request":
        content = "In which room I can find professor Javi Agenjo?"
    else:
        content = ""
    json_request = {"type": type, "content": content}
    # Serializing json
    return json.dumps(json_request, indent=4)


@pipeline_router.get("/test/response/")
async def testEVAResponse():
    type = "request"
    audio_object_1 = {"text": "Sure!", "audio": load_audio_blob_test(f"./data/test_to_remove/test_audio1.wav"), "duration": "10",
                      "phrase": "Hello"}
    audio_object_2 = {"text": "Professor Javi Agenjo is in room 54321",
                      "audio": load_audio_blob_test(f"./data/test_to_remove/test_audio2.wav"), "duration": "10",
                      "phrase": "Professor Javi Agenjo is in room 54321"}
    data = [audio_object_1, audio_object_2]
    json_response = {"type": type, "data": data}
    return json.dumps(json_response, indent=4)
