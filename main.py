from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("OPENAI_API_KEY")

@app.post("/v1/chat/completions")
async def proxy_completion(req: Request):
    try:
        body = await req.body()
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=30.0) as client:  # ⏱️ Timeout aumentado
            r = await client.post("https://api.openai.com/v1/chat/completions", content=body, headers=headers)

        return Response(content=r.content, status_code=r.status_code)

    except httpx.ReadTimeout:
        return JSONResponse(
            status_code=504,
            content={
                "error": "O servidor demorou muito para responder. Que tal tentar novamente em alguns segundos?"
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": f"Algo deu errado no servidor: {str(e)}. Por favor, tente novamente mais tarde."
            }
        )
