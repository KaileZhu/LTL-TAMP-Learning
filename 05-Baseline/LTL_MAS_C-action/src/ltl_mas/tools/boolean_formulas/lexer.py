import ply.lex as lex
#这实际上是一个编译器，把正则化符号转换为tokens
tokens = (
        "SYMBOL",
        "AND", "OR",
        "NOT",
        "TRUE",
          "LPAREN", "RPAREN")

t_SYMBOL = r"[a-z]+[a-z0-9_]*"
t_TRUE   = r"1"
t_AND    = r"&&"
t_OR     = r"\|\|"
t_NOT    = r"!"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_ignore = " "

def t_error(t):
    print('Illegal character',t.value[0])

def get_lexer():
    return lex.lex()
