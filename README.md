# Analisador Léxico Python

Analisador léxico em Python para a disciplina Compiladores do curso Ciências da Computação 8º semestre do IFCE Maracanaú.

## Sobre o Projeto

Este projeto implementa um analisador léxico manual (sem uso de geradores automáticos) para uma linguagem semelhante a C. O analisador recebe código-fonte como entrada e produz:

- Lista de tokens reconhecidos (tipo, lexema)
- Tabela de símbolos com identificadores e contagem de ocorrências
- Tratamento de erros léxicos

## Como Executar

### Executar o analisador

```bash
python lexer_manual.py
```

### Executar testes

```bash
pytest test_lexer.py
```

## Estrutura do Projeto

- `lexer_manual.py` - Analisador léxico
- `test_lexer.py` - Testes com validação de contagem de tokens
- `trabalho.md` - Especificação do trabalho

## Requisitos

- Python 3.x
- pytest (para executar os testes)
