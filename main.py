from fastapi import FastAPI
from pydantic import BaseModel

from llm_chat import chatbot




app= FastAPI()

@app.post('/my-chatbot')
def my_chatbot(request):
    response = chatbot(request)

    return response