'''
PARSER with SCALA Semantics Addition Assignment 4
Initializer function was implemented separating vardef into 2 functions: parmvardef and vardef
Use '_' for default value. Default value is 0.
Updated parser syntax from Assignment 3 due to have submitted it before date extension.E
@author: Gabriel A. Granell Jiménez
@date: November 29, 2022
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
    'NUM'
]

# Reserved words or variables
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'var': 'VAR',
    'def': 'DEF',
    'Int': 'INT',
    '_':'DEFAULT' #This is based on Scala's syntax.
}
# Tokens to be assigned.
unrelatedTokens = [
    'GE',
    'NE',
    'LE',
    'LBRACE',
    'RPAREN',
    'LPAREN',
    'RBRACE',
    'COMMA',
    'SEMI',
    'COLON',
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
    t.value = int(t.value)
    t.type='NUM'
    return t

def t_DEFAULT(t):
    r'_'
    t.type='DEFAULT'
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
exprs={}
expraslist={}#Used for expras tpye revision

def p_defdefs(p):
    '''defdefs : defdef defdefs
              | defdef'''
    if len(p)==3:
        p[0]=p[1],p[2]
    else:
        p[0]=p[1]

def p_defdef(p):
    'defdef : DEF ID LPAREN parmsopt RPAREN COLON type BECOMES LBRACE vardefsopt defdefsopt expras RBRACE'

    ids[p[2]]={'type':p[7],'defdef':'true','value':p[12]}
    if len(expraslist)!=0:
        if expraslist[p[12]]!='None':
            if ids[p[2]]['type']!=expraslist[p[12]]:#Problem with first function when figuring out expras type
                print("Error: Type mismatch in function definition. May be produced by empty function or first function when parser is reading. If so, ignore error.")
    values[(p[2])]=(p[4],p[7],p[10],p[11],p[12])
    procedures[p[2]]=(p[4],p[7])
    p[0]=p[2],p[4],p[7],p[8],p[10],p[11],p[12]
    

def p_parmsopt(p):
    '''parmsopt : parms
                | empty'''
    p[0]=p[1]

def p_parms(p): #Miny modification to be able to not have to manage same rule for normal variables.
    '''parms : parmvardef COMMA parms
            | parmvardef'''
    if len(p)==4:
        p[0]=p[1],p[3]
    else:
        p[0]=p[1]

def p_parmvardef(p):
    'parmvardef : ID COLON type'
    ids[p[1]]={'type':p[3],'defdef':'false','value':'None'}
    exprs[p[1]]=p[3]
    p[0]=(p[1],p[3])
    
def p_type(p):
    '''type : INT
            | LPAREN typesopt RPAREN ARROW type'''
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[5]

def p_typesopt(p):
    '''typesopt : types
                | empty'''
    p[0]=p[1]

def p_types(p):
    '''types : type COMMA types
            | type'''
    if len(p)==4:
        p[0]=p[1],p[3]
    else:
        p[0]=p[1]

def p_vardefsopt(p):
    '''vardefsopt : VAR vardef SEMI vardefsopt
                  | empty'''
    if(len(p)==2):
       p[0]=p[1]
    else:
        p[0]=p[1],p[2],p[4]

def p_vardef(p):#Modified to be able to manage variables individually from parameter variables.
    '''vardef : ID BECOMES expr 
            | ID COLON type BECOMES expr
            | ID COLON type'''
    if len(p)<=3:
        print("Error in initialization of variable ")
    elif len(p)==4:
        if p[2]=='=':
            ids[p[1]]={'type':exprs[p[3]],'defdef':'false','value':p[3]}#Infering type from expr
            exprs[p[1]]=p[3]
            p[0]=(p[1],'=',p[3]) 
        else:
            ids[p[1]]={'type':p[3],'defdef':'false','value':'None'} #Maintaining the original languages syntax.
            exprs[p[1]]=p[3]
            p[0]=(p[1],p[3]) 
    elif len(p)==6:
        ids[p[1]]={'type':p[3],'defdef':'false','value':p[5]} #Taking into consideration Scala syntax
        exprs[p[1]]=p[3]
        p[0]=(p[1],p[3],'=',p[5])
      

def p_defdefsopt(p):
    '''defdefsopt : defdefs
                  | empty'''
    p[0]=p[1]

def p_expras(p):
    '''expras : expra SEMI expras
              | expra'''    
    if len(p)==4:
        p[0]=p[1],p[3]
        expraslist[p[0]]=expraslist[p[1]]
    elif len(p)==2:
        p[0]=p[1]
        if p[0]==None:
            expraslist[p[0]]='None'
        else:
            expraslist[p[0]]=expraslist[p[1]]

def p_expra(p):
    '''expra : ID BECOMES expr
            | expr'''
    if(len(p)==4):
      if ids[p[1]]['defdef']=='false':#Not denote a procedure
        ids[p[1]]['value']=p[3]
        p[0]=p[1],p[2],p[3]
        expraslist[p[0]]=exprs[p[1]]
    else:
        p[0]=p[1]
        

def p_expr(p):
    '''expr : IF LPAREN test RPAREN LBRACE expras RBRACE ELSE LBRACE expras RBRACE
            | term
            | expr PLUS term
            | expr MINUS term'''
    if (len(p)==12):
        if exprs[p[6]]!=exprs[p[10]]:
            print("Error: Type mismatch in expression.")
        p[0]=p[3],p[6],p[10]
    elif(len(p)==2):
        p[0]=p[1]
    elif(len(p)==4):
        if exprs[p[1]]!=exprs[p[3]]:
            print("Error: Type mismatch in expression.")
        else:
            if p[2]=='+':
                p[0]=p[1],'+',p[3]
                exprs[tuple(p[0])]='Int'
                expraslist[tuple(p[0])]='Int'
            elif p[2]=='-':
                p[0]=p[1],'-',p[3]
                exprs[tuple(p[0])]='Int'
                expraslist[tuple(p[0])]='Int'

def p_term(p):
    '''term : factor
            | term STAR factor
            | term SLASH factor
            | term  PCT factor'''
    if(len(p)==2):
        p[0]=p[1]
    elif(len(p)==4):
        if exprs[p[1]]!=exprs[p[3]]:
            print("Error: Type mismatch in expression.")
        else:
            if p[2]=='*':
                p[0]=p[1],'*',p[3]
                exprs[tuple(p[0])]='Int'
                expraslist[tuple(p[0])]='Int'
            elif p[2]=='/':
                p[0]=p[1],'/',p[3]
                exprs[tuple(p[0])]='Int'
                expraslist[tuple(p[0])]='Int'
            elif p[2]=='%':
                p[0]=p[1],'%',p[3]
                exprs[tuple(p[0])]='Int'
                expraslist[tuple(p[0])]='Int'
        
def p_factor(p):
    '''factor : ID
              | DEFAULT
              | LPAREN expr RPAREN
              | factor LPAREN argsopt RPAREN'''
    if(len(p)==2):
        p[0]=p[1]
        if p[1]=='_':
            exprs['0']='Int' #Default value for an empty expression is 0.
            expraslist['0']='Int'#Default value for an empty expression is 0.
    elif(len(p)==4):
        p[0]=p[2]
    elif(len(p)==5):
        if ids[p[1]]['defdef']=='true':#Denote a procedure	
            p[0]=p[1],p[3]
            expraslist[tuple(p[0])]=ids[p[1]]['type']

def p_factorNUM(p):
    'factor : NUM'
    p[0]=p[1]
    exprs[p[0]]='Int'

def p_test(p):
    '''test : expr NE expr
            | expr LT expr
            | expr LE expr
            | expr GE expr
            | expr GT expr
            | expr EQ expr'''
    if exprs[p[1]]!=exprs[p[3]]:
            print("Error: Type mismatch in expression.")
    else:
        if p[2]=='!=':
            p[0]=p[1],'!=',p[3]
        elif p[2]=='<':
            p[0]=p[1],'<',p[3]
        elif p[2]=='<=':
            p[0]=p[1],'<=',p[3]
        elif p[2]=='>=':
            p[0]=p[1],'>=',p[3]
        elif p[2]=='>':
            p[0]=p[1],'>',p[3]
        elif p[2]=='==':
            p[0]=p[1],'==',p[3]

def p_argsopt(p):
    '''argsopt : args
              | empty'''
    p[0]=p[1]

def p_args(p):
    '''args : expr COMMA args
            | expr'''
    if(len(p)==4):
        p[0]=p[1],p[3]
    else:
        p[0]=p[1]

def p_error(p):
    print("Syntax error in input: " + str(p))
    pass
 
def p_empty(p):
    'empty :'
    p[0]=None

if __name__ == "__main__":
    file=open(sys.argv[1],'r') #Use test file included if you want to revise Scala rules.
    fileLines=file.read()
    parser = yacc.yacc()
    result=parser.parse(fileLines)

    print(fileLines)
    print('\n')

    #To help revise that everything is being parsed correctly
    print('Variables,types,final values:')
    for key, value in ids.items():
            print(key, ' : ', value)
    print('\n')
    print('Expressions, Terms, and Factors Timeline:')
    for key, value in exprs.items():
            print(key, ' : ', value)
    print('\n')
    print('Variables(or def with parameters) and values:')
    for key, value in values.items():
            print(key, ' : ', value)
    print('\n')
    print('Functions and parameters:')
    for key, value in procedures.items():
            print(key, ' : ', value)
    print('\n')
    print('Expras Timeline:')
    for key, value in expraslist.items():
            print(key, ' : ', value)
    print('\n')
    last_key=procedures[list(procedures.keys())[-1]]
    last_key=str(last_key)

    if last_key.count('Int')<3 or last_key.count('Int')>3:#Revising that main procedure is (Int,Int)=>Int.
      print('PARSING ERROR\nCode did not get parsed properly.\nPlease revise code.\n\nCheck things such as: ')
      print('\n1)Function definition -> Main function def must be (Int,Int)=>Int\n2)Variables that are missing initialization->If variable is null at the moment, use \'_\' to set a null value.\n3)Parameters->Parameter types do not need to be initialized.')
      
    #Parsed code
    print('Parsed:')
    print(result)