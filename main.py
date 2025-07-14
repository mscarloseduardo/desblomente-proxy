from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_BASE = "https://api.openai.com/v1"

@app.post("/v1/chat/completions")
async def proxy(request: Request):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    # 🧪 CAPTURA O CORPO DA REQUISIÇÃO
    body = await request.body()
    print("➡️ Corpo recebido:", body.decode())

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{OPENAI_API_BASE}/chat/completions",
                headers=headers,
                content=body
            )
        except Exception as e:
            print("❌ Erro ao chamar a OpenAI:", str(e))
            return JSONResponse(status_code=500, content={"error": "Erro ao chamar a OpenAI"})

    # 🧪 MOSTRA A RESPOSTA DA OPENAI
    print("⬅️ Status:", response.status_code)
    print("⬅️ Conteúdo:", response.text)

    return JSONResponse(
        status_code=response.status_code,
        content=response.json()
    )
