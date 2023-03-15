import os

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter
from endpoints.eva_pipeline import eva_pipeline_router

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

api_router_v1.include_router(eva_pipeline_router)

app.include_router(api_router_v1, prefix=API_PREFIX, tags=["api"])

if __name__ == "__main__":
    print("server starting...")
    port = 8000
    host = "127.0.0.1"
    print("#### STARTING EVA... BUT BETTER! ####\n")
    print("listening on {}:{}".format(host,port))
    print("#"*60)
    uvicorn.run(app, host=host, port=port)