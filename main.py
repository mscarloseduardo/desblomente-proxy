from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
from dotenv import load_dotenv

# Tenta carregar .env se existir
load_dotenv()

app = FastAPI()

# Libera tudo para testes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚨 LOG: verificar se a variável existe
api_key = os.getenv("OPENAI_API_KEY")
print(f"🔑 OPENAI_API_KEY carregada: {api_key[:5]}...")  # mostra só o começo por segurança

if not api_key:
    print("❌ ERRO: OPENAI_API_KEY não encontrada!")
else:
    print("✅ API Key carregada com sucesso!")

client = OpenAI(api_key=api_key)

@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        print("📥 Requisição recebida:", body)

        response = client.chat.completions.create(
            model=body["model"],
            temperature=body.get("temperature", 0.7),
            messages=body["messages"]
        )

        print("📤 Resposta enviada:", response.choices[0].message.content)
        return {"response": response.choices[0].message.content}

    except Exception as e:
        print("❌ ERRO durante a requisição:", str(e))
        return {"error": str(e)}
