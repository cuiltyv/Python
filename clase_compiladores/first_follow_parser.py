import ply.lex as lex
from collections import defaultdict

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

#Funciones de expresiones regulares
def t_COMMENT(t):
    r'\#.*'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENTIFIER')
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
    print(f"Illegal character {t.value[0]} in position {t.lexpos}")
    t.lexer.skip(1)

# Crear el lexer
lexer = lex.lex()

parse_table = {}
parse_table['EXP'] = {}
parse_table['EXP_PRIME'] = {}
parse_table['EXPRESION'] = {}
parse_table['EXPRESION_PRIME'] = {}
parse_table['TERMINO'] = {}
parse_table['TERMINO_PRIME'] = {}
parse_table['FACTOR'] = {}
parse_table['ASSIGN'] = {}
parse_table['CTE'] = {}
parse_table['VARS'] = {}
parse_table['SIGN'] = {}

parse_table['ASSIGN'] = { 'IDENTIFIER' : ['IDENTIFIER', 'OP_ASIGNA', 'EXPRESION', 'SEMICOL']}
parse_table['EXPRESION'] = { 'IDENTIFIER' : ['EXP', 'EXPRESION_PRIME'],
                            'LPAREN' : ['EXP', 'EXPRESION_PRIME'],
                            'OP_SUM' : ['EXP', 'EXPRESION_PRIME'],
                            'OP_SUB' : ['EXP', 'EXPRESION_PRIME'],
                            'CONST_INT' : ['EXP', 'EXPRESION_PRIME'],
                            'CONST_FLOAT' : ['EXP', 'EXPRESION_PRIME']}
parse_table['EXPRESION_PRIME'] = { 'GREATER' : ['GREATER', 'EXP'],
                                  'LESS' : ['LESS', 'EXP'],
                                  'NOT_EQUAL' : ['NOT_EQUAL', 'EXP'],
                                  'EQUALS' : ['EQUALS', 'EXP'],
                                  'LESS_EQUAL' : ['LESS_EQUAL', 'EXP'],
                                  'GREATER_EQUAL' : ['GREATER_EQUAL', 'EXP'],
                                  'RPAREN' : [],
                                  'SEMICOL' : []}
parse_table['EXP'] = { 'IDENTIFIER' : ['TERMINO', 'EXP_PRIME'],
                      'LPAREN' : ['TERMINO', 'EXP_PRIME'],
                      'OP_SUM' : ['TERMINO', 'EXP_PRIME'],
                      'OP_SUB' : ['TERMINO', 'EXP_PRIME'],
                      'CONST_INT' : ['TERMINO', 'EXP_PRIME'],
                      'CONST_FLOAT' : ['TERMINO', 'EXP_PRIME']}
parse_table['EXP_PRIME'] = { 'OP_SUM' : ['OP_SUM', 'TERMINO', 'EXP_PRIME'],
                            'OP_SUB' : ['OP_SUB', 'TERMINO', 'EXP_PRIME'],
                            'GREATER' : [],
                            'LESS' : [],
                            'NOT_EQUAL' : [],
                            'EQUALS' : [],
                            'LESS_EQUAL' : [],
                            'GREATER_EQUAL' : [],
                            'RPAREN' : [],
                            'SEMICOL' : [] }
parse_table['TERMINO'] = { 'IDENTIFIER' : ['FACTOR', 'TERMINO_PRIME'],
                          'LPAREN' : ['FACTOR', 'TERMINO_PRIME'],
                          'OP_SUM' : ['FACTOR', 'TERMINO_PRIME'],
                          'OP_SUB' : ['FACTOR', 'TERMINO_PRIME'],
                          'CONST_INT' : ['FACTOR', 'TERMINO_PRIME'],
                          'CONST_FLOAT' : ['FACTOR', 'TERMINO_PRIME']}
parse_table['TERMINO_PRIME'] = { 'OP_MULT' : ['OP_MULT', 'FACTOR', 'TERMINO_PRIME'],
                                'OP_DIV' : ['OP_DIV', 'FACTOR', 'TERMINO_PRIME'],
                                'OP_SUM' : [],
                                'OP_SUB' : [],
                                'GREATER' : [],
                                'LESS' : [],
                                'NOT_EQUAL' : [],
                                'EQUALS' : [],
                                'LESS_EQUAL' : [],
                                'GREATER_EQUAL' : [],
                                'RPAREN' : [],
                                'SEMICOL' : [] }
parse_table['FACTOR'] = { 'IDENTIFIER' : ['VARS'],
                        'LPAREN' : ['LPAREN', 'EXPRESION', 'RPAREN'],
                        'OP_SUM' : ['SIGN', 'VARS'],
                        'OP_SUB' : ['SIGN', 'VARS'],
                        'CONST_INT' : ['VARS'],
                        'CONST_FLOAT' : ['VARS']}
parse_table['SIGN'] = { 'OP_SUM' : ['OP_SUM'],
                        'OP_SUB' : ['OP_SUB']}
parse_table['VARS'] = { 'IDENTIFIER' : ['IDENTIFIER'],
                        'CONST_INT' : ['CTE'],
                        'CONST_FLOAT' : ['CTE']}
parse_table['CTE'] = { 'CONST_INT' : ['CONST_INT'],
                        'CONST_FLOAT' : ['CONST_FLOAT']}
                         

# Clase de tokens
class Tokens:
    def __init__(self, text):
        self.tokens = []
        self.pos = 0
        
        # A comparacion del codigo orignal, aqui se agrega un while que recorre el texto por el lexer y va agregando los tokens al array de tokens
        lexer.input(text)
        while True:
            tok = lexer.token()
            if not tok:
                break

            self.tokens.append((tok.type, tok.value))
        
        self.tokens.append(("$", ""))

    def current(self):
        return self.tokens[self.pos]

    def avanza(self):
        self.pos += 1
        return self.tokens[self.pos]

def addError(errors, expected, token, index):
    errors.append(f"ERROR en index {index}: esperaba {expected}, recibio {token}")

def ff_parser(tokens, errors):
    token, content = tokens.current()
    x = "ASSIGN"
    stack = []
    stack.append("$")
    stack.append(x)

    while stack:
        x = stack.pop()
        if x == "$" and token == "$":
            break

        if x == token:
            tokens.avanza()
            token, content = tokens.current()
        elif x in parse_table:
            if token in parse_table[x]:
                for i in reversed(parse_table[x][token]):
                    stack.append(i)
            else:
                addError(errors, token, x, tokens.pos)
        else:
            addError(errors, x, token, tokens.pos)


def parser(text):
    tokens = Tokens(text)
    errors = []
    ff_parser(tokens, errors)

    if tokens.pos < len(tokens.tokens)-1: #   Si no se consumio toda la linea, hubo algun token inesperado
        addError(errors, "operador", tokens.current(), tokens.pos)

    return errors

program = "";

with open("program.ld", "r") as file:
    program = file.read()

program = program.splitlines()

for line in program:
    print(f"\nTesting: {line}")
    errors = parser(line)
    
    if len(errors) == 0:
        print("OK")
    else:
        for e in errors:
            print(e) 