def normalize(value: str | None) -> str:
    if not value:
        return ""
    return "".join(ch for ch in value if ch.isdigit())


def is_valid_cpf(value: str | None) -> bool:
    cpf = normalize(value)
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False
    return _cpf_digit(cpf, 10) == int(cpf[9]) and _cpf_digit(cpf, 11) == int(cpf[10])


def _cpf_digit(cpf: str, weight_start: int) -> int:
    total = sum(int(cpf[i]) * (weight_start - i) for i in range(weight_start - 1))
    remainder = total % 11
    return 0 if remainder < 2 else 11 - remainder
