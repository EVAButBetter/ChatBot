from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import Request
class Message(BaseModel):
    isReceived: bool
    type: str
    content: str

pipeline_router = APIRouter(
    prefix="/pipeline",
    tags=["pipeline"],
)



@pipeline_router.post("/")
async def get_msg(request: Request):
    data = await request.json()
    content = data["content"]
    content["isReceived"] = True
    content["message"] = "vv"
    return content

@pipeline_router.get("/test")
async def test():
    return {"message": "what? do you want to ask to me"}