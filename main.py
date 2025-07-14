from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import openai

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Servidor DesbloMente ativo e rodando."}

@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()

        messages = body.get("messages", [])
        model = body.get("model", "gpt-4")
        temperature = body.get("temperature", 0.7)

        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature
        )

        # Extrai só o texto da resposta
        content = response.choices[0].message.content

        return JSONResponse(content={"message": content})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
