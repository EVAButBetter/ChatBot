import os

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter
from endpoints.pipeline import pipeline_router

import uvicorn

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api"

api_router_v1 = APIRouter(
    prefix="/v1",
    tags=["v1"],
)

api_router_v1.include_router(pipeline_router)

app.include_router(api_router_v1, prefix=API_PREFIX, tags=["api"])

if __name__ == "__main__":
    uvicorn.run("server:app", reload=True, host='0.0.0.0', port=os.getenv("PORT", default=8000), log_level="info")


# import asyncio

# import uvicorn
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from fastapi.responses import HTMLResponse
# from starlette.websockets import WebSocketDisconnect

# app = FastAPI()

# @app.websocket("/audio")
# async def audio(websocket: WebSocket):
#     await websocket.accept()

#     # Open the audio file and read the data
#     with open("data/audio/1679000906.mp3", "rb") as audio_file:
#         audio_data = audio_file.read()

#     data_dict = {
#         "audio": str(audio_data),
#         "message": "Here's your audio data!"
#     }

#     # Send the data dictionary as a JSON object over the WebSocket connection
#     await websocket.send_json(data_dict)


# if __name__ == "__main__":
#     # Start the WebSocket server using uvicorn
#     uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)