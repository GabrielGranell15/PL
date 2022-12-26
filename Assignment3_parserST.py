'''
PARSER with Semantics Assignment 3
@author: Gabriel A. Granell Jiménez
@date: November 8, 2022
'''

from xml.dom.pulldom import parseString
import sys
import ply.yacc as yacc
import ply.lex as lex
from ply.lex import TOKEN
#Did not import the Assignment1 lexer just in case. Lexer could be commented out and import the Assignment1_lexer.py.
#Lexer

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
    t.value=int(t.value,'Int')
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

#Build parser
'''
------------------------------------------------------------------------------------------------------------------------------------------------------
'''
start="defdefs"
ids={}
values={}
procedures={}

def p_defdefs(p):
    '''defdefs : defdef defdefs
              | defdef'''
    if len(p)==3:
        p[0]=[p[1],p[2]]
    else:
        p[0]=p[1]

def p_defdef(p):
    'defdef : DEF ID LPAREN parmsopt RPAREN COLON type BECOMES LBRACE vardefsopt defdefsopt expras RBRACE'
    ids[p[2]]=('def',p[7])
    values[(p[2])]=(p[4],p[7],p[10],p[11],p[12])
    procedures[p[2]]=(p[4],p[7])
    p[0]=(p[2],p[4],p[7],p[8],p[10],p[11],p[12])
    
def p_parmsopt(p):
    '''parmsopt : parms
                | empty'''
    p[0]=p[1]

def p_parms(p):
    '''parms : vardef COMMA parms
            | vardef'''
    if len(p)==4:
        p[0]=[p[1],p[3]]
    else:
        p[0]=p[1]

def p_vardef(p):
    'vardef : ID COLON type'
    ids[p[1]]=p[3]
    p[0]=(p[1],p[3])

def p_type(p):
    '''type : INT
            | LPAREN typesopt RPAREN ARROW type'''
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=(p[2],p[4],p[5])

def p_typesopt(p):
    '''typesopt : types
                | empty'''
    p[0]=p[1]

def p_types(p):
    '''types : type COMMA types
            | type'''
    if len(p)==4:
        p[0]=[p[1],p[3]]
    else:
        p[0]=p[1]

def p_vardefsopt(p):
    '''vardefsopt : VAR vardef SEMI vardefsopt
                  | empty'''
    if(len(p)==2):
       p[0]=p[1]
    else:
        p[0]=(p[1],p[2],p[4])

def p_defdefsopt(p):
    '''defdefsopt : defdefs
                  | empty'''
    p[0]=p[1]

def p_expras(p):
    '''expras : expra SEMI expras
              | expra'''
    if(len(p)==4):
        p[0]=[p[1],p[3]]
    else:
        p[0]=p[1]

def p_expra(p):
    '''expra : ID BECOMES expr
            | expr'''
    if(len(p)==4):
        values[p[1]]=p[3]
        p[0]=(p[1],p[2],p[3])
    else:
        p[0]=p[1]

def p_expr(p):
    '''expr : IF LPAREN test RPAREN LBRACE expras RBRACE ELSE LBRACE expras RBRACE
            | term
            | expr PLUS term
            | expr MINUS term'''
    if (len(p)==12):
        if ids[p[6]]!=ids[p[10]]:
            print("p_ expr: Error in types")
        else:
            p[0]=[p[1],[p[3]],(p[6]),p[8],(p[10])]
    elif(len(p)==2):
        p[0]=p[1]
    elif(len(p)==4):
        if ids[p[1]]!= 'Int' and ids[p[3]]!='Int':
            print("p_ expr: Error in types")
        else:
            if p[2]=='+':
                p[0]=['Int',p[1],'+',p[3]] 
            elif p[2]=='-':
                p[0]=['Int',p[1],'-',p[3]]

def p_term(p):
    '''term : factor
            | term STAR factor
            | term SLASH factor
            | term  PCT factor'''
    if(len(p)==2):
        p[0]=p[1]
    elif(len(p)==4):
        if ids[p[1]]!='Int' and ids[p[3]]!='Int':
            print("p_ term: Error in types")
        else:
            if p[2]=='*':
                p[0]=['Int',[p[1],'*',p[3]]]
            elif p[2]=='/':
                p[0]=['Int',[p[1],'/',p[3]]]
            elif p[2]=='%':
                p[0]=['Int',[p[1],'%',p[3]]]
        

def p_factor(p):
    '''factor : ID
              | NUM
              | LPAREN expr RPAREN
              | factor LPAREN argsopt RPAREN'''
    if(len(p)==2):
        p[0]=p[1]
        ids[p[0]]=ids[p[1]]
    elif(len(p)==4):
        p[0]=p[2]
    elif(len(p)==5):
        p[0]=[p[1],p[3]]

def p_test(p):
    '''test : expr NE expr
            | expr LT expr
            | expr LE expr
            | expr GE expr
            | expr GT expr
            | expr EQ expr'''
    if ids[p[1]]!='Int' and ids[p[3]]!='Int':
            print("p_ term: Error in types")
    else:
        if p[2]=='!=':
            p[0]=[p[1],'!=',p[3]]
        elif p[2]=='<':
            p[0]=[p[1],'<',p[3]]
        elif p[2]=='<=':
            p[0]=[p[1],'<=',p[3]]
        elif p[2]=='>=':
            p[0]=p[1],'>=',p[3]
        elif p[2]=='>':
            p[0]=[p[1],'>',p[3]]
        elif p[2]=='==':
            p[0]=[p[1],'==',p[3]]

def p_argsopt(p):
    '''argsopt : args
              | empty'''
    p[0]=p[1]

def p_args(p):
    '''args : expr COMMA args
            | expr'''
    if(len(p)==4):
        p[0]=[p[1],p[3]]
    else:
        p[0]=p[1]

def p_error(p):
    print("Syntax error in input: " + str(p))
    pass
 
def p_empty(p):
    'empty :'
    p[0]=None

if __name__ == "__main__":
     
    parser = yacc.yacc()
    # textfile = open("Test1.txt", 'r', errors='ignore').read()
    # textfile = input()
    # print(parser.parse(textfile))
    file=open(sys.argv[1],'r')
    fileLines=file.read()
    parser = yacc.yacc()
    result=parser.parse(fileLines)
    print(fileLines)
    print('\n')
    print('Variables and types:')
    for key, value in ids.items():
            print(key, ' : ', value)
    print('\n')
    print('Variables(or def with parameters) and values:')
    for key, value in values.items():
            print(key, ' : ', value)
    print('\n')
    for key, value in procedures.items():
            print(key, ' : ', value)
    last_key=procedures[list(procedures.keys())[-1]]
    lk=str(last_key)
    if lk.count('Int')<3:
        print('Main procedure must be (Int,Int)=>Int.Please revise your main procedures parameters.')
    print('\n')
    print(result)