import json
from unittest.mock import patch

from cpf_auth.handler import handler


def test_invalid_cpf_returns_400():
    result = handler({"body": json.dumps({"cpf": "111.111.111-11"})}, None)
    assert result["statusCode"] == 400


@patch("cpf_auth.handler.find_client_by_cpf", return_value=None)
def test_unknown_client_returns_404(_mock):
    result = handler({"body": json.dumps({"cpf": "52998224725"})}, None)
    assert result["statusCode"] == 404


@patch(
    "cpf_auth.handler.find_client_by_cpf",
    return_value={"id": "id-1", "nome": "Joao", "cpf": "52998224725", "status": "INATIVO"},
)
def test_inactive_client_returns_403(_mock):
    result = handler({"body": json.dumps({"cpf": "52998224725"})}, None)
    assert result["statusCode"] == 403


@patch(
    "cpf_auth.handler.find_client_by_cpf",
    return_value={"id": "id-1", "nome": "Joao", "cpf": "52998224725", "status": "ATIVO"},
)
@patch("cpf_auth.handler.issue_access_token", return_value="jwt-token")
def test_active_client_returns_token(_token, _repo):
    result = handler({"body": json.dumps({"cpf": "529.982.247-25"})}, None)
    body = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert body["accessToken"] == "jwt-token"
    assert body["profile"] == "CLIENTE"
