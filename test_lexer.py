import pytest
from lexer_manual import Scanner, TokenType
from collections import Counter

codigo = '''
int a = 10;
int b = 30;
if (a >= 10) {
    a = b + 5;
}
int 8a
'''
codigo2 = '''
#include <stdio.h>

int main(void) {
    printf("Hello, world!\n");
    return 0;
}
'''
codigo3 = '''
int main(void) {
    int x = 42;
    float y = 3.14;
    char c = 'a';

    x = x + 10;
    y = y * 2;
    c = '\n';

    return x;
}
'''
codigo4 = '''
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
'''

def scan_and_types_and_symbols(code):
    sc = Scanner(code)
    tokens = sc.scan_all()
    tipos = [t.tipo for t in tokens]
    tipo_counts = Counter(tipos)
    return tipos, sc.symbols, tipo_counts

def test_codigo():
    tipos, symbols, tipo_counts = scan_and_types_and_symbols(codigo)
    assert TokenType.KEYWORD in tipos
    assert TokenType.ID in tipos
    assert TokenType.NUM in tipos
    assert TokenType.ERRO in tipos
    assert tipos[-1] == TokenType.EOF
    assert symbols['a']['count'] == 3
    assert symbols['b']['count'] == 2
    assert tipo_counts[TokenType.KEYWORD] == 4  # int, int, if, int
    assert tipo_counts[TokenType.ID] == 5       # a, b, a, b, a
    assert tipo_counts[TokenType.NUM] == 4      # 10, 30, 10, 5
    assert tipo_counts[TokenType.ERRO] == 1     # 8a
    assert tipo_counts[TokenType.EOF] == 1

def test_codigo2():
    tipos, symbols, tipo_counts = scan_and_types_and_symbols(codigo2)
    assert TokenType.PP_DIRECTIVE in tipos
    assert TokenType.KEYWORD in tipos
    assert TokenType.ID in tipos
    assert TokenType.STRING in tipos
    assert TokenType.NUM in tipos
    assert tipos[-1] == TokenType.EOF
    assert symbols['main']['count'] == 1
    assert symbols['printf']['count'] == 1
    assert tipo_counts[TokenType.PP_DIRECTIVE] == 1
    assert tipo_counts[TokenType.KEYWORD] == 3  # int, return, void
    assert tipo_counts[TokenType.ID] == 2       # main, printf
    assert tipo_counts[TokenType.STRING] == 1   # "Hello, world!\n"
    assert tipo_counts[TokenType.NUM] == 1      # 0
    assert tipo_counts[TokenType.EOF] == 1

def test_codigo3():
    tipos, symbols, tipo_counts = scan_and_types_and_symbols(codigo3)
    assert TokenType.KEYWORD in tipos
    assert TokenType.ID in tipos
    assert TokenType.NUM in tipos
    assert TokenType.FLOAT in tipos
    assert TokenType.CHAR in tipos
    assert tipos[-1] == TokenType.EOF
    assert symbols['main']['count'] == 1
    assert symbols['x']['count'] == 4
    assert symbols['y']['count'] == 3
    assert symbols['c']['count'] == 2
    assert tipo_counts[TokenType.KEYWORD] == 6  # int, float, char, return, int, void
    assert tipo_counts[TokenType.ID] == 10      # main, x, y, c, x, x, y, y, c, x
    assert tipo_counts[TokenType.NUM] == 3      # 42, 10, x (return x)
    assert tipo_counts[TokenType.FLOAT] == 1    # 3.14
    assert tipo_counts[TokenType.CHAR] == 2     # 'a', '\n'
    assert tipo_counts[TokenType.EOF] == 1

def test_codigo4():
    tipos, symbols, tipo_counts = scan_and_types_and_symbols(codigo4)
    assert TokenType.KEYWORD in tipos
    assert TokenType.ID in tipos
    assert TokenType.NUM in tipos
    assert TokenType.MOD in tipos
    assert TokenType.EQ in tipos
    assert TokenType.STRING in tipos
    assert tipos[-1] == TokenType.EOF
    assert symbols['main']['count'] == 1
    assert symbols['i']['count'] == 4
    assert symbols['printf']['count'] == 2
    assert tipo_counts[TokenType.KEYWORD] == 7  # int, while, if, else, return, int, void
    assert tipo_counts[TokenType.ID] == 7       # main, i, i, i, i, printf, printf
    assert tipo_counts[TokenType.NUM] == 5      # 0, 5, 2, 0, 0
    assert tipo_counts[TokenType.MOD] == 1      # %
    assert tipo_counts[TokenType.EQ] == 1       # ==
    assert tipo_counts[TokenType.STRING] == 2   # "even\n", "odd\n"
    assert tipo_counts[TokenType.EOF] == 1