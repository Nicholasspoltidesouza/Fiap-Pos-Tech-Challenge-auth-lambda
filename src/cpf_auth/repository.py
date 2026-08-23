import os

import psycopg

from cpf_auth.validator import normalize


def _dsn() -> str:
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    name = os.getenv("POSTGRES_DB", "oficina_mec_db")
    user = os.getenv("POSTGRES_USER", "admin")
    password = os.getenv("POSTGRES_PASSWORD", "admin")
    return f"host={host} port={port} dbname={name} user={user} password={password}"


def find_client_by_cpf(cpf: str) -> dict | None:
    digits = normalize(cpf)
    sql = """
        SELECT id::text, nome, cpf_cnpj, COALESCE(status, 'ATIVO') AS status
        FROM tb_cliente
        WHERE regexp_replace(cpf_cnpj, '[^0-9]', '', 'g') = %s
        LIMIT 1
    """
    with psycopg.connect(_dsn()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (digits,))
            row = cur.fetchone()
            if row is None:
                return None
            return {"id": row[0], "nome": row[1], "cpf": normalize(row[2]), "status": row[3]}
