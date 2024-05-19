from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from infraestructure.web.routers.routes import routers
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(routers)

Instrumentator().instrument(app).expose(app)

