# LFA-DSL

[Especificações do trabalho](lfa-trab-final-2019-1.pdf)

### Grupo:
- Ewerson Vieira Nascimento (ewersonv@gmail.com)
- Paulo Ricardo Viana Ferreira (paulo_ricardosf@outlook.com)
- Willian Bruschi Vaneli (willianvaneli@gmail.com)

#### Ambiente de desenvolvimento:
Programa desenvolvido em Python (3.6.7), utilizando a biblioteca [Ply](https://www.dabeaz.com/ply/), Ubuntu 18.04 e PyCharm 2019.1.3 (Community Edition).

### Descrição dos arquivos:
Parser.py: 
Parsertab.py: 

### Descrição da linguagem:
A DSL proposta neste trabalho tem como objetivo prover uma linguagem que permita realizar operações matemáticas aritméticos. Optamos por utilizar a linguagem Python para o desenvolvimento, pela simplicidade de criação de artefatos em geral.
A linguagem permite utilizar artefatos de nomeação de variáveis, além de construção de comandos de seleção IF e repetição WHILE. Permitindo também artefatos de abstração conhecidos como função ou procedimento, geralmente utilizados nas diversas outras linguagens de programação. 

### Justificativa uso da biblioteca Ply:



### Tabela com Operadores e Expressões:

Operador | Descrição
--------- | ------
=     | Atribuição. Ex.: <variável> = <conteúdo>;
" "    | String. Ex.: “<caracteres>”;
{ }    | Área que pertence a um método ou expressão. Ex.: <método>{<operações>} ou <expressão>{<operações>};
+,-,*,/,^ | Operadores aritiméticos;
    
    
Expressão | Descrição
--------- | ------
def     | Expressão que define um método. Ex.: def <nome-do-método>(<argumentos>){ };
if    | Expressão que indica uma bifurcação exclusiva. Ex.: if (<variável-de-origem>, <variável-de-destino>) (<string>){<operações>};
while   | Expressão que indica um loop. Ex.: while (<variável-de-origem>, <variável-de-destino>) (<string>){<operações>*};


### Descrição dos arquivos:

Arquivo | Descrição
--------- | ------
parser.py     | Arquivo contendo a gramática em EBNF da linguagem e demais funções desenvolvidas em python. 
pasrsertab.py    | ....

### Gramática
````
        def p_contexto(entrada):
            '''
            contexto    : deffuncao
                        | bloco
            '''
            print(run(entrada[1]))

        def p_bloco(entrada):
            '''
            bloco   : funcao
                    | if
                    | while
                    | var_assign
                    | expression
            '''
            entrada[0] = entrada[1]

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
                        | empty
            '''
            entrada[0] = entrada[1]



        def p_if(entrada):
            '''
            if  : IF LPAR bloco RPAR LCHAVES bloco RCHAVES
            '''
            print("entrou if")
            entrada[0] = ('if',entrada[3],entrada[6])

        def p_while(entrada):
            '''
            while   : WHILE LPAR bloco RPAR LCHAVES bloco RCHAVES
            '''
            print("entrou while")
            entrada[0] = ('while',entrada[3],entrada[6])

        #def p_linha(entrada):
            '''
            linha   : expression ENDLINE
            '''
            entrada[0] = entrada[1]
        Definicao de como passar um valor para uma variavel 
        def p_var_assign(entrada):
            '''
            var_assign  : NAME EQUALS term
            '''
            entrada[0] = ('=', entrada[1],entrada[3])

        Definicao de expressao exige que a maior hierarquia apareca primeiro
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

        Definicao de uma variavel 
        def p_term_var(entrada):
            '''
            term    : NAME
            '''
            entrada[0] = ('var', entrada[1])

        def p_error(entrada):
            print("Syntax error found!" + entrada.value)

        def p_empty(entrada):
            '''
            empty   :
            '''
            entrada[0]= entrada

        parser = yacc.yacc()
        env é um dicionário que contém as variáveis. Este dicionário é global.
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
