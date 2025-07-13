from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import openai
import os

app = FastAPI()

# Defina sua chave secreta da OpenAI como variável de ambiente no Render (não aqui diretamente)
openai.api_key = os.environ.get("OPENAI_API_KEY")


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    try:
        body = await request.json()
        response = openai.ChatCompletion.create(**body)
        return JSONResponse(content=response)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
