"""Avaliador seguro de expressões matemáticas.

Usa o módulo ``ast`` em vez de ``eval``: só operadores, números, constantes e
funções da lista branca são aceitos. Qualquer outra coisa gera ErroDeExpressao.
"""

from __future__ import annotations

import ast
import math
import operator

LIMITE_EXPOENTE = 1000


class ErroDeExpressao(ValueError):
    """Expressão inválida, insegura ou impossível de calcular."""


_BINARIOS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARIOS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_FUNCOES = {
    "sqrt": math.sqrt,
    "abs": abs,
    "round": round,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "fatorial": math.factorial,
}

_CONSTANTES = {
    "pi": math.pi,
    "e": math.e,
}


def avaliar(expressao: str) -> float | int:
    """Calcula o valor de ``expressao``.

    >>> avaliar("2 + 3 * 4")
    14
    >>> avaliar("sqrt(16) + 2 ** 3")
    12.0
    """
    if not expressao or not expressao.strip():
        raise ErroDeExpressao("expressão vazia")
    try:
        arvore = ast.parse(expressao.strip(), mode="eval")
    except SyntaxError as exc:
        raise ErroDeExpressao(f"sintaxe inválida: {exc.msg}") from exc
    return _avaliar_no(arvore.body)


def _avaliar_no(no: ast.AST) -> float | int:
    if isinstance(no, ast.Constant):
        if isinstance(no.value, bool) or not isinstance(no.value, (int, float)):
            raise ErroDeExpressao(f"valor não permitido: {no.value!r}")
        return no.value

    if isinstance(no, ast.Name):
        if no.id in _CONSTANTES:
            return _CONSTANTES[no.id]
        raise ErroDeExpressao(f"nome desconhecido: {no.id}")

    if isinstance(no, ast.BinOp):
        operacao = _BINARIOS.get(type(no.op))
        if operacao is None:
            raise ErroDeExpressao("operador não permitido")
        esquerda = _avaliar_no(no.left)
        direita = _avaliar_no(no.right)
        if isinstance(no.op, ast.Pow) and abs(direita) > LIMITE_EXPOENTE:
            raise ErroDeExpressao(f"expoente acima do limite ({LIMITE_EXPOENTE})")
        try:
            return operacao(esquerda, direita)
        except ZeroDivisionError as exc:
            raise ErroDeExpressao("divisão por zero") from exc
        except OverflowError as exc:
            raise ErroDeExpressao("resultado grande demais") from exc

    if isinstance(no, ast.UnaryOp):
        operacao = _UNARIOS.get(type(no.op))
        if operacao is None:
            raise ErroDeExpressao("operador não permitido")
        return operacao(_avaliar_no(no.operand))

    if isinstance(no, ast.Call):
        if not isinstance(no.func, ast.Name) or no.func.id not in _FUNCOES:
            raise ErroDeExpressao("função não permitida")
        if no.keywords:
            raise ErroDeExpressao("argumentos nomeados não são permitidos")
        argumentos = [_avaliar_no(arg) for arg in no.args]
        try:
            return _FUNCOES[no.func.id](*argumentos)
        except (ValueError, TypeError, OverflowError) as exc:
            raise ErroDeExpressao(f"erro em {no.func.id}(): {exc}") from exc

    raise ErroDeExpressao("construção não permitida")
