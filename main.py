from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Libera acesso para qualquer origem (ideal para testes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicia cliente da OpenAI com chave secreta da variável de ambiente
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        response = client.chat.completions.create(
            model=body["model"],
            temperature=body.get("temperature", 0.7),
            messages=body["messages"]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
