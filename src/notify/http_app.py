import json

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from notify.handler import handler

app = FastAPI(title="Oficina Notify Function", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "UP"}


@app.post("/notify")
async def notify(request: Request):
    body = await request.body()
    result = handler({"body": body.decode("utf-8")}, None)
    return JSONResponse(status_code=result["statusCode"], content=json.loads(result["body"]))
