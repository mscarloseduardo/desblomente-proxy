from fastapi import FastAPI, Request
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    messages = body.get("messages", [])
    model = body.get("model", "gpt-4")
    temperature = body.get("temperature", 0.7)

    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=messages
    )

    return {"choices": [{"message": {"content": response.choices[0].message.content}}]}
