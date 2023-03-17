import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter
from endpoints.eva_pipeline import eva_pipeline_router
import uvicorn
# url = "10.55.0.7:8765/ws"
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router_v1 = APIRouter()

api_router_v1.include_router(eva_pipeline_router)

app.include_router(api_router_v1)

if __name__ == "__main__":
    print("server starting...")
    port = 8765
    # host = "10.55.0.7"
    host = "0.0.0.0"
    ssl_keyfile = "key.pem"
    ssl_certfile = "cert.pem"
    print("#### STARTING EVA...! ####\n")
    print("listening on {}:{}".format(host, port))
    print("#" * 60)
    uvicorn.run(
        app,
        host=host,
        port=port,
        ssl_keyfile=ssl_keyfile,
        ssl_certfile=ssl_certfile,
    )
