from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

# Middleware CORS para aceitar requisições externas (Lovable, etc)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para mais segurança depois, troque "*" por domínios confiáveis
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_BASE = "https://api.openai.com/v1"

@app.post("/v1/chat/completions")
async def proxy(request: Request):
    try:
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
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
