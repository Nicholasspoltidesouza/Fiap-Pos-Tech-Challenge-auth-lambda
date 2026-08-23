import json
import logging
import os
import smtplib
from email.message import EmailMessage

LOGGER = logging.getLogger("notify-lambda")
logging.basicConfig(level=logging.INFO)


def _body(event: dict) -> dict:
    raw = event.get("body") or "{}"
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
        payload = _body(event)
    except json.JSONDecodeError:
        return _response(400, {"message": "Invalid JSON body"})

    order_id = payload.get("orderId")
    status = payload.get("status")
    cpf = payload.get("cpfCnpj")
    failed = bool(payload.get("failed"))

    log = {
        "event": "work_order_notification",
        "orderId": order_id,
        "status": status,
        "cpfCnpj": cpf,
        "failed": failed,
        "correlationId": payload.get("correlationId"),
    }
    LOGGER.info(json.dumps(log))

    if failed:
        LOGGER.error(json.dumps({**log, "alert": "work_order_processing_failure"}))

    _send_mail(payload)
    return _response(202, {"accepted": True, "orderId": order_id})


def _send_mail(payload: dict) -> None:
    host = os.getenv("MAIL_HOST", "localhost")
    port = int(os.getenv("MAIL_PORT", "1025"))
    sender = os.getenv("MAIL_FROM", "oficina@oficina.com")
    to = os.getenv("MAIL_TO", "notificacoes@oficina.com")
    message = EmailMessage()
    message["From"] = sender
    message["To"] = to
    message["Subject"] = f"Work order {payload.get('orderId')} -> {payload.get('status')}"
    message.set_content(json.dumps(payload, indent=2, default=str))
    try:
        with smtplib.SMTP(host, port, timeout=5) as smtp:
            smtp.send_message(message)
    except OSError as exc:
        LOGGER.warning(json.dumps({"event": "smtp_failure", "reason": str(exc)}))
