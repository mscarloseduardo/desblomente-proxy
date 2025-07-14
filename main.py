from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import openai

# Carrega variáveis do .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

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

        result = {
            "choices": [
                {
                    "message": {
                        "content": response.choices[0].message["content"]
                    }
                }
            ]
        }

        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
