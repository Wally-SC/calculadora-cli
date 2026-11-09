# calculadora-cli

Calculadora de expressões matemáticas para o terminal, feita em Python puro.

O ponto central do projeto é **não usar `eval`**: a expressão é convertida em
árvore sintática com o módulo `ast` e só operadores, números, constantes e
funções de uma lista branca são avaliados. Código malicioso como
`__import__('os').system(...)` é rejeitado.

## Uso

```bash
python -m calculadora "2 + 3 * 4"          # 14
python -m calculadora "sqrt(16) + 2 ** 3"  # 12
python -m calculadora                      # modo interativo
```

Operadores: `+ - * / // % **` e parênteses.
Funções: `sqrt abs round sin cos tan log log10 exp fatorial`.
Constantes: `pi`, `e`.

## Testes

```bash
pip install pytest
pytest
```

## O que este projeto pratica

- Análise de árvore sintática (`ast`) e lista branca de operações
- Tratamento de erros com exceção própria
- Testes parametrizados com pytest
- CLI com `argparse`
