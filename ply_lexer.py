import ply.lex as lex

reserved = {
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE'
} 

tokens = [
    'CONST_INT',
    'IDENTIFIER',
    'OP_ASIGNA',
    'SEMICOL'
] + list(reserved.values())

t_OP_ASIGNA = r'='
t_SEMICOL = r';'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
    return t

def t_CONST_INT (t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

data =  """ 

      if a = 27;
      otra_var = 12;
  """

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
