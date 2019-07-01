# LFA-DSL

[Especificações do trabalho](lfa-trab-final-2019-1.pdf)

### Grupo:
- Ewerson Vieira Nascimento (ewersonv@gmail.com)
- Paulo Ricardo Viana Ferreira (paulo_ricardosf@outlook.com)
- Willian Bruschi Vaneli (willianvaneli@gmail.com)

#### Ambiente de desenvolvimento:
Programa desenvolvido em Python (3.6.7), utilizando a biblioteca [Ply](https://www.dabeaz.com/ply/), visual studio code, SO windowns.

### Descrição dos arquivos:
Parser.py:
Parsertab.py:

### Descrição da linguagem:
A DSL proposta neste trabalho tem como objetivo prover uma linguagem que permita realizar operações matemáticas aritméticos. Optamos por utilizar a linguagem Python para o desenvolvimento, pela simplicidade de criação de artefatos em geral.
A linguagem permite utilizar artefatos de nomeação de variáveis, além de construção de comandos de seleção IF e repetição WHILE. Permitindo também artefatos de abstração conhecidos como função ou procedimento, geralmente utilizados nas diversas outras linguagens de programação. 

### Justificativa uso da biblioteca Ply:
A biblioteca ply apresenta facilidade de declaração dos tokens e EBNF, onde é possível separar cada declaração e trata-la de modo exclusivo.


### Tabela com Operadores e Expressões:

Operador | Descrição
--------- | ------
=              | Atribuição. Ex.: <variável> = <conteúdo>;
==,>,<,>=,<=   | Comparadores lógicos
{ }            | Delimitadores de bloco, podem ser usados em IF,While, declaração de função ou em chamada de função;
+,-,*,/,^,//,% | Operadores aritiméticos;
    
    
Expressão | Descrição
--------- | ------
def         | Expressão que define uma função. Ex.: def <nome-do-método>(<argumentos>){ };
if          | Expressão que indica uma estrutura de seleção. Ex.: if (<condição>){<bloco>};
while       | Expressão que indica um loop. Ex.: while (<condição>){<operações>*};


### Descrição dos arquivos:

Arquivo | Descrição
--------- | ------
parser.py     | Arquivo contendo a gramática em EBNF da linguagem e demais funções desenvolvidas em python. 
pasrsertab.py    | ....

### Gramática
Gramática em EBNF

````
precedence = (
    ('left','IGUAL','MENOR','MAIOR','MENORIGUAL','MAIORIGUAL'),
    ('left','PLUS','MINUS'),
    ('left','DIVIDEINT','QUOTIENT'),
    ('left','MULTIPLY','DIVIDE'),
    ('left','EXPONENT'),
    ('left','LPAR','RPAR'),
    ('left','LCHAVES','RCHAVES')
)


    '''
    contexto    : deffuncao
                | bloco
                | empty
    '''
    bloco   : linha [ENDLINE bloco]*
    '''
    linha   : funcao
            | if
            | while
            | return
            | var_assign
            | expression
    '''
    return  : RETURN term [COMMA return]*
    '''
    funcao  : NAME LPAR values RPAR
    '''
    values  : NAME [COMMA values]*
            | NUMBER [COMMA values]*
    '''
    deffuncao   : DEF NAME LPAR args RPAR LCHAVES bloco RCHAVES
    '''
    args    : NAME [COMMA args]*
    '''
    expression  : term
    '''
    if  : IF LPAR bloco RPAR LCHAVES bloco RCHAVES
    '''
    while   : WHILE LPAR bloco RPAR LCHAVES bloco RCHAVES
    '''
    var_assign  : NAME EQUALS term
                | NAME EQUALS funcao
    '''
    term    : term EXPONENT term
            | term MULTIPLY term
            | term DIVIDE term
            | term DIVIDEINT term
            | term QUOTIENT term
            | term MINUS term
            | term PLUS term
            | term IGUAL term
            | term MENOR term
            | term MAIOR term
            | term MENORIGUAL term
            | term MAIORIGUAL term
      | fator
      | NAME
    '''
    factor  : nterm
            | NUMBER
            | positive
            | negative
    '''
    negative    : MINUS term
    '''
    positive    : PLUS term
    '''
    nterm : LPAR term RPAR
    '''
    empty   :
    '''

````

Gramática no código

````
precedence = (
    ('left','IGUAL','MENOR','MAIOR','MENORIGUAL','MAIORIGUAL'),
    ('left','PLUS','MINUS'),
    ('left','DIVIDEINT','QUOTIENT'),
    ('left','MULTIPLY','DIVIDE'),
    ('left','EXPONENT'),
    ('left','LPAR','RPAR'),
    ('left','LCHAVES','RCHAVES')
)

def p_contexto(entrada):
    '''
    contexto    : deffuncao
                | bloco
                | empty
    '''
    print(run(entrada[1]))


def p_bloco_linhas(entrada):
    '''
    bloco   : linha ENDLINE bloco
    '''
    entrada[0] = ('blocoLinhas',entrada[1],entrada[3])


def p_bloco_linha(entrada):
    '''
    bloco   : linha
    '''
    entrada[0] = entrada[1]


def p_linha(entrada):
    '''
    linha   : funcao
            | if
            | while
            | return
            | var_assign
            | expression
    '''
    entrada[0] = entrada[1]


def p_return(entrada):
    '''
    return  : RETURN term COMMA return
    '''
    entrada[0] = ('returns',entrada[2],entrada[4])

def p_return_return(entrada):
    '''
    return  : RETURN term
    '''
    entrada[0] = ('return',entrada[2])


def p_funcao(entrada):
    '''
    funcao  : NAME LPAR values RPAR
    '''
    entrada[0]= ('func',entrada[1],entrada[3])
    

def p_values_value_name(entrada):
    '''
    values  : NAME COMMA values
    '''
    entrada[0]= ('values',('var',entrada[1]),entrada[3])

def p_values_value_number(entrada):
    '''
    values  : NUMBER COMMA values
    '''
    entrada[0]= ('values',entrada[1],entrada[3])

def p_values_number(entrada):
    '''
    values  : NUMBER
    '''
    entrada[0]= ('value',entrada[1])

def p_values_name(entrada):
    '''
    values  : NAME
    '''
    entrada[0]= ('value',('var',entrada[1]))



def p_deffuncao(entrada):
    '''
    deffuncao   : DEF NAME LPAR args RPAR LCHAVES bloco RCHAVES
    '''
    entrada[0] = ('def', entrada[2],entrada[4],entrada[7])


def p_args(entrada):
    '''
    args    : NAME COMMA args
    '''
    entrada[0]= ('fcs',entrada[1],entrada[3])

def p_args_arg(entrada):
    '''
    args :   NAME
    '''
    entrada[0] = ('fc', entrada[1])


def p_expression(entrada):
    '''
    expression  : term
    '''
    entrada[0] = entrada[1]
    


def p_if(entrada):
    '''
    if  : IF LPAR bloco RPAR LCHAVES bloco RCHAVES
    '''
    entrada[0] = ('if',entrada[3],entrada[6])

def p_while(entrada):
    '''
    while   : WHILE LPAR bloco RPAR LCHAVES bloco RCHAVES
    '''
    entrada[0] = ('while',entrada[3],entrada[6])


def p_var_assign(entrada):
    '''
    var_assign  : NAME EQUALS term
                | NAME EQUALS funcao
    '''
    entrada[0] = ('=', entrada[1],entrada[3])

def p_term(entrada):
    '''
    term    : term EXPONENT term
            | term MULTIPLY term
            | term DIVIDE term
            | term DIVIDEINT term
            | term QUOTIENT term
            | term MINUS term
            | term PLUS term
            | term IGUAL term
            | term MENOR term
            | term MAIOR term
            | term MENORIGUAL term
            | term MAIORIGUAL term
    '''
    entrada[0] = (entrada[2], entrada[1], entrada[3])


def p_term_factor(entrada):
    '''
    term    : factor
    '''
    entrada[0] = entrada[1]


def p_factor(entrada):
    '''
    factor  : nterm
            | NUMBER
            | positive
            | negative
    '''
    entrada[0] = entrada[1]
    

def p_negative(entrada):
    '''
    negative    : MINUS term
    '''
    entrada[0] = - entrada[2]

def p_positive(entrada):
    '''
    positive    : PLUS term
    '''
    entrada[0] = entrada[2]


def p_nterm(entrada):
    '''
    nterm : LPAR term RPAR
    '''
    entrada[0] = entrada[2]

# Definicao de uma variavel 
def p_term_var(entrada):
    '''
    term    : NAME
    '''
    entrada[0] = ('var', entrada[1])


def p_empty(entrada):
    '''
    empty   :
    '''
    entrada[0]= entrada


````


#### Instalando o Lark:
Para poder instalar o Lark, primeiro precisamos instalar o [Pip](https://pypi.org/project/pip/).

1. Começamos atualizando a lista de pacotes:

    ``$ sudo apt update``

2. Como estamos utilizando o Python 3, instalaremos o Pip com o seguinte comando:

    ``$ sudo apt install python3-pip``

3. Para verificar se o Pip foi instalado corretamente, fazemos:

    ``$ pip3 --version``c

    Teremos como retorno algo similar a:

    ``pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)``

4. Agora, para instalar o Lark, basta fazer:

    ``$ pip3 install lark-parser``
