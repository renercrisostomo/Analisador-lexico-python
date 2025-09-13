# Trabalho Prático – Implementação Manual de um Analisador Léxico

Desenvolver em Python um analisador léxico manual (sem uso de geradores automáticos como Lex, Flex, PLY ou ANTLR) para uma linguagem semelhante a C. O analisador deve receber como entrada um código-fonte e produzir como saída:

- A lista de tokens reconhecidos (tipo, lexema e atributo quando existir).
- A tabela de símbolos, contendo todos os identificadores encontrados e a quantidade de ocorrências.

## Funcionalidades obrigatórias

1. **Identificadores e palavras-chave**

- Identificadores: `[A-Za-z_][A-Za-z0-9_]*`.
- Palavras-chave: mínimo de 20 reservadas de C (`int`, `float`, `char`, `if`, `else`, `while`, `return`, etc.).
- Palavras-chave não entram na tabela de símbolos.

2. **Literais**

- Inteiros: decimal.
- Reais (float): com ponto decimal (3.14).
- Caractere: `'a'`, `'\n'`.
- String: `"texto\n"`.

3. **Operadores e delimitadores**

- Aritméticos: `+`, `-`, `*`, `/`, `%`.
- Relacionais: `==`, `!=`, `<`, `<=`, `>`, `>=`.
- Lógicos: `&&`, `||`, `!`.
- Atribuição: `=`, `+=`, `-=`, `*=`, `/=`, etc.
- Outros: `;`, `,`, `.`, `(`, `)`, `{`, `}`, `[`, `]`, `->`, `...`.

4. **Comentários**

- Linha: `// comentário até o fim da linha`.
- Bloco: `/* comentário até fechar */`.
- Comentários devem ser ignorados.

5. **Diretivas de pré-processador**

- Linhas que começam com `#` devem ser reconhecidas como token especial `PP_DIRECTIVE`.

6. **Tabela de símbolos**

- Estrutura (ex.: `dict`) para armazenar identificadores e número de ocorrências.

## Tratamento de erros léxicos

O analisador deve gerar um token `ERROR` quando encontrar sequências inválidas, como:

- String não terminada (`"abc...`).
- Uso incorreto de vírgula como separador decimal (`3,14`).
- Nome de variáveis que começam com números.

## Entrada

Um arquivo ou string contendo código-fonte em linguagem C-like.

## Saída esperada

1. Lista de tokens (na ordem em que aparecem).
2. Tabela de símbolos com identificadores e número de ocorrências.

## Avaliação

- Reconhecimento de tokens.
- Tabela de símbolos.
- Tratamento de erros léxicos.
- Qualidade do código.

## Entrega

- **Identificação**: No início do vídeo, deve constar o nome do(s) aluno(s) envolvido(s).
- **Formato da entrega**: A entrega consistirá em um vídeo de apresentação do trabalho, contendo:
  - Explicação completa do funcionamento do código desenvolvido.
  - Apresentação dos fundamentos teóricos relacionados.
  - Demonstração da execução do programa com os exemplos indicados.
- **Duração**: O vídeo deve ter cerca de 10 minutos.
- **Publicação**: O vídeo deve ser publicado no YouTube e o link disponibilizado no Classroom.
- **Código-fonte**: Além do vídeo, é obrigatório enviar o código-fonte utilizado.
- **Prazo de entrega**: Até o dia 12/09.
- **Forma de realização**: O trabalho pode ser feito individualmente ou em dupla.

## Nota

- Vale 5 pontos na N1.

## Exemplo de código de entradas

```c
#include <stdio.h>

int main(void) {
   printf("Hello, world!\n");
   return 0;
}
```

```c
int main(void) {
   int x = 42;
   float y = 3.14;
   char c = 'a';

   x = x + 10;
   y = y * 2;
   c = '\n';

   return x;
}
```

```c
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
```