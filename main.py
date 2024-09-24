import ply.lex as lex
import ply.yacc as yacc

# %s - stirng
# %i - int
# %.f/%.2d - float/double

def ler_arquivo(file_path):
    with open(file_path, 'r') as file:
        linhas = file.readlines() 
    return [linha.strip() for linha in linhas]

tokens = (
    'PRINTF',
    'LEFT_PARENTESIS',
    'RIGHT_PARENTESIS',
    'STRING',
    'COMMA',
    'SEMICOLON',
    'INT',
    'FLOAT',
    # 'CHAR'
    'IDENTIFIER'
)

t_PRINTF = r'printf'
t_LEFT_PARENTESIS = r'\('
t_RIGHT_PARENTESIS = r'\)'
t_STRING = r'\".*?\"'
t_COMMA = r','
t_SEMICOLON = r';'
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'

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

precedence = ()

# fixme corrigir para aceitar com argumentos 
def p_statement(p):
    '''statement : PRINTF LEFT_PARENTESIS first_arg additional_args RIGHT_PARENTESIS SEMICOLON'''
    print(f"Parsed printf with args: {p[3]} and additional: {p[4]}")

def p_first_arg(p):
    '''first_arg : STRING'''
    p[0] = p[1]

def p_additional_args_multiple(p):
    '''additional_args : COMMA arg additional_args'''
    p[0] = [p[2]] + p[3]

def p_additional_args_single(p):
    '''additional_args : COMMA arg'''
    p[0] = [p[2]]

def p_additional_args_empty(p):
    '''additional_args : '''
    p[0] = []

def p_arg(p):
    '''arg : INT
           | FLOAT
           | IDENTIFIER'''
    p[0] = p[1]

def p_error(p):
    print("Syntax error at '%s'" % p.value if p else "Syntax error at EOF")

lexer = lex.lex()
parser = yacc.yacc()

dados = ler_arquivo('dados2.txt')
for palavra in dados:
    parser.parse(palavra)
