import json
from unittest.mock import patch

from notify.handler import handler


@patch("notify.handler._send_mail")
def test_notify_accepts_payload(send_mail):
    payload = {"orderId": "abc", "status": "EM_EXECUCAO", "cpfCnpj": "52998224725"}
    result = handler({"body": json.dumps(payload)}, None)
    assert result["statusCode"] == 202
    send_mail.assert_called_once()


@patch("notify.handler._send_mail")
def test_notify_flags_processing_failure(send_mail):
    payload = {"orderId": "abc", "status": "RECEBIDA", "failed": True}
    result = handler({"body": json.dumps(payload)}, None)
    assert result["statusCode"] == 202
    send_mail.assert_called_once()
