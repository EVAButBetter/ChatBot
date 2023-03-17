import json

# from run import start
from endpoints.ConnectionManager import ConnectionManager
from lib.tts.tts_system import TextToSpeechSystem
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter
from pipeline.pipeline import  Pipeline
OUTPUT_DIR = "data/audio/"
eva_pipeline_router = APIRouter()
tts = TextToSpeechSystem(OUTPUT_DIR)
manager = ConnectionManager()
pipeline = Pipeline()
import json


def encode(ws_message, ws_type):
    """
    Generates message for the client

    Message for the client according to the protocol in
    websocketProtocol.md

    Parameters:
    ws_message (str): content of the message
    ws_type (str): type of communication

    Returns:
    request_json (dict): message according to protocol
    """
    request = dict()
    request["type"] = "request"
    request["content"] = ws_message
    request_json = json.dumps(request)
    return request_json


def decode(response_json):
    """
    Extracts message from the client

    Decodes from the client according to the protocol in
    websocketProtocol.md

    Parameters:
    response_json (dict): message from the client

    Return:
    user (str): content of the message from the client
    """
    response = json.loads(response_json)
    user = response["content"]
    return user


@eva_pipeline_router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
):
    request = dict()
    await manager.connect(websocket)
    try:
        while True:
            response_communication = await websocket.receive_text()
            response = json.loads(response_communication)
            res = None
            if response["type"] == "start":
                # first response
                presentation = (
                    "Hi, my name is Eva, the new ICT Departament Virtual Assistant! I'll we happy to help you."
                    " Are you looking for a person, a research group or a room in particular?"
                )
                request["type"] = "request"
                # get Audio Phrase
                blob, duration = await tts.text_to_speech(presentation)
                data = {"phrase": presentation, "audio": blob, "duration": duration}
                request["content"] = {"text": presentation, "data": [data]}
                request_communication = json.dumps(request)
                print(request_communication)
                await manager.send_message(request_communication,websocket)
                
                # presentation = ("Hi, my name is Eva, the new ICT Departament Virtual Assistant! I'll we happy to help you."
                #             " Are you looking for a person, a research group or a room in particular?")
                # request['type'] = 'request'
                # payload = {'text': presentation}
                # r = requests.get("http://localhost:3000/"+'phrases/phrase', params=payload)
                # if r.status_code==200 and len(r.json()):
                #     data = r.json()[0]
                # else: 
                #     data = None
                # request['content'] = {'text': presentation, 'data': [data]}
                # #request['content'] = presentation
                # #getAudioPhrase
                # request_communication = json.dumps(request)
                # await manager.send_message(request_communication,websocket)

                # second response.?
                response_communication = await websocket.receive_text()
                print("RESPONSE: ", response_communication)
                response = json.loads(response_communication)
                if response["type"] == "end":
                    conversation = False
                    request_json = encode("", "end")
                    continue
                content = response["content"]
                print("CONTENT: ", content)

                # start conversation
                conversation = True
                while conversation:
                    audios = []
                    if response["type"] == "end":
                        conversation = False
                        request_json = encode("", "end")
                        continue
                    question = response["content"]

                    # should handle the question here
                    # res = handle_function(question)
                    # res = question  # only for testing, so return the question
                    message = pipeline.run(question)

                    # get audio response in conversation
                    # getAudioPhrase
                    blob, duration = await tts.text_to_speech(message)
                    data = {"phrase": message, "audio": blob, "duration": duration}
                    request["type"] = "request"
                    request["content"] = {"text": message, "data": [data]}
                    request_json = json.dumps(request)

                    # send audio back
                    await manager.send_message(request_json, websocket)

                    # retrieve user's response
                    response_json = await websocket.receive_text()
                    response = json.loads(response_json)
                    content = response["content"]

                    # handle response
                    if "No" in content:
                        conversation = False
                        message = "See you next time, bye."
                        request["type"] = "request"

                        blob, duration = await tts.text_to_speech(message)
                        data = {"phrase": message, "audio": blob, "duration": duration}
                        request["content"] = {"text": message, "data": [data]}

                        request_json = json.dumps(request)
                        await manager.send_message(request_json, websocket)
                        request_json = encode("", "end")
                        await manager.send_message(request_json, websocket)

            elif response["type"] == "end":
                conversation = False
                agent = "See you next time, bye."
                request["type"] = "request"
                # getAudioPhrase
                blob, duration = await tts.text_to_speech(agent)
                data = {"phrase": presentation, "audio": blob, "duration": duration}

                request["content"] = {"text": agent, "data": [data]}
                request_json = json.dumps(request)
                await manager.send_message(request_json, websocket)
                request_json = encode("", "end")
                await manager.send_message(request_json, websocket)

            else:
                # no need to get audio here?
                message = (
                    f'I\'m confused... I have received a {response["type"]} message.'
                )
                # getAudioPhrase
                request_json = encode(message, "request")
                await manager.send_message(request_json, websocket)
                request_json = encode("", "end")
                await manager.send_message(request_json, websocket)
    except WebSocketDisconnect as e:
        manager.disconnect(websocket)


# @eva_pipeline_router.websocket("/ws")
# async def websocket_endpoint(
#     websocket: WebSocket,
# ):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             data = json.loads(data)
#             question = data["content"]
#             await manager.send_message(f"your input: {question}", websocket)

#             # handle question
#             # answer = handle(question)

#             answer = question # for testing
#             blob_audio, duration = await text_to_speech.text_to_speech(answer)
#             result = {"type": "request", "content": {"text":"","data":[{"data":"","audio":str(blob_audio),"duration":duration}]}}
#             json_data = json.dumps(result)
#             await manager.send_message_to_downstream(json_data, websocket)

#     except WebSocketDisconnect as e:
#         manager.disconnect(websocket)


# for testing
# var socket = new WebSocket("ws://localhost:8000/api/v1/eva_pipeline/ws")
# socket.addEventListener("message",(res)=>{console.log(res)})
# data = '{"type":"request", "content":"what is your name"}'
