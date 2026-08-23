import json

from cpf_auth.repository import find_client_by_cpf
from cpf_auth.tokens import issue_access_token
from cpf_auth.validator import is_valid_cpf, normalize


def _body(event: dict) -> dict:
    raw = event.get("body") or "{}"
    if event.get("isBase64Encoded"):
        import base64

        raw = base64.b64decode(raw).decode("utf-8")
    if isinstance(raw, dict):
        return raw
    return json.loads(raw or "{}")


def _response(status: int, payload: dict) -> dict:
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(payload),
    }


def handler(event, _context):
    try:
        body = _body(event)
    except json.JSONDecodeError:
        return _response(400, {"message": "Invalid JSON body"})

    cpf = normalize(body.get("cpf") or body.get("cpfCnpj"))
    if not is_valid_cpf(cpf):
        return _response(400, {"message": "Invalid CPF"})

    client = find_client_by_cpf(cpf)
    if client is None:
        return _response(404, {"message": "Client not found"})
    if client["status"] != "ATIVO":
        return _response(403, {"message": "Client is not active", "status": client["status"]})

    token = issue_access_token(client)
    return _response(
        200,
        {
            "accessToken": token,
            "tokenType": "Bearer",
            "profile": "CLIENTE",
            "cpf": client["cpf"],
            "clientId": client["id"],
            "name": client["nome"],
        },
    )
