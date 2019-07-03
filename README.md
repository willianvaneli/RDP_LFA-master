# LFA-DSL

[Especificações do trabalho](lfa-trab-final-2019-1.pdf)

## Grupo:
- Ewerson Vieira Nascimento (ewersonv@gmail.com)
- Paulo Ricardo Viana Ferreira (paulo_ricardosf@outlook.com)
- Willian Bruschi Vaneli (willianvaneli@gmail.com)

## Ambiente de desenvolvimento:
- Programa desenvolvido em Python (3.6.7) 
- Biblioteca [Ply](https://www.dabeaz.com/ply/)
- Visual studio code
- Windows

## Introdução:
A DSL proposta neste trabalho tem como objetivo prover uma linguagem que permita realizar operações matemáticas aritméticas. Optamos por utilizar a linguagem Python para o desenvolvimento pela facilidade que os integrantes do grupo possuem com a mesma.
A linguagem permite utilizar artefatos de nomeação de variáveis, além de construção de comandos de seleção IF e repetição WHILE. Permitindo também artefatos de abstração conhecidos como função ou procedimento, utilizados nas diversas outras linguagens de programação.

## Definição da DSL
### Gramática
Gramática em EBNF

```
contexto    ::= deffuncao
            | bloco
            | empty

bloco       ::= linha [ENDLINE bloco]*

linha       ::= funcao
            | if
            | while
            | return
            | var_assign
            | expression

return      ::= RETURN term [COMMA return]*

funcao      ::= NAME LPAR values RPAR

values      ::= NAME [COMMA values]*
            | NUMBER [COMMA values]*

deffuncao   ::= DEF NAME LPAR args RPAR LCHAVES bloco RCHAVES

args        ::= NAME [COMMA args]*

expression  ::= term

if          ::= IF LPAR bloco RPAR LCHAVES bloco RCHAVES

while       ::= WHILE LPAR bloco RPAR LCHAVES bloco RCHAVES

var_assign  ::= NAME EQUALS term
            | NAME EQUALS funcao

term        ::= term EXPONENT term
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
            | term IGUAL funcao
            | term MENOR funcao
            | term MAIOR funcao
            | term MENORIGUAL funcao
            | term MAIORIGUAL funcao
            | fator
            | NAME

factor      ::= nterm
            | NUMBER
            | positive
            | negative

negative    ::= MINUS term

positive    ::= PLUS term

nterm       ::= LPAR term RPAR

empty       ::=
```

### Gramática no código

````python
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

### Diagrama de sintaxe
![Alt Text](https://github.com/willianvaneli/RDP_LFA-master/blob/master/img/args.png)
![Alt Text](https://github.com/willianvaneli/RDP_LFA-master/blob/master/img/bloco.png)
![Alt Text](https://github.com/willianvaneli/RDP_LFA-master/blob/master/img/return.png)

![Alt Text](https://github.com/willianvaneli/RDP_LFA-master/blob/master/img/linha.png)
![Alt Text](https://github.com/willianvaneli/RDP_LFA-master/blob/master/img/values.png)
![Alt Text](https://github.com/willianvaneli/RDP_LFA-master/blob/master/img/funcao.png)

![Alt Text](https://github.com/willianvaneli/RDP_LFA-master/blob/master/img/contexto.png)
![Alt Text](https://github.com/willianvaneli/RDP_LFA-master/blob/master/img/deffuncao.png)
![Alt Text](https://github.com/willianvaneli/RDP_LFA-master/blob/master/img/empty.png)
![Alt Text](https://github.com/willianvaneli/RDP_LFA-master/blob/master/img/expression.png)
![Alt Text](https://github.com/willianvaneli/RDP_LFA-master/blob/master/img/factor.png)
![Alt Text](https://github.com/willianvaneli/RDP_LFA-master/blob/master/img/negative.png)

![Alt Text](https://github.com/willianvaneli/RDP_LFA-master/blob/master/img/ntermn.png)
![Alt Text](https://github.com/willianvaneli/RDP_LFA-master/blob/master/img/positive.png)

![Alt Text](https://github.com/willianvaneli/RDP_LFA-master/blob/master/img/term.png)

![Alt Text](https://github.com/willianvaneli/RDP_LFA-master/blob/master/img/var_assign.png)
![Alt Text](https://github.com/willianvaneli/RDP_LFA-master/blob/master/img/while.png)
![Alt Text](https://github.com/willianvaneli/RDP_LFA-master/blob/master/img/if.png)

### Exemplos de código

Nomeação de variaveis<br>
a = 2<br>
a = b = c = 2<br>
c = b // a<br>
a = b = z = pow(2,6)<br>
lstResults = calc(a,b,c)<br>


Estrutura de seleção<br>
if(a>b){b = b + c; a = a / c; pow(2,6)}<br>
if(a<b){while(a<b){a=a+1;a=a+1}}<br>


Estrutura de repetição<br>
while(a<=40){a=a+1}<br>
while(a<100){if(a==20){a = pow(a,2)};a = a + 1}<br>



Declaração de função<br>
def funcao2(a,b,c){if(a>b){b = b + c; a = a / c}; return a, return b}<br>
lstResults = funcao2(a,b,c)<br>
def pow(a,b){a = a ^ b; return a}<br>
while(a<100){a = pow(a,b)}<br>

## Definição da AST
~ dividir o código em classes para fazer o diagrama de classes ~



## Justificativa uso da biblioteca Ply:
A biblioteca Ply apresenta facilidade de declaração dos tokens e EBNF, onde é possível separar cada declaração e trata-la de modo exclusivo.


## Tabela com Operadores e Expressões:

Operador | Descrição
--------- | ------
=              | Atribuição. Ex.: <variável> = <conteúdo>;
==,>,<,>=,<=   | Comparadores lógicos
{ }            | Delimitadores de bloco, podem ser usados em IF, While, declaração de função ou em chamada de função;
+,-,*,/,^,//,% | Operadores aritiméticos;
    
    
Expressão | Descrição
--------- | ------
def         | Expressão que define uma função. Ex.: def <nome-do-método>(<argumentos>){ };
if          | Expressão que indica uma estrutura de seleção. Ex.: if (<condição>){<bloco>};
while       | Expressão que indica um loop. Ex.: while (<condição>){<operações>*};

## Estrutura da aplicação

```
trabalho-final-lfa-DHM
|_ DSL-ply
  |_ ply (pasta da biblioteca ply)
  |_parser.out
  |_parser.py
  |_parsertab.py
|_ Testes
  |_ 
|_ Readme.md
|_ relatório.pdf
```

### Descrição dos arquivos:

Arquivo | Descrição
--------- | ------
[parser.py](DSL-ply/parser.py)    | Arquivo contendo a gramática em EBNF da linguagem e demais funções desenvolvidas em python. 
[pasrsetab.py](DSL-ply/parsetab.py)    | Arquivo gerado automaticamente pelo Ply contendo informações de execução do parser.
[parser.out](DSL-ply/parser.out) | Arquivo gerado pelo Ply contendo informações sobre a gramática e os estados do parser.


#### Para a execução do parser é necessário instalar o python e a biblioteca ply.  

## Instalando python.  

### _Windows_  
Acessar o site oficial do [python](https://www.python.org/downloads/) realizar o download,  
Antes de iniciar a instalação selecione a opção de configurar o path, avance e aguarde o fim da instalação.  

### _Ubuntu_  
#### _Passo 1 - Pré requisitos_

Execute na linha de comando:

``$ sudo apt-get install build-essential checkinstall``

``$ sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev \ libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev``

#### _Passo 2 - Download do python 3.7_

Execute na linha de comando:

``$ cd /usr/src``

``$ sudo wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz``

Agora extraia o pacote com o comando:

``$ sudo tar xzf Python-3.7.3.tgz``

#### _Passo 3 instale o python_

Execute na linha de comando:
``$ cd Python-3.7.3``

``$ sudo ./configure --enable-optimizations``

``$ sudo make altinstall``

#### _Passo 4 cheque a instalação do python_  

Execute na linha de comando:  

``$ python3 --version``

Caso retorne ``Python-3.7.3`` a instalação foi realizada com sucesso.


## _Instalando biblioteca ply_  

Após fazer o download no [site](http://www.dabeaz.com/ply/) basta extrair o conteudo do arquivo compactado e acessar a pasta ply-3.11, onde está localizado o arquivo ``setup.py`` por linha de comando e executar o seguinte comando:

``$ python setup.py install``

dependendo do SO pode ser que seja necessário usar

``$ python3 setup.py install``
