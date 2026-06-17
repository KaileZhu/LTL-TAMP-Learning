# 最初始的文件，简单的词法分析器，用于将输入字符串分解为特定的令牌，并识别一些常见的字符和操作符。
import ply.lex as lex

# 要识别的令牌类别
tokens = (
        "SYMBOL",
        "AND",
        "OR",
        "NOT",
        "TRUE",
        "LPAREN",
        "RPAREN")

t_SYMBOL = r"[a-z]+[a-z0-9_]*"  # 匹配1 or 多个小写字母，后面跟0 or 多个小写字母数学下划线
t_TRUE   = r"1"  # 1 布尔值true
t_AND    = r"&&"  # && 逻辑”与“操作符
t_OR     = r"\|\|"  # || 表示逻辑”或“操作符
t_NOT    = r"!"  # ! 表示逻辑”非“操作符
t_LPAREN = r"\("  # （ 匹配左括号
t_RPAREN = r"\)"  # ) 匹配右括号
t_ignore = " "  # 空格

def t_error(t):
    """遇到非法字符，打印错误信息"""
    print("Illegal character '%s'" % t.value[0])

def get_lexer():
    #  返回已经初始化的此法分析器对象
    return lex.lex()
