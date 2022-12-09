import logging
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

logger = logging.getLogger("fastapi")

class Message(BaseModel):
    message: str

@app.post("/")
def get_message(message: Message):
    logger.info("Received message: %s", message.message)
    return Message(message="Hello World")
