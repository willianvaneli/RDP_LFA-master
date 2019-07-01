import ply.yacc as yacc
import ply.lex as lex
from ply import *
import sys


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
    'DEF',
    'IF',
    'WHILE',
    'IGUAL',
    'MENOR',
    'MAIOR',
    'MENORIGUAL',
    'MAIORIGUAL',
    'RETURN'
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
t_COMMA = r'\,'
t_ENDLINE = r'\;'
t_IGUAL = r'\=\='
t_MENOR = r'\<'
t_MAIOR = r'\>'
t_MENORIGUAL = r'\<\='
t_MAIORIGUAL = r'\>\='

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

def t_IF(tokens):
    r'if'
    tokens.type = 'IF'
    return tokens
    

def t_WHILE(tokens):
    r'while'
    tokens.type = 'WHILE'
    return tokens

def t_RETURN(tokens):
    r'return'
    tokens.type = 'RETURN'
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

#def p_linha(entrada):
#    '''
#    linha   : expression ENDLINE
#    '''
#    entrada[0] = entrada[1]
 
# Definicao de como passar um valor para uma variavel 
def p_var_assign(entrada):
    '''
    var_assign  : NAME EQUALS term
                | NAME EQUALS funcao
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

#def p_error(entrada):
#    print("Syntax error found!" + entrada.value)

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
                resultado = run(entrada[2])
                env[entrada[1]] = resultado
                return resultado
            else:
                env[contexto+entrada[1]] = run(entrada[2])
                return entrada[2]
        elif entrada[0] == '==':
            return run(entrada[1]) == run(entrada[2])
        elif entrada[0] == '>':
            return run(entrada[1]) > run(entrada[2])
        elif entrada[0] == '>=':
            return run(entrada[1]) >= run(entrada[2])
        elif entrada[0] == '<':
            return run(entrada[1]) < run(entrada[2])
        elif entrada[0] == '<=':
            return run(entrada[1]) <= run(entrada[2])
        elif entrada[0] == 'if':
            if (run(entrada[1])):
                print ('executa if')
                return run(entrada[2])
            else:
                print ('não executa if')
        elif entrada[0] == 'while':
            while (run(entrada[1])):
                run(entrada[2])
        elif entrada[0] == 'var':
            if contexto+entrada[1] in env:
                return env[contexto+entrada[1]]
            elif entrada[1] in env:
                return env[entrada[1]]
            else:
                print ('Undeclared variable found! -> ' + entrada[1])
                return None
        elif entrada[0] == 'def':
            env['func'+entrada[1]] = []
            # para variaveis
            env['func'+entrada[1]].append([])
            # para bloco
            env['func'+entrada[1]].append([])
            # para valores
            env['func'+entrada[1]].append([])
            # para retorno
            env['func'+entrada[1]].append([]) 
            env['func'+entrada[1]][1].append(entrada[3])
            contexto = entrada[1]
            print("vai rodar as variaveis")
            run(entrada[2])
            contexto=''
        elif entrada[0] == 'fcs':
            env['func'+contexto][0].append(entrada[1])
            run(entrada[2])
        elif entrada[0] == 'fc':
            env['func'+contexto][0].append(entrada[1])
        elif entrada[0] == 'func':
            contexto = entrada[1]
            run(entrada[2])
            rodaFuncao("func"+contexto)
            env["func"+contexto][2]=[]
            limpaVarFun("func"+contexto)
            #retornando resultados da função
            listaResultados = []
            # caso um resultado
            if (len(env["func"+contexto][3])==0):
                print("funcao sem retorno")
                contexto=''
                return None
            if (len(env["func"+contexto][3]) == 1 ):
                resultado = run(env["func"+contexto][3])
                contexto=''
                return resultado
            #caso vários resultados
            else:
                for  i in env["func"+contexto][3] :
                    listaResultados.append(run(i))
                contexto=''
                return listaResultados
        elif entrada[0] == 'value':
            env['func'+contexto][2].append(run(entrada[1]))
        elif entrada[0] == 'values':
            env['func'+contexto][2].append(run(entrada[1]))
            run(entrada[2])
        elif entrada[0] == 'blocoLinhas':
            run(entrada[1])
            run(entrada[2])
        elif entrada[0] == 'return':
            env['func'+contexto][3].append(run(entrada[1]))
        elif entrada[0] == 'returns':
            env['func'+contexto][3].append(run(entrada[1]))
            run(entrada[2])
    else:
        return entrada


def rodaFuncao (fun):
    if len(env[fun][0]) != len(env[fun][2]):
        print ("Entrada da funcao nao compativel com os parametros de entrada")
    else:
        i = 0
        while (i < len(env[fun][2])) :
            env[contexto+env[fun][0][i]] = env[fun][2][i]          
            #print(str(contexto+env[fun][0][i]) + " com o  valor " + str(env[fun][2][i]))
            i+=1
        #print ( run(env[fun][1][0]) )
    
    return run(env[fun][1][0])


def limpaVarFun(fun):
    i = 0
    #lst = []
    while (i < len(env[fun][0])) :
        env.pop(contexto+env[fun][0][i])
        i+=1
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