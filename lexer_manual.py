# Analisador Léxico Manual em Python - Compiladores
# Francisco Renêr Lopes Crisostomo

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Dict

# =========================
# TIPOS DE TOKEN (granular)
# =========================
class TokenType(Enum):
  # categorias gerais
  ID = auto()            # identificadores (variáveis, funções)
  KEYWORD = auto()       # palavras reservadas (int, if, while, etc.)
  NUM = auto()           # números inteiros
  FLOAT = auto()         # números reais
  CHAR = auto()          # literal de caractere
  STRING = auto()        # literal de string
  PP_DIRECTIVE = auto()  # diretiva de pré-processador
  EOF = auto()           # fim de arquivo
  ERRO = auto()          # sequência inválida (ex.: "8a")

  # operadores de 2 ou mais caracteres
  EQ = auto()       # ==
  NE = auto()       # !=
  LE = auto()       # <=
  GE = auto()       # >=
  AND = auto()      # &&
  OR = auto()       # ||
  ARROW = auto()    # ->
  ELLIPSIS = auto() # ...

  # operadores de atribuição compostos
  PLUSEQ = auto()   # +=
  MINUSEQ = auto()  # -=
  STAREQ = auto()   # *=
  SLASHEQ = auto()  # /=

  # operadores de 1 caractere
  ASSIGN = auto()   # =
  PLUS = auto()     # +
  MINUS = auto()    # -
  STAR = auto()     # *
  SLASH = auto()    # /
  MOD = auto()      # %
  LT = auto()       # <
  GT = auto()       # >
  NOT = auto()      # !

  # delimitadores
  SEMI = auto()     # ;
  COMMA = auto()    # ,
  DOT = auto()      # .
  LPAREN = auto()   # (
  RPAREN = auto()   # )
  LBRACE = auto()   # {
  RBRACE = auto()   # }
  LBRACKET = auto() # [
  RBRACKET = auto() # ]

# estrutura de um token
@dataclass
class Token:
  tipo: TokenType   # tipo (enum acima)
  lexema: str       # representação textual do token
            # para ID será idN; para outros, o lexema literal

# =========================
# CONFIGURAÇÃO DA LINGUAGEM
# =========================
KEYWORDS = {
  "int", "float", "char", "if", "else", "while", "return", "for", "do", "switch", "case", "break", "continue", "void", "struct", "typedef", "const", "unsigned", "signed", "static", "enum", "sizeof", "goto", "default", "long", "short", "double", "register", "volatile", "extern", "auto"
}

# operadores compostos (2 ou mais chars)
OPERATORS_2PLUS = {
  "==": TokenType.EQ,
  "!=": TokenType.NE,
  "<=": TokenType.LE,
  ">=": TokenType.GE,
  "&&": TokenType.AND,
  "||": TokenType.OR,
  "->": TokenType.ARROW,
  "...": TokenType.ELLIPSIS,
  "+=": TokenType.PLUSEQ,
  "-=": TokenType.MINUSEQ,
  "*=": TokenType.STAREQ,
  "/=": TokenType.SLASHEQ,
}
# operadores simples (1 char)
OPERATORS_1 = {
  "=": TokenType.ASSIGN,
  "+": TokenType.PLUS,
  "-": TokenType.MINUS,
  "*": TokenType.STAR,
  "/": TokenType.SLASH,
  "%": TokenType.MOD,
  "<": TokenType.LT,
  ">": TokenType.GT,
  "!": TokenType.NOT,
}
# delimitadores (pontuação)
DELIMS = {
  ";": TokenType.SEMI,
  ",": TokenType.COMMA,
  ".": TokenType.DOT,
  "(": TokenType.LPAREN,
  ")": TokenType.RPAREN,
  "{": TokenType.LBRACE,
  "}": TokenType.RBRACE,
  "[": TokenType.LBRACKET,
  "]": TokenType.RBRACKET,
}

# =========================
# SCANNER MANUAL
# =========================
class Scanner:
  def __init__(self, codigo: str):
    self.codigo = codigo
    self.i = 0                     # índice atual no código
    self.tokens: List[Token] = []  # lista de tokens encontrados
    self.symbols = {}  # type: Dict[str, Dict[str, int]]  # tabela de símbolos {nome: {id: int, count: int}}
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

  # emite um identificador (gera idN e atualiza tabela de símbolos com contagem)
  def _emit_id(self, name: str):
    if name not in self.symbols:
      self.symbols[name] = {"id": self._next_sym_id, "count": 1}
      self._next_sym_id += 1
    else:
      self.symbols[name]["count"] += 1
    sym_id = self.symbols[name]["id"]
    self.tokens.append(Token(TokenType.ID, f"id{sym_id}"))

  # função principal: percorre todo o código e gera lista de tokens
  def scan_all(self) -> List[Token]:


    while self.i < len(self.codigo):
      ch = self._peek()

      # ignora espaços em branco
      if ch.isspace():
        self._advance()
        continue


      # ignora comentários de linha (// ... até fim da linha)
      if ch == '/' and self._peek2() == '//':
        self._advance()  # /
        self._advance()  # /
        while self._peek() not in '\n\0':
          self._advance()
        if self._peek() == '\n':
          self._advance()
        continue

      # ignora comentários de bloco (/* ... */)
      if ch == '/' and self._peek2() == '/*':
        self._advance()  # /
        self._advance()  # *
        while True:
          if self._peek() == '\0':
            break  # erro: comentário não fechado, mas apenas ignora
          if self._peek() == '*' and self.codigo[self.i+1:self.i+2] == '/':
            self._advance()  # *
            self._advance()  # /
            break
          self._advance()
        continue

      # Diretiva de pré-processador (linha começando com # em qualquer lugar da linha)
      if ch == "#":
        lex = self._advance()
        while self._peek() not in "\n\0":
          lex += self._advance()
        self.tokens.append(Token(TokenType.PP_DIRECTIVE, lex.strip()))
        if self._peek() == '\n':
          self._advance()
        continue


      # Literais de string
      if ch == '"':
        lex = self._advance()
        closed = False
        while self._peek() != '\0':
          c = self._advance()
          lex += c
          if c == '\n':
            lex += c
            continue
          if c == '\\' and self._peek() != '\0':
            lex += self._advance()
            continue
          if c == '"' and (len(lex) < 2 or lex[-2] != '\\'):
            closed = True
            break
          if c == '\n':
            break
        if closed:
          self.tokens.append(Token(TokenType.STRING, lex))
        else:
          self.tokens.append(Token(TokenType.ERRO, lex))
        continue

      # Literais de caractere
      if ch == "'":
        lex = self._advance()
        closed = False
        while self._peek() != '\0':
          c = self._advance()
          lex += c
          if c == '\n':
            lex += c
            continue
          if c == '\\' and self._peek() != '\0':
            lex += self._advance()
            continue
          if c == "'" and (len(lex) < 2 or lex[-2] != '\\'):
            closed = True
            break
          if c == '\n':
            break
        if closed:
          self.tokens.append(Token(TokenType.CHAR, lex))
        else:
          self.tokens.append(Token(TokenType.ERRO, lex))
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
      if ch.isdigit() or (ch == '.' and self._peek( ) and self._peek() != '\0' and self._peek().isdigit()):
        lex = ''
        is_float = False
        if ch == '.':
          lex += self._advance()
          is_float = True
        else:
          lex += self._advance()
          while self._peek().isdigit():
            lex += self._advance()
        # Float
        if self._peek() == ".":
          lookahead = self.codigo[self.i+1] if self.i+1 < len(self.codigo) else "\0"
          if lookahead.isdigit():
            lex += self._advance()  # pega o ponto
            is_float = True
            while self._peek().isdigit():
              lex += self._advance()
        # Erro: vírgula como separador decimal
        if self._peek() == ",":
          lex += self._advance()
          while self._peek().isdigit():
            lex += self._advance()
          self.tokens.append(Token(TokenType.ERRO, lex))
          continue
        # se após número vier letra/_ → erro único (ex: "8a")
        if self._is_ident_part(self._peek()):
          while self._is_ident_part(self._peek()):
            lex += self._advance()
          self.tokens.append(Token(TokenType.ERRO, lex))
        else:
          if is_float:
            self.tokens.append(Token(TokenType.FLOAT, lex))
          else:
            self.tokens.append(Token(TokenType.NUM, lex))
        continue

      # Operadores (checa primeiro os de 3, depois 2 chars)
      three = self.codigo[self.i:self.i+3]
      if three in OPERATORS_2PLUS:
        self.tokens.append(Token(OPERATORS_2PLUS[three], three))
        self.i += 3
        continue
      two = self._peek2()
      if two in OPERATORS_2PLUS:
        self.tokens.append(Token(OPERATORS_2PLUS[two], two))
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
    for name, data in items:
      print(f"id{data['id']:<3}  {name:<15}  ocorrências: {data['count']}")

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
  
  exemplos = [
    ("codigo", codigo),
    ("codigo2", codigo2),
    ("codigo3", codigo3),
    ("codigo4", codigo4),
  ]
  for nome, cod in exemplos:
    print(f"\n{'='*40}\nExemplo: {nome}\n{'='*40}")
    sc = Scanner(cod)
    sc.scan_all()
    sc.print_tokens()
    sc.print_symbol_table(sort_by_name=False)