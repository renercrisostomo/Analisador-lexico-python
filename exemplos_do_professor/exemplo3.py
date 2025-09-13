# lexer_ply.py
import re
import ply.lex as lex
from collections import OrderedDict

# -----------------------------
# Palavras reservadas
# -----------------------------
reserved = {
  "int": "INT",
  "float": "FLOAT",
  "return": "RETURN",
  "if": "IF",
  "else": "ELSE",
  "while": "WHILE",
  "for": "FOR",
  "break": "BREAK",
  "continue": "CONTINUE",
}

# -----------------------------
# Lista de tokens
# -----------------------------
tokens = (
  # gerais
  "ID", "NUM",
  # operadores 2-chars
  "EQ", "NE", "LE", "GE",
  # operadores 1-char
  "ASSIGN", "PLUS", "MINUS", "TIMES", "DIVIDE", "LT", "GT",
  # delimitadores
  "SEMI", "COMMA", "LPAREN", "RPAREN", "LBRACE", "RBRACE",
  # erro específico (número seguido de letras)
  "BADNUMID",
) + tuple(reserved.values())

# -----------------------------
# Tokens simples (regex diretos)
# -----------------------------
t_EQ     = r"=="
t_NE     = r"!="
t_LE     = r"<="
t_GE     = r">="

t_ASSIGN = r"="
t_PLUS   = r"\+"
t_MINUS  = r"-"
t_TIMES  = r"\*"
t_DIVIDE = r"/"
t_LT     = r"<"
t_GT     = r">"

t_SEMI   = r";"
t_COMMA  = r","
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"

# -----------------------------
# Ignorar espaços e tabs
# -----------------------------
t_ignore = " \t"

# -----------------------------
# Comentários
# -----------------------------
def t_BLOCKCOMMENT(t):
  r"/\*[^*]*\*+(?:[^/*][^*]*\*+)*/"
  # ignora (não retorna token)
  pass

def t_LINECOMMENT(t):
  r"//[^\n]*"
  pass

# -----------------------------
# Nova linha (atualiza linha se quiser)
# -----------------------------
def t_newline(t):
  r"\n+"
  t.lexer.lineno += len(t.value)

# -----------------------------
# BADNUMID: número seguido de letra/_ (ex.: 8a, 12foo)
# (coloque ANTES de NUM para ter prioridade)
# -----------------------------
def t_BADNUMID(t):
  r"\d+[A-Za-z_]\w*"
  # Mantemos como token para tratarmos como erro na visualização
  return t

# -----------------------------
# Números inteiros
# -----------------------------
def t_NUM(t):
  r"\d+"
  t.value = int(t.value)
  return t

# -----------------------------
# Identificadores / Reservadas
# -----------------------------
def t_ID(t):
  r"[A-Za-z_]\w*"
  t.type = reserved.get(t.value, "ID")
  return t

# -----------------------------
# Erros léxicos genéricos
# -----------------------------
def t_error(t):
  # Consome 1 caractere inválido e segue
  print(f"[lex] Erro léxico: caractere inválido '{t.value[0]}'")
  t.lexer.skip(1)

# -----------------------------
# Criação do lexer
# -----------------------------
lexer = lex.lex(reflags=re.MULTILINE)

# -----------------------------
# Visualização: tokens + tabela de símbolos
# -----------------------------
def scan_with_symbols(code: str):
  lexer.input(code)
  raw = list(lexer)  # tokens brutos de PLY

  # Tabela de símbolos (ordem de aparição)
  symtab = OrderedDict()  # nome -> idN
  next_id = 1

  # Lista de tokens “bonitos” (ID rotulado como idN)
  pretty_tokens = []

  for tk in raw:
    if tk.type == "ID":
      if tk.value not in symtab:
        symtab[tk.value] = f"id{next_id}"
        next_id += 1
      pretty_tokens.append(("ID", symtab[tk.value]))
    elif tk.type == "NUM":
      pretty_tokens.append(("NUM", str(tk.value)))
    elif tk.type == "BADNUMID":
      pretty_tokens.append(("ERRO", tk.value))  # ex.: 8a
    else:
      # operadores, delimitadores e reservadas: mantemos tipo e lexema
      lexema = tk.value if isinstance(tk.value, str) else str(tk.value)
      pretty_tokens.append((tk.type, lexema))

  # Acrescenta EOF no final (consistente com exemplos anteriores)
  pretty_tokens.append(("EOF", ""))

  return pretty_tokens, symtab

def print_tokens(tokens):
  print("\n=== LISTA DE TOKENS ===")
  for ttype, lexeme in tokens:
    print(f"{ttype:<9} {lexeme}")

def print_symbol_table(symtab: OrderedDict):
  print("\n=== TABELA DE SÍMBOLOS ===")
  for name, rid in symtab.items():
    print(f"{rid:<4} {name}")

# -----------------------------
# Exemplo de uso
# -----------------------------
if __name__ == "__main__":
  codigo = """
  int a = 10;
  float b = a + 5;
  if (a >= 10) {
    b = b - 1;
  }
  /* bloco
     de comentário */
  // comentário de linha
  8a
  """
  tokens, symtab = scan_with_symbols(codigo)
  print_tokens(tokens)
  print_symbol_table(symtab)