import ply.lex as lex
import ply.yacc as yacc

# Palabras reservadas
reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'print' : 'PRINT',
    'main' : 'MAIN',
    'program' : 'PROGRAM',
    'var' : 'VAR',
    'int' : 'INT',
    'float' : 'FLOAT',
    'do' : 'DO',
    'void' : 'VOID',
    'string' : 'STRING',
    'end' : 'END',
} 

# Tokens
tokens = [
    'CONST_INT',
    'IDENTIFIER',
    'OP_ASIGNA',
    'EQUALS',
    'SEMICOL',
    'OP_SUM',
    'OP_SUB',
    'OP_MULT',
    'OP_DIV',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'LSQBRACKET',
    'RSQBRACKET',
    'LBRACKET',
    'RBRACKET',
    'GREATER',
    'LESS',
    'NOT_EQUAL',
    'LESS_EQUAL',
    'GREATER_EQUAL',
    'COMMENT',
    'COLON',
    'CONST_FLOAT',
    'CONST_STRING',
] + list(reserved.values())

# Expresiones regulares
t_OP_ASIGNA = r'='
t_EQUALS = r'=='
t_SEMICOL = r';'
t_OP_SUM = r'\+'
t_OP_SUB = r'-'
t_OP_MULT = r'\*'
t_OP_DIV = r'/'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQBRACKET = r'\['
t_RSQBRACKET = r'\]'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_GREATER = r'>'
t_LESS = r'<'
t_NOT_EQUAL = r'!='
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_COLON = r':'

# Funciones de expresiones regulares
def t_COMMENT(t):
    r'\#.*'
    pass  # Ignore comments

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_CONST_FLOAT(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_CONST_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_CONST_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]  # Remove quotes
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print(f"Lexic error at character {t.value[0]} in position {t.lexpos} at line {t.lineno}")
    t.lexer.skip(1)


#PARSER

#PROGRAM  ::= 'program' 'id' ';' VARS_OPT FUNCS_OPT 'main' Body 'end'
def p_program(p):
    'program : PROGRAM IDENTIFIER SEMICOL VARS_OPT FUNCS_OPT MAIN Body END'
    pass

#VARS_OPT ::= VARS | epsilon
def p_VARS_OPT(p):
    '''VARS_OPT : VARS
                | empty'''
    pass

#FUNCS_OPT ::= FUNCS FUNCS_OPT | epsilon
def p_FUNCS_OPT(p):
    '''FUNCS_OPT : FUNCS FUNCS_OPT
                 | empty'''
    pass

#VARS     ::= 'var' VARS_INIT
def p_VARS(p):
    'VARS : VAR VARS_INIT'
    pass

#VARS_INIT ::= 'id' MORE_IDS ':' TYPE ';' | 'id' MORE_IDS ':' TYPE ';' VARS_INIT
def p_VARS_INIT(p):
    '''VARS_INIT : IDENTIFIER MORE_IDS COLON TYPE SEMICOL
                 | IDENTIFIER MORE_IDS COLON TYPE SEMICOL VARS_INIT'''
    pass

#MORE_IDS ::= ',' 'id' MORE_IDS | epsilon
def p_MORE_IDS(p):
    '''MORE_IDS : COMMA IDENTIFIER MORE_IDS
                | empty'''
    pass

#FUNCS    ::= 'void' 'id' '(' ARGS ')' '[' VARS_OPT Body ']' ';'
def p_FUNCS(p):
    'FUNCS : VOID IDENTIFIER LPAREN ARGS RPAREN LSQBRACKET VARS_OPT Body RSQBRACKET SEMICOL'
    pass

#MORE_ARGS ::= ',' 'id' ':' 'type' MORE_ARGS | epsilon
def p_MORE_ARGS(p):
    '''MORE_ARGS : COMMA IDENTIFIER COLON TYPE MORE_ARGS
                 | empty'''
    pass

#ARGS ::= 'id' ':' 'type' MORE_ARGS | epsilon
def p_ARGS(p):
    '''ARGS : IDENTIFIER COLON TYPE MORE_ARGS
            | empty'''
    pass

#Body     ::= '{' STATEMENT_OPT '}'
def p_Body(p):
    'Body : LBRACKET STATEMENT_OPT RBRACKET'
    pass

#STATEMENT_OPT ::= STATEMENT STATEMENT_OPT | epsilon
def p_STATEMENT_OPT(p):
    '''STATEMENT_OPT : STATEMENT STATEMENT_OPT
                     | empty'''
    pass

#STATEMENT
#       ::= ASSIGN
#           | CONDITION
#           | CYCLE
#           | F_Call
#           | Print
def p_STATEMENT(p):
    '''STATEMENT : ASSIGN
                    | CONDITION
                    | CYCLE
                    | F_CALL
                    | PRINTP'''
    pass

#ASSIGN   ::= 'id' '=' EXPRESION ';'
def p_ASSIGN(p):
    'ASSIGN : IDENTIFIER OP_ASIGNA EXPRESION SEMICOL'
    pass

#CONDITION    ::= 'if' '(' EXPRESION ')' Body ELSE_ARG ';'
def p_CONDITION(p):
    'CONDITION : IF LPAREN EXPRESION RPAREN Body ELSE_ARG SEMICOL'
    pass

#ELSE_ARG    ::= 'else' Body | epsilon
def p_ELSE_ARG(p):
    '''ELSE_ARG : ELSE Body
                | empty'''
    pass

#CYCLE    ::= 'do' Body 'while' '(' Expresion ')' ';'
def p_CYCLE(p):
    '''CYCLE : DO Body WHILE LPAREN EXPRESION RPAREN SEMICOL'''
    pass
    
#Print    ::= 'print' '(' ( EXPRESION | 'cte.string' ) MORE_PRINT_ARGS ')' ';'
def p_PRINTP(p):
    '''PRINTP : PRINT LPAREN CONST_STRING MORE_PRINT_ARGS RPAREN SEMICOL
            | PRINT LPAREN EXPRESION MORE_PRINT_ARGS RPAREN SEMICOL'''
    pass

#MORE_PRINT_ARGS ::=  ',' ( EXPRESION | 'cte.string' ) MORE_PRINT_ARGS | epsilon
def p_MORE_PRINT_ARGS(p):
    '''MORE_PRINT_ARGS : COMMA CONST_STRING MORE_PRINT_ARGS
                        | COMMA EXPRESION MORE_PRINT_ARGS
                       | empty'''
    pass

#TYPE     ::= 'int'
#           | 'float'
def p_TYPE(p):
    '''TYPE : INT
            | FLOAT'''
    
    pass

#EXPRESION ::= EXP EXPRESION_OPT
def p_EXPRESION(p):
    'EXPRESION : EXP EXPRESION_OPT'
    pass

#EXPRESION_OPT ::= ( '<' | '>' | '!=' | '==' | '>=' | '<=' ) EXP | epsilon
def p_EXPRESION_OPT(p):
    '''EXPRESION_OPT : LESS EXP
                     | GREATER EXP
                     | NOT_EQUAL EXP
                     | EQUALS EXP
                     | LESS_EQUAL EXP
                     | GREATER_EQUAL EXP
                     | empty'''
    pass

#EXP      ::= TERMINO EXP_OPT
def p_EXP(p):
    'EXP : TERMINO EXP_OPT'
    pass

#EXP_OPT ::= ('+' | '-' ) TERMINO EXP_OPT | epsilon
def p_EXP_OPT(p):
    '''EXP_OPT : OP_SUM TERMINO EXP_OPT
               | OP_SUB TERMINO EXP_OPT
               | empty'''
    pass

#TERMINO  ::= FACTOR TERMINO_OPT
def p_TERMINO(p):
    'TERMINO : FACTOR TERMINO_OPT'
    pass

#TERMINO_OPT ::= ( '*' | '/' ) FACTOR TERMINO_OPT | epsilon
def p_TERMINO_OPT(p):
    '''TERMINO_OPT : OP_MULT FACTOR TERMINO_OPT
                   | OP_DIV FACTOR TERMINO_OPT
                   | empty'''
    pass

#FACTOR   ::= '(' EXPRESION ')' | SIGN ( 'id' | CTE )
def p_FACTOR(p):
    '''FACTOR : LPAREN EXPRESION RPAREN
              | SIGN IDENTIFIER 
              | SIGN CTE'''
    pass

#SIGN ::= '+' | '-' | epsilon
def p_SIGN(p):
    '''SIGN : OP_SUM
            | OP_SUB
            | empty'''
    pass

#F_CALL   ::= 'id' '(' OPT_EXPRESION ')' ';'
def p_F_CALL(p):
    'F_CALL : IDENTIFIER LPAREN OPT_EXPRESION RPAREN SEMICOL'
    pass

#OPT_EXPRESION :: EXPRESION MORE_EXPRESION | epsilon
def p_OPT_EXPRESION(p):
    '''OPT_EXPRESION : EXPRESION MORE_EXPRESION
                     | empty'''
    pass


# MORE_EXPRESION ::= ',' EXPRESION MORE_EXPRESION | epsilon
def p_MORE_EXPRESION(p):
    '''MORE_EXPRESION : COMMA EXPRESION MORE_EXPRESION
                      | empty'''
    pass

# CTE ::= 'cte_int' | 'cte_float'
def p_CTE(p):
    '''CTE : CONST_INT
           | CONST_FLOAT'''
    pass
    
def p_empty(p):
    'empty :'
    pass
    

def p_error(p):
    # Read ahead looking for a terminating ";"
    if p:
        print(f"Syntax error at token '{p.type}', value '{p.value}' (line {p.lineno})")
    else:
        return

    while True:
        tok = parser.token()             
        if not tok or tok.type == 'SEMICOL': break
    parser.errok()

    # Return SEMI to the parser as the next lookahead token
    return tok 

# Crear el lexer
lexer = lex.lex()


parser = yacc.yacc()

# Probar un código de ejemplo

program = ""

with open('program.ld', 'r') as file:
    program = file.read()



result = parser.parse(program, lexer=lexer)
print(result)






#Gramatic fetuchinni
"""
PROGRAM  ::= 'program' 'id' ';' VARS_OPT FUNCS_OPT 'main' Body 'end'

VARS_OPT ::= VARS | epsilon

FUNCS_OPT ::= FUNCS FUNCS_OPT | epsilon

VARS     ::= 'var' VARS_INIT

VARS_INIT ::= 'id' MORE_IDS ':' TYPE ';' | 'id' MORE_IDS ':' TYPE ';' VARS_INIT

MORE_IDS ::= ',' 'id' MORE_IDS | epsilon

FUNCS    ::= 'void' 'id' '(' ARGS ')' '[' VARS_OPT Body ']' ';'

MORE_ARGS ::= ',' 'id' ':' TYPE MORE_ARGS | epsilon

ARGS ::= 'id' ':' TYPE MORE_ARGS | epsilon

Body     ::= '{' STATEMENT_OPT '}'

STATEMENT_OPT ::= STATEMENT STATEMENT_OPT | epsilon

STATEMENT
         ::= ASSIGN
           | CONDITION
           | CYCLE
           | F_Call
           | Print

ASSIGN   ::= 'id' '=' EXPRESION ';'

CONDITION    ::= 'if' '(' EXPRESION ')' Body ELSE_ARG ';'

ELSE_ARG    ::= 'else' Body | epsilon
   
CYCLE    ::= 'do' Body 'while' '(' Expresion ')' ';'

Print    ::= 'print' '(' ( EXPRESION | 'cte.string' ) MORE_PRINT_ARGS ')' ';'

MORE_PRINT_ARGS ::=  ',' ( EXPRESION | 'cte.string' ) MORE_PRINT_ARGS | epsilon

TYPE     ::= 'int'
           | 'float'

EXPRESION
         ::= EXP EXPRESION_OPT

EXPRESION_OPT ::= ( '<' | '>' | '!=' | '==' ) EXP | epsilon

EXP      ::= TERMINO EXP_OPT

EXP_OPT ::= ('+' | '-' ) TERMINO EXP_OPT | epsilon

TERMINO  ::= FACTOR TERMINO_OPT

TERMINO_OPT ::= ( '*' | '/' ) FACTOR TERMINO_OPT | epsilon

FACTOR   ::= '(' EXPRESION ')'
            | SIGN ( 'id' | CTE )

SIGN ::= '+' | '-' | epsilon
            
F_CALL   ::= 'id' '(' OPT_EXPRESION ')' ';'

OPT_EXPRESION :: EXPRESION MORE_EXPRESION | epsilon

MORE_EXPRESION ::= ',' EXPRESION MORE_EXPRESION | epsilon

CTE      ::= 'cte_int'
           | 'cte_float'


"""



# GRAMATICINI FUNCIONALINI
"""

PROGRAM  ::= 'program' 'id' ';' VARS_OPT FUNCS_OPT 'main' Body 'end'

VARS_OPT ::= VARS | epsilon

FUNCS_OPT ::= FUNCS FUNCS_OPT | epsilon

VARS     ::= 'var' VARS_INIT

VARS_INIT ::= 'id' MORE_IDS ':' TYPE ';' | 'id' MORE_IDS ':' TYPE ';' VARS_INIT

MORE_IDS ::= ',' 'id' MORE_IDS | epsilon

FUNCS    ::= 'void' 'id' '(' ARGS ')' '[' VARS_OPT Body ']' ';'

MORE_ARGS ::= ',' 'id' ':' 'type' MORE_ARGS | epsilon

ARGS ::= 'id' ':' 'type' MORE_ARGS | epsilon

Body     ::= '{' STATEMENT_OPT '}'

STATEMENT_OPT ::= STATEMENT STATEMENT_OPT | epsilon

STATEMENT
         ::= ASSIGN
           | CONDITION
           | CYCLE
           | F_Call
           | Print

ASSIGN   ::= 'id' '=' EXPRESION ';'

CONDITION    ::= 'if' '(' EXPRESION ')' Body ELSE_ARG ';'
ELSE_ARG    ::= 'else' Body | epsilon
   
CYCLE    ::= 'do' Body 'while' '(' Expresion ')' ';'

Print    ::= 'print' '(' ( EXPRESION | 'cte.string' ) MORE_PRINT_ARGS ')' ';'

MORE_PRINT_ARGS ::=  ',' ( EXPRESION | 'cte.string' ) MORE_PRINT_ARGS | epsilon

TYPE     ::= 'int'
           | 'float'

EXPRESION ::= EXP EXPRESION_OPT

EXPRESION_OPT ::= ( '<' | '>' | '!=' | '==' ) EXP | epsilon

EXP      ::= TERMINO EXP_OPT

EXP_OPT ::= ('+' | '-' ) TERMINO EXP_OPT | epsilon

TERMINO  ::= FACTOR TERMINO_OPT

TERMINO_OPT ::= ( '*' | '/' ) FACTOR TERMINO_OPT | epsilon

FACTOR   ::= '(' EXPRESION ')'
            | SIGN ( 'id' | CTE )

SIGN ::= '+" | '-' | epsilon
            
F_CALL   ::= 'id' '(' OPT_EXPRESION ')' ';'

OPT_EXPRESION :: EXPRESION MORE_EXPRESION | epsilon

MORE_EXPRESION ::= ',' EXPRESION MORE_EXPRESION | epsilon

CTE      ::= 'cte_int'
           | 'cte_float'


"""