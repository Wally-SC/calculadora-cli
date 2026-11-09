import math

import pytest

from calculadora import ErroDeExpressao, avaliar
from calculadora.cli import main


@pytest.mark.parametrize(
    "expressao, esperado",
    [
        ("1 + 1", 2),
        ("2 + 3 * 4", 14),
        ("(2 + 3) * 4", 20),
        ("10 / 4", 2.5),
        ("10 // 4", 2),
        ("10 % 4", 2),
        ("2 ** 10", 1024),
        ("-3 + 5", 2),
        ("sqrt(16)", 4.0),
        ("fatorial(5)", 120),
        ("abs(-7)", 7),
    ],
)
def test_expressoes_validas(expressao, esperado):
    assert avaliar(expressao) == esperado


def test_constantes():
    assert avaliar("pi") == math.pi
    assert avaliar("2 * pi") == pytest.approx(2 * math.pi)


@pytest.mark.parametrize(
    "expressao",
    [
        "",
        "   ",
        "1 +",
        "1 / 0",
        "__import__('os').system('echo oi')",
        "open('arquivo')",
        "x + 1",
        "'texto'",
        "2 ** 100000",
        "sqrt(-1)",
        "[1, 2, 3]",
        "True + 1",
    ],
)
def test_expressoes_invalidas_ou_inseguras(expressao):
    with pytest.raises(ErroDeExpressao):
        avaliar(expressao)


def test_cli_sucesso(capsys):
    assert main(["2 + 3 * 4"]) == 0
    assert capsys.readouterr().out.strip() == "14"


def test_cli_erro(capsys):
    assert main(["1 / 0"]) == 1
    assert "divisão por zero" in capsys.readouterr().err
