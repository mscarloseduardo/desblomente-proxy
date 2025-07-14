from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuste para ["https://lovable.dev"] se quiser restringir depois
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Garanta que não tenha \n invisível na chave
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()
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
