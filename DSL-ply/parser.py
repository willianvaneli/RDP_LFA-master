import ply.yacc as yacc
import ply.lex as lex
from ply import *
import sys

keywords = (
    'LET', 'READ', 'DATA', 'PRINT', 'GOTO', 'IF', 'THEN', 'FOR', 'NEXT', 'TO', 'STEP',
    'END', 'STOP', 'DEF', 'GOSUB', 'DIM', 'REM', 'RETURN', 'RUN', 'LIST', 'NEW',
)

'''
Definicao o conjunto dos tokens
'''

tokens = [
    'NUMBER',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'DIVIDEINT',
    'QUOTIENT',
    'EXPONENT',
    'LPAR',
    'RPAR',
    'EQUALS',
    'NAME',
    'LCHAVES',
    'RCHAVES',
    'COMMA',
    'ENDLINE',
    'DEF'
]

# Definindo os tokens onde tokens = conjunto

t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVIDE = r'\/'
t_MULTIPLY = r'\*'
t_EQUALS = r'\='
t_DIVIDEINT = r'\/\/'
t_QUOTIENT = r'\%'
t_EXPONENT = r'\^'
t_LPAR = r'\('
t_RPAR = r'\)'
t_LCHAVES = r'\{'
t_RCHAVES = r'\}'
#t_DEF = r'def'
t_COMMA = r'\,'
t_ENDLINE = r'\;'

# Ignorando espacos em branco
t_ignore = r' '


# Definindo um numero 
def t_NUMBER(tokens):
    r'\d+\.?\d*([Ee][+-]?\d+)?'
    tokens.value = float(tokens.value)
    return tokens

def t_DEF(tokens):
    r'def'
    tokens.type = 'DEF'
    return tokens


# Definindo name para variaveis, exige uma letra e pode ser seguido por letras ou numeros 
def t_NAME(tokens):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    tokens.type = 'NAME'
    return tokens

def t_error(tokens):
    print("Não pode ser processado, verifique a entrada")
    tokens.lexer.skip(1)

lexer = lex.lex()

env = {}
contexto = ''

# Definindo as precedencias
precedence = (
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
                | funcao
                | expression
    '''
    print(run(entrada[1]))


def p_funcao(entrada):
    '''
    funcao  : NAME LPAR values RPAR
    '''
    print("funcao")
    entrada[0]= ('func',entrada[1],entrada[3])
    

def p_values(entrada):
    '''
    values  : NUMBER
            | NAME
    '''
    print("valor")
    entrada[0]= ('value',entrada[1])


def p_value(entrada):
    '''
    values  : NAME COMMA values
    '''
    entrada[0]= ('values',entrada[1],entrada[3])

def p_deffuncao(entrada):
    '''
    deffuncao   : DEF NAME LPAR args RPAR bloco
    '''
    entrada[0] = ('def', entrada[2],entrada[4],entrada[6])


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
                | var_assign
                | empty
    '''
    entrada[0] = entrada[1]
    

def p_bloco(entrada):
    '''
    bloco   : LCHAVES expression RCHAVES
    '''
    entrada[0] = entrada[2]


#def p_linha(entrada):
#    '''
#    linha   : expression ENDLINE
#    '''
#    entrada[0] = entrada[1]
 
# Definicao de como passar um valor para uma variavel 
def p_var_assign(entrada):
    '''
    var_assign  : NAME EQUALS term
    '''
    entrada[0] = ('=', entrada[1],entrada[3])

# Definicao de expressao exige que a maior hierarquia apareca primeiro
def p_term(entrada):
    '''
    term    : term EXPONENT term
            | term MULTIPLY term
            | term DIVIDE term
            | term DIVIDEINT term
            | term QUOTIENT term
            | term MINUS term
            | term PLUS term
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

def p_error(entrada):
    print("Syntax error found!" + entrada.value)

def p_empty(entrada):
    '''
    empty   :
    '''
    entrada[0]= entrada

parser = yacc.yacc()
# env é um dicionário que contém as variáveis. Este dicionário é global.

# Executando a string de entrada
def run(entrada):
    global env
    global contexto
    if type(entrada) == tuple:
        if entrada[0] == '+':
            return run(entrada[1]) + run(entrada[2])
        elif entrada[0] == '-':
            return run(entrada[1]) - run(entrada[2])
        elif entrada[0] == '*':
            return run(entrada[1]) * run(entrada[2])
        elif entrada[0] == '/':
            return run(entrada[1]) / run(entrada[2])
        elif entrada[0] == '//':
            return run(entrada[1]) // run(entrada[2])
        elif entrada[0] == '%':
            return run(entrada[1]) % run(entrada[2])
        elif entrada[0] == '^':
            return run(entrada[1]) ** run(entrada[2])
        elif entrada[0] == '=':
            if (contexto == ''):
                env[entrada[1]] = run(entrada[2])
            else:
                env[contexto+entrada[1]] = run(entrada[2])
        elif entrada[0] == 'var':
            if entrada[1] in env:
                return env[entrada[1]]
            elif contexto+entrada[1] in env:
                return env[contexto+entrada[1]]
            else:
                return 'Undeclared variable found!'
        elif entrada[0] == 'def':
            print(entrada[1])
            env['func'+entrada[1]] = []
            env['func'+entrada[1]].append([])
            env['func'+entrada[1]].append([])
            env['func'+entrada[1]].append([])
            env['func'+entrada[1]][1].append(entrada[3])
            contexto = entrada[1]
            run(entrada[2])
            contexto=''
            print('declarando funcao')
        elif entrada[0] == 'fcs':
            env['func'+contexto][0].append(entrada[1])
            run(entrada[2])
        elif entrada[0] == 'fc':
            env['func'+contexto][0].append(entrada[1])
        elif entrada[0] == 'func':
            contexto = entrada[1]
            run(entrada[2])
            rodaFuncao("func"+contexto)
            print('salvou a funcao')
        elif entrada[0] == 'value':
            env['func'+contexto][2].append(entrada[1])
        elif entrada[0] == 'values':
            env['func'+contexto][2].append(entrada[1])
            run(entrada[2])
            print('teoricamente rodaria a funcao')
    else:
        return entrada


def rodaFuncao (fun):
    if len(env[fun][0]) != len(env[fun][2]):
        print ("Entrada da funcao nao compativel com os parametros de entrada")
    else:
        print("roda funcao")
        print("funcao - " + fun)
        print("Variaveis - ")
        for i in env[fun][0]:
            print(i+"\n")
        print ("Contexto - ")
        i = 0
        while (i < len(env[fun][1])) :
            print (i)
            print("\n")
            env[contexto+env[fun][0][i]] = env[fun][2][i]
            #env[fun][2][i] = 0
            i+=1
        print ("valores atuais - \n")
        for k in env[fun][2]:
            print (k)
            print("\n")
        print ( run(env[fun][2]) )
    
    return 0




while True:
    s = input('>> ')
    if s == 'exit':
        break
    try:
        lexer.input(s)
        while True:
            tok = lexer.token()
            if not tok:
                break           
    except EOFError:
        break
    parser.parse(s)