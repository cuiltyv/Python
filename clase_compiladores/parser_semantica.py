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

class Estructura:

    stack_operandos = []
    cubo = {}
    counter_temporales = 0
    cuadruplos = []
    linea = 0
    symbol_table = {}
    stack_saltos = []
    current_type = None
    lista_auxiliar = []
    listas_aux = []
    listas_index = 0
    
    def __init__(self):
        self.stack = []
        self.cubo = {
            ('int','int','+'): 'int',
            ('int','int','-'): 'int',
            ('int','int','*'): 'int',
            ('int','int','/'): 'int',
            ('int','int','<'): 'bool',
            ('int','int','>'): 'bool',
            ('int','int','<='): 'bool',
            ('int','int','>='): 'bool',
            ('int','int','=='): 'bool',
            ('int','int','!='): 'bool',
            ('float','float','<'): 'bool',
            ('float','float','>'): 'bool',
            ('float','float','<='): 'bool',
            ('float','float','>='): 'bool',
            ('float','float','=='): 'bool',
            ('float','float','!='): 'bool',
            ('float','int','<'): 'bool',
            ('float','int','>'): 'bool',
            ('float','int','<='): 'bool',
            ('float','int','>='): 'bool',
            ('float','int','=='): 'bool',
            ('float','int','!='): 'bool',
            ('int','float','<'): 'bool',
            ('int','float','>'): 'bool',
            ('int','float','<='): 'bool',
            ('int','float','>='): 'bool',
            ('int','float','=='): 'bool',
            ('int','float','!='): 'bool',
            ('int','int','=') : 'int',
            ('float','float','=') : 'float',
            ('int','float','=') : 'float',
            ('float','int','=') : 'float',
            ('bool','bool','=='): 'bool',
            ('bool','bool','!='): 'bool',
            ('bool','bool','<'): 'error',
            ('bool','bool','>'): 'error',
            ('bool','bool','<='): 'error',
            ('bool','bool','>='): 'error',
    }

        self.counter_temporales = 0
        self.cuadruplos = []
        self.linea = 0
        self.stack_saltos = []
        self.symbol_table = {}
        self.current_type = None
        self.listas_aux = []

estructura = Estructura()

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

# VARS_INIT ::= lista_ids ':' tipo ';'
# lista_ids ::= id
# lista_ids ::= lista_ids ',' id

#VARS     ::= 'var' VARS_INIT
def p_VARS(p):
    'VARS : VAR VARS_INIT'
    pass


# separar regla de vars para no tener la recursion en var y tener la lista auxiliar

#VARS_INIT ::= 'id' MORE_IDS ':' TYPE ';' | 'id' MORE_IDS ':' TYPE ';' VARS_INIT
def p_VARS_INIT(p):
    '''VARS_INIT : LISTA_IDS COLON TYPE SEMICOL'''

    pass

def p_VARS_INIT_MORE(p):
    '''VARS_INIT : LISTA_IDS COLON TYPE SEMICOL VARS_INIT''' 
    pass

def p_LISTA_IDS(p):
    '''LISTA_IDS : IDENTIFIER'''
    if p[1] not in estructura.lista_auxiliar:
        estructura.lista_auxiliar.append(p[1])
        print(f"Metiendo {p[1]} a la lista")
    else:
        print(f"Error: Variable '{p[1]}' ya declarada.")
        return
    pass

def p_LISTA_IDS_MORE(p):
    '''LISTA_IDS : LISTA_IDS COMMA IDENTIFIER'''
    if p[3] not in estructura.lista_auxiliar:
        estructura.lista_auxiliar.append(p[3])
        print(f"Metiendo {p[3]} a la lista")
    else:
        print(f"Error: Variable '{p[3]}' ya declarada.")
        return
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
    # verificar que id exista, si existe extraer su tipo de la tabla de simbolos
    valor, tipo = estructura.stack_operandos.pop()

    nombre = p[1]
    if nombre not in estructura.symbol_table:
        print(f"Error: Variable '{nombre}' no declarada.")
        return
    
    tipo_variable = estructura.symbol_table[nombre]
    resultado = estructura.cubo.get((tipo_variable, tipo, '='), 'error')

    if resultado != 'error':

        estructura.linea += 1
        estructura.cuadruplos.append((estructura.linea, '=', valor, None, nombre))

    pass

# CONDITION ::= 'if' '(' EXPRESION ')' Body ELSE_ARG ';'
def p_CONDITION(p):
    'CONDITION : IF LPAREN EXPRESION RPAREN CUADRUPLO_IF Body ELSE_ARG SEMICOL'
    if estructura.stack_saltos:
        salto_final_else = estructura.stack_saltos.pop()
        estructura.cuadruplos[salto_final_else] = (
            estructura.cuadruplos[salto_final_else][0],
            estructura.cuadruplos[salto_final_else][1],
            estructura.cuadruplos[salto_final_else][2],
            estructura.cuadruplos[salto_final_else][3],
            estructura.linea + 1
        )

def p_CUADRUPLO_IF(p):
    'CUADRUPLO_IF :'
    valor, tipo = estructura.stack_operandos.pop()
    if tipo != 'bool':
        print(f"Error: La condición no es booleana. Tipo encontrado: {tipo}")
        return
    estructura.linea += 1
    estructura.cuadruplos.append((estructura.linea, 'gotof', valor, None, 'TEMP'))
    estructura.stack_saltos.append(estructura.linea - 1)

# ELSE_ARG ::= 'else' Body
def p_ELSE_ARG(p):
    'ELSE_ARG : ELSE CUADRUPLO_ELSE Body'
    
def p_CUADRUPLO_ELSE(p):
    'CUADRUPLO_ELSE : empty'
    estructura.linea += 1
    estructura.cuadruplos.append((estructura.linea, 'goto', None, None, 'TEMP'))
    goto_final_index = estructura.linea - 1

    if len(estructura.stack_saltos) > 0:
        gotof_index = estructura.stack_saltos.pop()
        estructura.cuadruplos[gotof_index] = (
            estructura.cuadruplos[gotof_index][0],
            estructura.cuadruplos[gotof_index][1],
            estructura.cuadruplos[gotof_index][2],
            estructura.cuadruplos[gotof_index][3],
            estructura.linea + 1  # Inicio del else
        )
        estructura.stack_saltos.append(goto_final_index)
    else:
        print("Error: No hay salto para asignar en ELSE")


# ELSE_ARG ::= ε
def p_ELSE_ARG_EMPTY(p):
    'ELSE_ARG : empty'
    if len(estructura.stack_saltos) > 0:
        gotof_index = estructura.stack_saltos.pop()
        estructura.cuadruplos[gotof_index] = (
            estructura.cuadruplos[gotof_index][0],
            estructura.cuadruplos[gotof_index][1],
            estructura.cuadruplos[gotof_index][2],
            estructura.cuadruplos[gotof_index][3],
            estructura.linea + 1
        )
    else:
        print("Error: No hay salto para asignar en ELSE vacío")


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
    
    print(f"Lista auxiliar: {estructura.lista_auxiliar}")

    for cosa in estructura.lista_auxiliar:
        if cosa not in estructura.symbol_table:
            estructura.symbol_table[cosa] = p[1]
            print(f"Agregando {cosa} a la tabla de simbolos con tipo {p[1]}")
        else:
            print(f"Error: Variable '{cosa}' ya declarada.")
            return

    estructura.lista_auxiliar = []
  
    print(f"Tipo actual: {estructura.current_type}")
    print(p[1])

    p[0] = p[1]

    pass



# VOLTEAR LA GRAMATICA IZQUIERDA A DERECHA
# exp ::= Exp + Termino
# Termino ::= termino * factor

#EXP      ::= TERMINO EXP_OPT

#EXP_OPT ::= ('+' | '-' ) TERMINO EXP_OPT | epsilon
    



# EXPRESION ::= EXP | EXP (relop) EXP
def p_EXPRESION(p):
    '''EXPRESION : EXP'''
    pass


def p_EXPRESION_REL(p):
    '''EXPRESION : EXP LESS EXP
                 | EXP GREATER EXP
                 | EXP NOT_EQUAL EXP
                 | EXP EQUALS EXP
                 | EXP LESS_EQUAL EXP
                 | EXP GREATER_EQUAL EXP
                 '''
    
    valor_2, tipo_2 = estructura.stack_operandos.pop()
    valor_1, tipo_1 = estructura.stack_operandos.pop()
    operador = p[2]

    resultado = estructura.cubo.get((tipo_1,tipo_2,operador),'error')

    if resultado != 'error':
        estructura.counter_temporales += 1
        variable_temporal = f"t{estructura.counter_temporales}"    
        estructura.stack_operandos.append((variable_temporal,resultado))


        estructura.linea += 1
        estructura.cuadruplos.append((estructura.linea,operador,valor_1,valor_2,variable_temporal))
    
    


# EXP ::= EXP ('+'|'-') TERMINO | TERMINO
def p_EXP(p):
    '''EXP : TERMINO'''
    pass

def p_EXP_SUM(p):
    '''EXP : EXP OP_SUM TERMINO'''
    print(f"Stack operandos: {estructura.stack_operandos}")
    valor_2, tipo_2 = estructura.stack_operandos.pop()
    valor_1, tipo_1 = estructura.stack_operandos.pop()

    resultado = estructura.cubo.get((tipo_1,tipo_2,'+'),'error')


    if resultado != 'error':
        estructura.counter_temporales += 1
        variable_temporal = f"t{estructura.counter_temporales}"    

        estructura.stack_operandos.append((variable_temporal,resultado))


        estructura.linea += 1
        estructura.cuadruplos.append((estructura.linea,'+',valor_1,valor_2,variable_temporal))
    else:
        print(f"No se puede hacer operacion de + con {tipo_1} y {tipo_2}")


    pass

def p_EXP_SUB(p):
    '''EXP : EXP OP_SUB TERMINO'''
    print(f"Stack operandos: {estructura.stack_operandos}")
    valor_2, tipo_2 = estructura.stack_operandos.pop()
    valor_1, tipo_1 = estructura.stack_operandos.pop()

    resultado = estructura.cubo.get((tipo_1,tipo_2,'-'),'error')


    if resultado != 'error':
        estructura.counter_temporales += 1
        variable_temporal = f"t{estructura.counter_temporales}"    

        estructura.stack_operandos.append((variable_temporal,resultado))


        estructura.linea += 1
        estructura.cuadruplos.append((estructura.linea,'-',valor_1,valor_2,variable_temporal))
    else:
        print(f"No se puede hacer operacion de - con {tipo_1} y {tipo_2}")


    pass

# TERMINO ::= TERMINO ('*'|'/') FACTOR | FACTOR
def p_TERMINO(p):
    '''TERMINO : FACTOR'''
    pass

def p_TERMINO_MULT(p):
    '''TERMINO : TERMINO OP_MULT FACTOR'''
    print(f"Stack operandos: {estructura.stack_operandos}")
    valor_2, tipo_2 = estructura.stack_operandos.pop()
    valor_1, tipo_1 = estructura.stack_operandos.pop()

    resultado = estructura.cubo.get((tipo_1,tipo_2,'*'),'error')


    if resultado != 'error':
        estructura.counter_temporales += 1
        variable_temporal = f"t{estructura.counter_temporales}"    

        estructura.stack_operandos.append((variable_temporal,resultado))


        estructura.linea += 1
        estructura.cuadruplos.append((estructura.linea,'*',valor_1,valor_2,variable_temporal))
    else:
        print(f"No se puede hacer operacion de * con {tipo_1} y {tipo_2}")


    pass

def p_TERMINO_DIV(p):
    '''TERMINO : TERMINO OP_DIV FACTOR'''
    print(f"Stack operandos: {estructura.stack_operandos}")
    valor_2, tipo_2 = estructura.stack_operandos.pop()
    valor_1, tipo_1 = estructura.stack_operandos.pop()

    resultado = estructura.cubo.get((tipo_1,tipo_2,'/'),'error')


    if resultado != 'error':
        estructura.counter_temporales += 1
        variable_temporal = f"t{estructura.counter_temporales}"    

        estructura.stack_operandos.append((variable_temporal,resultado))


        estructura.linea += 1
        estructura.cuadruplos.append((estructura.linea,'/',valor_1,valor_2,variable_temporal))
    else:
        print(f"No se puede hacer operacion de / con {tipo_1} y {tipo_2}")


    pass



#FACTOR   ::= '(' EXPRESION ')' | SIGN ( 'id' | CTE )
def p_FACTOR(p):
    '''FACTOR : LPAREN EXPRESION RPAREN'''
    
    pass

def p_FACTOR_ID(p):
    '''FACTOR : IDENTIFIER'''
    
    valor = p[1]
    
    if p[1] not in estructura.symbol_table:
        print(f"Error: Variable '{p[1]}' no declarada.")
        return
    
    tipo = estructura.symbol_table[p[1]]
    estructura.stack_operandos.append((valor, tipo))
    pass

def p_FACTOR_ID_SIGN(p):
    '''FACTOR : SIGN IDENTIFIER'''
    
    valor = p[2]
    
    print("ACABA")
    if p[2] not in estructura.symbol_table:
        print(f"Error: Variable '{p[2]}' no declarada.")
        return
    

    sign = p[1] if p[1] is not None else '+'
    if sign == '-':
        estructura.linea += 1
        estructura.counter_temporales += 1
        temp_var = f"t{estructura.counter_temporales}"
        estructura.cuadruplos.append((estructura.linea, '-', valor, None, temp_var))
        type = estructura.symbol_table[p[2]]
        estructura.stack_operandos.append((temp_var, type))
       
        
    pass

def p_FACTOR_CTE(p):
    '''FACTOR : SIGN CTE'''
    valor = p[2]

    sign = p[1]
    if sign == '-':
        estructura.counter_temporales += 1
        temp_var = f"t{estructura.counter_temporales}"
        estructura.linea += 1
        estructura.cuadruplos.append((estructura.linea, '-', valor, None, temp_var))
        estructura.stack_operandos.append((temp_var, type))
        
    pass


#SIGN ::= '+' | '-' | epsilon
def p_SIGN(p):
    '''SIGN : OP_SUM
            | OP_SUB
            | empty'''
    p[0] = p[1]
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
    '''CTE : CTE_INT
           | CTE_FLOAT'''
    pass
    
def p_CTE_INT(p):
    'CTE_INT : CONST_INT'
    estructura.stack_operandos.append((p[1], 'int'))
    pass

def p_CTE_FLOAT(p):
    'CTE_FLOAT : CONST_FLOAT'
    estructura.stack_operandos.append((p[1], 'float'))
    pass

def p_empty(p):
    'empty :'
    pass
    

def p_error(p):
    if p:
        print(f"Syntax error at token '{p.type}', value '{p.value}' (line {p.lineno})")
    else:
        return

    while True:
        tok = parser.token()             
        if not tok or tok.type == 'SEMICOL': break
    parser.errok()

    

    return tok 

# Crear el lexer
lexer = lex.lex()


parser = yacc.yacc()


program = ""

with open('program.ld', 'r') as file:
    program = file.read()



result = parser.parse(program, lexer=lexer)


for q in estructura.cuadruplos:
    print(q)

print("Tabla de simbolos")
for key, value in estructura.symbol_table.items():
    print(f"{key}: {value}")


#Gramatica
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