import ply.lex as lex
import ply.yacc as yacc
import re

def ler_arquivo(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        linhas = file.readlines() 
    return [linha.strip() for linha in linhas]

reserved = {
    'printf': 'PRINTF',
}

tokens = (
    'LEFT_PARENTESIS',
    'RIGHT_PARENTESIS',
    'STRING',
    'COMMA',
    'SEMICOLON',
    'INT',
    'FLOAT',
    'IDENTIFIER'
) + tuple(reserved.values())  

t_LEFT_PARENTESIS = r'\('
t_RIGHT_PARENTESIS = r'\)'
t_STRING = r'\".*?\"'
t_COMMA = r','
t_SEMICOLON = r';'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*(\s*\+\s*[a-zA-Z_][a-zA-Z0-9_]*)*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

precedence = (
    ('left', 'PRINTF'),
    ('left', 'IDENTIFIER'),
)

def p_statement(p):
    '''statement : PRINTF LEFT_PARENTESIS first_arg additional_args RIGHT_PARENTESIS SEMICOLON'''
    semantic_validation(p)
    print(f"Parsed printf with args: {p[3]} and additional: {p[4]}")

def p_first_arg(p):
    '''first_arg : STRING'''
    p[0] = p[1]

def p_additional_args(p):
    '''additional_args : COMMA arg additional_args
                       | COMMA arg
                       | empty'''
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    elif len(p) == 3:
        p[0] = [p[2]]
    else:
        p[0] = []

def p_empty(p):
    '''empty :'''
    p[0] = []

def p_arg(p):
    '''arg : INT
           | FLOAT
           | STRING
           | IDENTIFIER'''
    p[0] = p[1]

def p_error(p):
    print("Syntax error at '%s'" % p.value if p else "Syntax error at EOF")

def semantic_validation(p):
    placeholders = re.findall(r'%[sidf]', p[3])
    if(len(placeholders) != len(p[4])):
        raise ValueError('SEMANTIC ERROR')
    zipped = list(zip(placeholders, p[4]))
    for pair in zipped:
        placeholder = pair[0]
        value = pair[1]
        if not isinstance(value, str):
            if(re.match(r'%i', placeholder)):
                if not isinstance(value, int):
                    raise ValueError('SEMANTIC ERROR')
            elif(re.match(r'%[df]', placeholder)):
                if not isinstance(value, float):
                    raise ValueError('SEMANTIC ERROR')
            elif(re.match(r'%s', placeholder)):
                if not re.match(r'\".*?\"', value):
                    raise ValueError('SEMANTIC ERROR')
        elif re.match(r'\".*?\"', value) and re.match(r'%[idf]', placeholder):
            raise ValueError('SEMANTIC ERROR')

lexer = lex.lex()
parser = yacc.yacc()

dados = ler_arquivo('dados2.txt')
for palavra in dados:
    parser.parse(palavra)
