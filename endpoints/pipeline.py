import json
import base64
from fastapi import APIRouter
from fastapi.responses import FileResponse
from pipeline.pipeline import  Pipeline

pipeline = Pipeline()

pipeline_router = APIRouter(
    prefix="/pipeline",
    tags=["pipeline"],
)

@pipeline_router.get("/")
async def test(request: str):
    request_dict = json.loads(request)
    message = request_dict.get("message")
    response = pipeline.run(message)
    return {"message": f"{response}"}
