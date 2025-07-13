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
    body = await request.body()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{OPENAI_API_BASE}/chat/completions",
            headers=headers,
            content=body
        )
    
    return JSONResponse(
        status_code=response.status_code,
        content=response.json()
    )
