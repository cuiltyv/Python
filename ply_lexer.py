import ply.lex as lex
from collections import defaultdict

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

tokens = [
    'CONST_INT',
    'IDENTIFIER',
    'OP_ASIGNA',
    'EQUALS',
    'SEMICOL',
    'OP_ARITH',
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

t_OP_ASIGNA = r'='
t_EQUALS = r'=='
t_SEMICOL = r';'
t_OP_ARITH = r'[-+*/]'
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

def t_COMMENT(t):
    r'\#.*'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENTIFIER')   # Check for reserved words
    if(t.type == 'IDENTIFIER'):
        simbolos[t.value].append((t.type, indx, t.lexpos))
    return t

def t_CONST_FLOAT (t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_CONST_INT (t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_CONST_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]  # Quita comillas
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character {t.value[0]} in position {t.lexpos}")
    errors.append((t.value[0], t.lexpos, indx))
    t.lexer.skip(1)




data =  """ 
    program celcius_to_farenheit;
    var celcius, farenheit : float;
    main {
        celcius = 10.0
        farenheit = (celcius * 9 / 5) + 32;
        print(farenheit);
        if(farenheit > 70){
            print("Calido");
        } else {
            print("Fresco")
        }
    }
    end
  """

lexer = lex.lex()

dataPerLine = data.splitlines()
indx = 0
errors = []
simbolos = defaultdict(list)

for indx, line in enumerate(dataPerLine):
    
    line = line.strip()

    lexer.input(line)

    print(f"Linea {indx}: {line if line else 'Linea Vacia'}")

    while True:
        tok = lexer.token()
        if not tok:
            break
        # print(tok)
        print(f"{tok.type:<15} value: {tok.value:<8} lexpos: {tok.lexpos}")
   
   #LexToken({self.type},{self.value!r},{self.lineno},{self.lexpos}) <- Asi se asigna el valor al tok = lexer.token()
        
    print()

print("Tabla de Errores")
for error, pos, index in errors:
    print(f"Error: {error:<6} linea: {index:<6} lexpos: {pos}")

print("\nTabla de Simbolos")
for substring, attributes in simbolos.items():
      for (token,line,index) in attributes:
        print(f"Token: {token:<14} valor: {substring:<8} linea: {line:<8} lexpos: {index}")