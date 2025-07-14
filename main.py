from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    messages = body.get("messages", [])
    model = body.get("model", "gpt-4")
    temperature = body.get("temperature", 0.7)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )

        return {
            "choices": [
                {
                    "message": {
                        "content": response.choices[0].message.content
                    }
                }
            ]
        }

    except Exception as e:
        return {"error": str(e)}
