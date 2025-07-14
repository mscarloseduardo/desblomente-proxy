from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import openai

# Carrega variáveis do .env
load_dotenv()

# Inicializa o FastAPI
app = FastAPI()

# Ativa CORS para permitir requisições do Lovable ou qualquer outro frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para segurança, depois substitua por ["https://lovable.dev"] se quiser restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota básica para teste
@app.get("/")
def root():
    return {"status": "Servidor DesbloMente ativo e rodando."}

# Rota do proxy para requisições do Lovable
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
