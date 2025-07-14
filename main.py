from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import openai

# Carrega variáveis do .env
load_dotenv()

# Inicializa FastAPI
app = FastAPI()

# Mensagem de teste para rota principal
@app.get("/")
def root():
    return {"status": "Servidor DesbloMente ativo e rodando."}

# Rota de proxy para o Lovable (ou outro front)
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

        return JSONResponse(content=response)
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
