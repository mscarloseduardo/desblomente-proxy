from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
import traceback

app = FastAPI()

# CORS para permitir chamadas do Lovable ou outras origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cliente OpenAI usando chave vinda do ambiente
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        response = client.chat.completions.create(
            model=data.get("model", "gpt-4"),
            messages=data["messages"],
            temperature=data.get("temperature", 0.7)
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        print("Erro interno:\n", traceback.format_exc())
        return {"error": str(e)}
