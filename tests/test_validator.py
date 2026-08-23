from cpf_auth.validator import is_valid_cpf, normalize


def test_normalize_strips_mask():
    assert normalize("529.982.247-25") == "52998224725"


def test_valid_cpf():
    assert is_valid_cpf("529.982.247-25")
    assert is_valid_cpf("39053344705")


def test_invalid_cpf():
    assert not is_valid_cpf("111.111.111-11")
    assert not is_valid_cpf("12345678900")
    assert not is_valid_cpf("")
