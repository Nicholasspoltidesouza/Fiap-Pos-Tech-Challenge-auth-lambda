from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from cpf_auth.handler import handler

app = FastAPI(title="Oficina CPF Auth Function", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "UP"}


@app.post("/auth/cpf")
async def authenticate(request: Request):
    body = await request.body()
    event = {"body": body.decode("utf-8")}
    result = handler(event, None)
    return JSONResponse(status_code=result["statusCode"], content=__import__("json").loads(result["body"]))
