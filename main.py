from fastapi import FastAPI
from src.utils.db import Base, engine

Base.metadata.create_all(engine)

app = FastAPI(
    title="Task Management App",
    description="Task Management App System by FastAPI",
    version="1.0.0"
)


