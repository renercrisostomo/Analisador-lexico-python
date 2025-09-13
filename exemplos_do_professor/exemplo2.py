# =========================
# SCANNER (AFD) – Baseado em Estados
# =========================
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Dict, Tuple

# -------------------------
# Tipos de token (granular)
# -------------------------
class TokenType(Enum):
  # gerais
  ID = auto()
  KEYWORD = auto()
  NUM = auto()
  EOF = auto()
  ERRO = auto()
  # operadores 2-chars
  EQ = auto()   # ==
  NE = auto()   # !=
  LE = auto()   # <=
  GE = auto()   # >=
  # operadores 1-char
  ASSIGN = auto()  # =
  PLUS = auto() # +
  MINUS = auto()   # -
  STAR = auto() # *
  SLASH = auto()   # /
  LT = auto()   # <
  GT = auto()   # >
  # delimitadores
  SEMI = auto() # ;
  COMMA = auto()   # ,
  LPAREN = auto()  # (
  RPAREN = auto()  # )
  LBRACE = auto()  # {
  RBRACE = auto()  # }

@dataclass
class Token:
  tipo: TokenType
  lexema: str  # para ID: "idN"; p/ demais, literal (ou "" p/ EOF)

# -------------------------
# Léxico da linguagem
# -------------------------
KEYWORDS = {"int", "if", "else", "while", "return"}

# -------------------------
# Classes de caracteres p/ AFD
# -------------------------
class CC(Enum):
  WS = auto()    # whitespace
  LETTER = auto()   # A..Z a..z
  DIGIT = auto()     # 0..9
  UNDERSCORE = auto()  # _
  EQUAL = auto()     # =
  LT = auto()    # <
  GT = auto()    # >
  BANG = auto()  # !
  PLUS = auto()  # +
  MINUS = auto()     # -
  STAR = auto()  # *
  SLASH = auto()     # /
  SEMI = auto()  # ;
  COMMA = auto()     # ,
  LPAREN = auto()   # (
  RPAREN = auto()   # )
  LBRACE = auto()   # {
  RBRACE = auto()   # }
  EOF = auto()     # fim da entrada
  OTHER = auto()     # qualquer outro

def class_of(ch: str) -> CC:
  if ch == "\0": return CC.EOF
  if ch.isspace(): return CC.WS
  if ch.isalpha(): return CC.LETTER
  if ch.isdigit(): return CC.DIGIT
  if ch == "_": return CC.UNDERSCORE
  if ch == "=": return CC.EQUAL
  if ch == "<": return CC.LT
  if ch == ">": return CC.GT
  if ch == "!": return CC.BANG
  if ch == "+": return CC.PLUS
  if ch == "-": return CC.MINUS
  if ch == "*": return CC.STAR
  if ch == "/": return CC.SLASH
  if ch == ";": return CC.SEMI
  if ch == ",": return CC.COMMA
  if ch == "(": return CC.LPAREN
  if ch == ")": return CC.RPAREN
  if ch == "{": return CC.LBRACE
  if ch == "}": return CC.RBRACE
  return CC.OTHER

# -------------------------
# Estados do AFD
# -------------------------
class S(Enum):
  START = auto()
  ID = auto()
  NUM = auto()
  NUM_ERR = auto()  # números seguidos de letras/_ → ERRO (ex.: 8a)
  EQ1 = auto()    # lido "="; pode virar "==" ou aceitar "="
  LT1 = auto()    # lido "<"; pode virar "<=" ou aceitar "<"
  GT1 = auto()    # lido ">"; pode virar ">=" ou aceitar ">"
  BANG1 = auto()  # lido "!"; só aceita "!=" (senão ERRO)
  PLUS = auto()
  MINUS = auto()
  STAR = auto()
  SLASH = auto()
  SEMI = auto()
  COMMA = auto()
  LPAREN = auto()
  RPAREN = auto()
  LBRACE = auto()
  RBRACE = auto()
  EOF = auto()
  ERR = auto()    # caractere isolado inválido
  DEAD = auto()  # sem transição (parada para maximal munch)

# -------------------------
# Mapa de estados ACEITÁVEIS → função de criação de token
# (a classificação por tipo é decidida pós-varredura)
# -------------------------
ACCEPTING = {
  S.ID, S.NUM, S.NUM_ERR,
  S.EQ1, S.LT1, S.GT1, S.BANG1,
  S.PLUS, S.MINUS, S.STAR, S.SLASH,
  S.SEMI, S.COMMA, S.LPAREN, S.RPAREN, S.LBRACE, S.RBRACE,
  S.EOF, S.ERR,
}

# -------------------------
# Transições do AFD
# proximo_estado(estado, classe) -> novo estado (ou DEAD)
# -------------------------
def proximo_estado(st: S, cc: CC) -> S:
  # START: decide pelo 1º char
  if st == S.START:
    return {
      CC.LETTER: S.ID,
      CC.UNDERSCORE: S.ID,
      CC.DIGIT: S.NUM,
      CC.EQUAL: S.EQ1,
      CC.LT: S.LT1,
      CC.GT: S.GT1,
      CC.BANG: S.BANG1,
      CC.PLUS: S.PLUS,
      CC.MINUS: S.MINUS,
      CC.STAR: S.STAR,
      CC.SLASH: S.SLASH,
      CC.SEMI: S.SEMI,
      CC.COMMA: S.COMMA,
      CC.LPAREN: S.LPAREN,
      CC.RPAREN: S.RPAREN,
      CC.LBRACE: S.LBRACE,
      CC.RBRACE: S.RBRACE,
      CC.EOF: S.EOF,
      CC.WS: S.START,   # (o caller geralmente pula WS antes)
    }.get(cc, S.ERR)

  # ID: consome LETTER/DIGIT/UNDERSCORE
  if st == S.ID:
    if cc in (CC.LETTER, CC.DIGIT, CC.UNDERSCORE):
      return S.ID
    return S.DEAD

  # NUM: consome dígitos; se vier parte de id → NUM_ERR
  if st == S.NUM:
    if cc == CC.DIGIT:
      return S.NUM
    if cc in (CC.LETTER, CC.UNDERSCORE):
      return S.NUM_ERR
    return S.DEAD

  # NUM_ERR: consome tudo que seria parte de id, permanece erro
  if st == S.NUM_ERR:
    if cc in (CC.LETTER, CC.DIGIT, CC.UNDERSCORE):
      return S.NUM_ERR
    return S.DEAD

  # "=" → "==" ou "="
  if st == S.EQ1:
    if cc == CC.EQUAL:
      return S.DEAD  # aceitará "==" (2 chars) — ver mapeamento ao final
    return S.DEAD   # aceitará "="

  # "<" → "<=" ou "<"
  if st == S.LT1:
    if cc == CC.EQUAL:
      return S.DEAD  # aceitará "<="
    return S.DEAD   # aceitará "<"

  # ">" → ">=" ou ">"
  if st == S.GT1:
    if cc == CC.EQUAL:
      return S.DEAD  # aceitará ">="
    return S.DEAD   # aceitará ">"

  # "!" → "!=" (senão ERRO '!')
  if st == S.BANG1:
    if cc == CC.EQUAL:
      return S.DEAD  # aceitará "!="
    return S.DEAD   # aceitará "!" como ERRO

  # tokens de 1 char: aceitam e param
  if st in {S.PLUS, S.MINUS, S.STAR, S.SLASH,
        S.SEMI, S.COMMA, S.LPAREN, S.RPAREN, S.LBRACE, S.RBRACE,
        S.EOF, S.ERR}:
    return S.DEAD

  return S.DEAD

# -------------------------
# Scanner AFD com maximal munch
# -------------------------
class ScannerAFD:
  def __init__(self, codigo: str):
    self.codigo = codigo
    self.i = 0
    self.tokens: List[Token] = []
    # tabela de símbolos: nome → índice (1-based)
    self.symbols: Dict[str, int] = {}
    self._next_sym_id = 1

  # utilidades de leitura
  def _peek(self) -> str:
    return self.codigo[self.i] if self.i < len(self.codigo) else "\0"

  def _advance(self) -> str:
    ch = self._peek()
    self.i += 1
    return ch

  def _skip_ws(self):
    while self._peek().isspace():
      self._advance()

  # mapeia estado final + lexema → Token
  def _make_token_from_state(self, st: S, lex: str) -> Token:
    # identificador ou palavra-chave
    if st == S.ID:
      if lex in KEYWORDS:
        return Token(TokenType.KEYWORD, lex)
      # ID: gerar idN e registrar
      if lex not in self.symbols:
        self.symbols[lex] = self._next_sym_id
        self._next_sym_id += 1
      sid = self.symbols[lex]
      return Token(TokenType.ID, f"id{sid}")

    # números válidos
    if st == S.NUM:
      return Token(TokenType.NUM, lex)

    # número inválido seguido de letras/_ (8a)
    if st == S.NUM_ERR:
      return Token(TokenType.ERRO, lex)

    # operadores compostos e simples
    if st == S.EQ1:
      return Token(TokenType.EQ if lex == "==" else TokenType.ASSIGN, lex)
    if st == S.LT1:
      return Token(TokenType.LE if lex == "<=" else TokenType.LT, lex)
    if st == S.GT1:
      return Token(TokenType.GE if lex == ">=" else TokenType.GT, lex)
    if st == S.BANG1:
      return Token(TokenType.NE if lex == "!=" else TokenType.ERRO, lex)

    if st == S.PLUS:  return Token(TokenType.PLUS,  lex)
    if st == S.MINUS: return Token(TokenType.MINUS, lex)
    if st == S.STAR:  return Token(TokenType.STAR,  lex)
    if st == S.SLASH: return Token(TokenType.SLASH, lex)

    # delimitadores
    if st == S.SEMI:   return Token(TokenType.SEMI,   lex)
    if st == S.COMMA:  return Token(TokenType.COMMA,  lex)
    if st == S.LPAREN: return Token(TokenType.LPAREN, lex)
    if st == S.RPAREN: return Token(TokenType.RPAREN, lex)
    if st == S.LBRACE: return Token(TokenType.LBRACE, lex)
    if st == S.RBRACE: return Token(TokenType.RBRACE, lex)

    if st == S.EOF: return Token(TokenType.EOF, "")

    # caractere inválido isolado
    return Token(TokenType.ERRO, lex)

  def scan_all(self) -> List[Token]:
    while True:
      self._skip_ws()
      start = self.i
      st = S.START

      # se estamos no EOF, emite EOF e encerra
      if self._peek() == "\0":
        self.tokens.append(Token(TokenType.EOF, ""))
        break

      last_accept_state: S | None = None
      last_accept_index = start

      # avança enquanto houver transição (maximal munch)
      while True:
        ch = self._peek()
        cc = class_of(ch)
        nxt = proximo_estado(st, cc)

        if nxt == S.DEAD:
          # parar: emite o último estado de aceitação conhecido
          if last_accept_state is None:
            # nenhum estado aceito: consome 1 char como ERRO
            bad = self._advance()
            self.tokens.append(Token(TokenType.ERRO, bad))
          else:
            lex = self.codigo[start:last_accept_index]
            self.i = last_accept_index  # volta para o último aceito
            # Ajuste especial para operadores de 2 chars:
            # se estado for EQ1/LT1/GT1/BANG1 e houver '=' logo após,
            # o lexema aceito deve incluir esse '='
            if last_accept_state in {S.EQ1, S.LT1, S.GT1, S.BANG1}:
              # checa se de fato era 2-chars
              if self.i < len(self.codigo) and self.codigo[self.i - 1] in "=<>!":
                # já estamos posicionados após o 1º char.
                # se o próximo for '=', inclui.
                if self._peek() == "=" and (self.codigo[self.i - 1] in "=<>!"):
                  lex = self.codigo[start:self.i + 1]
                  self.i += 1
            tok = self._make_token_from_state(last_accept_state, lex)
            self.tokens.append(tok)
          break
        else:
          # consome e atualiza estado
          self._advance()
          st = nxt
          # se é estado de aceitação, guarda posição
          if st in ACCEPTING:
            last_accept_state = st
            last_accept_index = self.i

    return self.tokens

  # Impressões didáticas
  def print_tokens(self):
    print("\n=== LISTA DE TOKENS ===")
    for t in self.tokens:
      print(f"{t.tipo.name:<7}  {t.lexema}")

  def print_symbol_table(self, sort_by_name: bool = False):
    print("\n=== TABELA DE SÍMBOLOS ===")
    items = list(self.symbols.items())
    if sort_by_name:
      items.sort(key=lambda x: x[0])
    for name, idx in items:
      print(f"id{idx:<3}  {name}")

# -------------------------
# Exemplo de uso
# -------------------------
if __name__ == "__main__":
  codigo = """
  int a = 10;
  int b = 30;
  if (a >= 10) {
    a = b + 5;
  }
  8a
  """
  sc = ScannerAFD(codigo)
  sc.scan_all()
  sc.print_tokens()
  sc.print_symbol_table(sort_by_name=False)
