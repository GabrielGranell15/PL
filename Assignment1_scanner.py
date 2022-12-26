'''
LEXER Assignment 1
@author: Gabriel A. Granell Jiménez
@date: September 1, 2022
'''
import ply.lex as lex
from ply.lex import TOKEN
import sys

# Base tokens
tokens = [
    'ID',
    'DELIMITERS',
    'OPERATORS',
    'NUM'
]

# Reserved words or variables
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'var': 'VAR',
    'def': 'DEF',
    'Int': 'INT'
}
# Tokens to be assigned.
unrelatedTokens = [
    'GE',
    'NE',
    'LE',
    'DUALOPERATORS',
    'MINUS',
    'LBRACE',
    'RPAREN',
    'LPAREN',
    'RBRACE',
    'COMMA',
    'SEMI',
    'COLON',
    'RESERVED',
    'ARROW',
    'EQ'
]

# Operators and their token values
operator_2 = {'+': 'PLUS',
              '-': 'MINUS',
              '*': 'STAR',
              '/': 'SLASH',
              '=': 'BECOMES',
              '<': 'LT',
              '>': 'GT',
              '%': 'PCT',
              }

#List of tokens
tokens += list(reserved.values()) + unrelatedTokens + list(operator_2.values())

#Ignores
t_ignore = ' \t'

def t_ignore_COMMENT(t):
    r'\/\/.*'
    pass

#Token definitions
def t_RESERVED(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type=reserved.get(t.value,'ID')#Getting ID
    return t

def t_NUM(t):
    r'\d+'
    t.value=int(t.value)
    return t

def t_DELIMITERS(t):
    r'\( | \) | \{ | \} | \, | \; | \:'
    if t.value == '(':
        t.type = 'LPAREN'
    elif t.value == ')':
        t.type = 'RPAREN'
    elif t.value == '{':
        t.type = 'LBRACE'
    elif t.value == '}':
        t.type = 'RBRACE'
    elif t.value == ',':
        t.type = 'COMMA'
    elif t.value == ';':
        t.type = 'SEMI'
    elif t.value == ':':
        t.type='COLON'
    return t

def t_DUALOPERATORS(t):
    r'\<\= | \>\= | \!\= | \=\= | \=\>'
    if t.value == '>=':
        t.type = 'GE'
    elif t.value == '!=':
        t.type = 'NE'
    elif t.value == '<=':
        t.type = 'LE'
    elif t.value == '==':
        t.type='EQ'
    elif t.value == '=>':
        t.type='ARROW'
    return t

def t_OPERATORS(t):
    r'\+ | \- | \* | \/ | \= | \< | \> |%'
    if t.value == '-':
        t.type = 'MINUS'
    if t.value in operator_2:
        t.type = operator_2[t.value]
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#Build lexer
lexer = lex.lex()

'''
#Test
data="""def f(a:Int, b:Int):Int = { var c:Int;
        def g(a:Int, b:(Int)=>Int):Int = { b(a)
        }def h(c:Int):Int = {
        def g():Int = { c-b
        }
        g() }
        c = a+b;
        g(c,h) }"""

lexer.input(data)

while True:
    tok=lexer.token()
    if not tok:
        break
    print(tok)
    '''

#Write "python Assignment1_scanner.py Test_program.rtf" or any .txt or .rtf file on terminal to run lexer or uncomment Test and change input to "data". Afterwards, comment the file reader to test lexer.

#File read: 

fileName=sys.argv[1]
file=open(fileName,"r")
fileStr=""

for line in file:
    fileStr+=line

file.close()

lexer.input(fileStr)

#Print rows and tokens in a ordered.
row=0
while True:
    tok=lexer.token()

    if not tok:
        break

    if row!=int(tok.lineno):
        row=int(tok.lineno)
        print("\nRow:"+str(row)+"\n")

    print(tok)