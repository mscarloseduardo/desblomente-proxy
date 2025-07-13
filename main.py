
from fastapi import FastAPI, Request
import openai
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Permitir requisições de qualquer origem (para teste)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔐 SUA API KEY AQUI (SEGURA)
openai.api_key = "SUA_CHAVE_API_AQUI"

@app.post("/proxy")
async def proxy(request: Request):
    data = await request.json()
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=data["messages"]
    )
    return response
