from __future__ import annotations

import argparse
import sys

from calculadora.core import ErroDeExpressao, avaliar


def _formatar(valor: float | int) -> str:
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))
    return str(valor)


def modo_interativo() -> int:
    print("Calculadora — digite uma expressão ('sair' para encerrar)")
    while True:
        try:
            linha = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if linha.lower() in {"sair", "exit", "quit"}:
            return 0
        if not linha:
            continue
        try:
            print(_formatar(avaliar(linha)))
        except ErroDeExpressao as exc:
            print(f"erro: {exc}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="calculadora",
        description="Calculadora de expressões matemáticas (sem eval).",
    )
    parser.add_argument("expressao", nargs="?", help='ex.: "2 + 3 * sqrt(16)"')
    args = parser.parse_args(argv)

    if args.expressao is None:
        return modo_interativo()

    try:
        print(_formatar(avaliar(args.expressao)))
    except ErroDeExpressao as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 1
    return 0
