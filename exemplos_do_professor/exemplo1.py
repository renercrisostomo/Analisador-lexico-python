from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Dict

# =========================
# TIPOS DE TOKEN (granular)
# =========================
class TokenType(Enum):
  # categorias gerais
  ID = auto()       # identificadores (variáveis, funções)
  KEYWORD = auto()  # palavras reservadas (int, if, while, etc.)
  NUM = auto()      # números inteiros
  EOF = auto()      # fim de arquivo
  ERRO = auto()     # sequência inválida (ex.: "8a")

  # operadores de 2 caracteres
  EQ = auto()       # ==
  NE = auto()       # !=
  LE = auto()       # <=
  GE = auto()       # >=

  # operadores de 1 caractere
  ASSIGN = auto()   # =
  PLUS = auto()     # +
  MINUS = auto()    # -
  STAR = auto()     # *
  SLASH = auto()    # /
  LT = auto()       # <
  GT = auto()       # >

  # delimitadores
  SEMI = auto()     # ;
  COMMA = auto()    # ,
  LPAREN = auto()   # (
  RPAREN = auto()   # )
  LBRACE = auto()   # {
  RBRACE = auto()   # }

# estrutura de um token
@dataclass
class Token:
  tipo: TokenType   # tipo (enum acima)
  lexema: str       # representação textual do token
            # para ID será idN; para outros, o lexema literal

# =========================
# CONFIGURAÇÃO DA LINGUAGEM
# =========================
KEYWORDS = {"int", "if", "else", "while", "return"}  # palavras reservadas

# operadores compostos (2 chars)
OPERATORS_2 = {
  "==": TokenType.EQ,
  "!=": TokenType.NE,
  "<=": TokenType.LE,
  ">=": TokenType.GE,
}
# operadores simples (1 char)
OPERATORS_1 = {
  "=": TokenType.ASSIGN,
  "+": TokenType.PLUS,
  "-": TokenType.MINUS,
  "*": TokenType.STAR,
  "/": TokenType.SLASH,
  "<": TokenType.LT,
  ">": TokenType.GT,
}
# delimitadores (pontuação)
DELIMS = {
  ";": TokenType.SEMI,
  ",": TokenType.COMMA,
  "(": TokenType.LPAREN,
  ")": TokenType.RPAREN,
  "{": TokenType.LBRACE,
  "}": TokenType.RBRACE,
}

# =========================
# SCANNER MANUAL
# =========================
class Scanner:
  def __init__(self, codigo: str):
    self.codigo = codigo
    self.i = 0                     # índice atual no código
    self.tokens: List[Token] = []  # lista de tokens encontrados
    self.symbols: Dict[str, int] = {}  # tabela de símbolos {nome: índice}
    self._next_sym_id = 1          # próximo id para identificadores (id1, id2...)

  # olhar caractere atual sem consumir
  def _peek(self) -> str:
    return self.codigo[self.i] if self.i < len(self.codigo) else "\0"

  # olhar dois caracteres (para operadores de 2 chars)
  def _peek2(self) -> str:
    if self.i + 1 < len(self.codigo):
      return self.codigo[self.i] + self.codigo[self.i + 1]
    return "\0\0"

  # avança e retorna caractere atual
  def _advance(self) -> str:
    ch = self._peek()
    self.i += 1
    return ch

  # regra: identificador começa com letra ou underscore
  @staticmethod
  def _is_ident_start(ch: str) -> bool:
    return ch.isalpha() or ch == "_"

  # regra: dentro do identificador pode ter letras, dígitos ou underscore
  @staticmethod
  def _is_ident_part(ch: str) -> bool:
    return ch.isalnum() or ch == "_"

  # emite um identificador (gera idN e atualiza tabela de símbolos)
  def _emit_id(self, name: str):
    if name not in self.symbols:
      self.symbols[name] = self._next_sym_id
      self._next_sym_id += 1
    sym_id = self.symbols[name]
    self.tokens.append(Token(TokenType.ID, f"id{sym_id}"))

  # função principal: percorre todo o código e gera lista de tokens
  def scan_all(self) -> List[Token]:
    while self.i < len(self.codigo):
      ch = self._peek()

      # ignora espaços em branco
      if ch.isspace():
        self._advance()
        continue

      # Identificadores e palavras-chave
      if self._is_ident_start(ch):
        lex = self._advance()
        while self._is_ident_part(self._peek()):
          lex += self._advance()
        if lex in KEYWORDS:
          self.tokens.append(Token(TokenType.KEYWORD, lex))
        else:
          self._emit_id(lex)
        continue

      # Números
      if ch.isdigit():
        lex = self._advance()
        while self._peek().isdigit():
          lex += self._advance()
        # se após número vier letra/_ → erro único (ex: "8a")
        if self._is_ident_part(self._peek()):
          while self._is_ident_part(self._peek()):
            lex += self._advance()
          self.tokens.append(Token(TokenType.ERRO, lex))
        else:
          self.tokens.append(Token(TokenType.NUM, lex))
        continue

      # Operadores (checa primeiro os de 2 chars)
      two = self._peek2()
      if two in OPERATORS_2:
        self.tokens.append(Token(OPERATORS_2[two], two))
        self.i += 2
        continue
      if ch in OPERATORS_1:
        self.tokens.append(Token(OPERATORS_1[ch], self._advance()))
        continue

      # Delimitadores
      if ch in DELIMS:
        self.tokens.append(Token(DELIMS[ch], self._advance()))
        continue

      # Qualquer outro caractere é erro
      self.tokens.append(Token(TokenType.ERRO, self._advance()))

    # fim de arquivo
    self.tokens.append(Token(TokenType.EOF, ""))
    return self.tokens

  # impressão simples da lista de tokens
  def print_tokens(self):
    print("\n=== LISTA DE TOKENS ===")
    for t in self.tokens:
      print(f"{t.tipo.name:<7}  {t.lexema}")

  # impressão da tabela de símbolos
  def print_symbol_table(self, sort_by_name: bool = False):
    print("\n=== TABELA DE SÍMBOLOS ===")
    items = list(self.symbols.items())
    if sort_by_name:
      items.sort(key=lambda x: x[0])  # ordena alfabeticamente
    for name, idx in items:
      print(f"id{idx:<3}  {name}")

# =========================
# EXEMPLO DE USO
# =========================
if __name__ == "__main__":
  codigo = """
  int a = 10;
  int b = 30;
  if (a >= 10) {
    a = b + 5;
  }
  int 8a
  """
  codigo2 = """
  #include <stdio.h>

  int main(void) {
    printf("Hello, world!\n");
    return 0;
  }
  """
  codigo3 = """
  int main(void) {
    int x = 42;
    float y = 3.14;
    char c = 'a';

    x = x + 10;
    y = y * 2;
    c = '\n';

    return x;
  }
  """
  codigo4 = """
  int main(void) {
    int i = 0;

    while (i < 5) {
        if (i % 2 == 0) {
          printf("even\n");
        } else {
          printf("odd\n");
        }
        i++;
    }

    return 0;
  }
  """
  
  sc = Scanner(codigo2)
  sc.scan_all()
  sc.print_tokens()
  sc.print_symbol_table(sort_by_name=False)