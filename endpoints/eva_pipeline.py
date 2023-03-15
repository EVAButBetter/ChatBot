import json
# from run import start
from endpoints.ConnectionManager import ConnectionManager
from lib.tts.tts_system import TextToSpeechSystem
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter

eva_pipeline_router = APIRouter(
    prefix="/eva_pipeline",
    tags=["eva_pipeline"],
)
OUTPUT_DIR = "data/audio/"
text_to_speech = TextToSpeechSystem(OUTPUT_DIR)
manager = ConnectionManager()

@eva_pipeline_router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            question = data["content"]
            await manager.send_message(f"your input: {question}", websocket)
            
            # handle question
            # answer = handle(question)
            
            answer = question # for testing
            blob_audio, duration = await text_to_speech.text_to_speech(answer)
            result = {"type": "request", "content": {"text":"","data":[{"data":"","audio":str(blob_audio),"duration":duration}]}}
            json_data = json.dumps(result)
            await manager.send_message_to_downstream(json_data, websocket)
            
    except WebSocketDisconnect as e:
        manager.disconnect(websocket)
        
        
# for testing
# var socket = new WebSocket("ws://localhost:8000/api/v1/eva_pipeline/ws")
# socket.addEventListener("message",(res)=>{console.log(res)})
# data = '{"type":"request", "content":"what is your name"}'