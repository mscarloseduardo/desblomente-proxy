from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Libera acesso CORS para qualquer origem (necessário para Lovable e testes externos)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou substitua por ["https://lovable.app"] se quiser limitar
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    
    try:
        response = client.chat.completions.create(
            model=data["model"],
            temperature=data.get("temperature", 0.7),
            messages=data["messages"]
        )
        return { "response": response.choices[0].message.content }
    
    except Exception as e:
        return { "error": str(e) }
