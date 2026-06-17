#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

class Parser(object):
    """解析输入字符串,并生成一个表示图的字典:键是顶点对（起点和终点），值是边的条件"""
    # Expression for the eat_whitespace function
    white_regx  = re.compile(r"\s+")  # 匹配一个或多个空白字符（包括空格、制表符和换行符）
    # Expressions for the input language
    vertex_regx = re.compile(r"(?P<name>\w+_\w+):\s*")  # 匹配一个以字母数字下划线组成的字符串，后面跟着一个冒号和一个或多个空白字符。
    never_regx  = re.compile(r"never \{ /\*(?P<formula>.+)\*/")  # 匹配字符串"never { /"，后面跟着任意数量的任意字符，直到遇到"/"为止
    if_regex    = re.compile(r"if")  # 匹配字符串"if"。这个字符串通常表示一个条件语句的开始
    edge_regex  = re.compile(r":: (?P<cond>\(.*\)) -> goto (?P<dest>\w+_\w+)")  # 匹配表示有向边的字符串
    fi_regex    = re.compile(r"fi;")  # 匹配字符串"fi;"。这个字符串通常表示一个条件语句的结束
    skip_regex  = re.compile(r"skip")  # 匹配字符串"skip"。这个字符串通常表示一个跳过操作。
    end_regex   = re.compile(r"\}")  # 匹配字符串"}"。这个字符串通常表示一个代码块的结束

    def __init__(self, instring):
        self.instring = instring
        self.pos = 0

    def eat_whitespace(self):
        """去除字符串中的空白字符"""
        match = Parser.white_regx.match(self.instring, self.pos)
        while (match != None):
            self.pos += len(match.group(0))
            match = Parser.white_regx.match(self.instring, self.pos)

    def accept(self, expr, strip_whitespace=True):
        """用于匹配输入字符串"""
        if strip_whitespace:
            self.eat_whitespace()  # 保证字符串中没有空白
        match = expr.match(self.instring, self.pos)
        # 匹配输入字符串的位置与正则表达式
        if (match == None):
            return None
        self.pos += len(match.group(0))  # 匹配对象的结束位置加上匹配到的字符串长度，即更新当前位置为匹配结束的位置
        return match.groupdict()  # 返回匹配结果的字典形式

    def parse(self):
        """"解析ltl公式并返回表示边的字典"""
        edges = {}
        self.formula = self.accept(Parser.never_regx)["formula"]
        vertex = self.accept(Parser.vertex_regx)
        while (vertex != None):
            vertex_name = vertex["name"]
            if (self.accept(Parser.if_regex) != None):
                edge = self.accept(Parser.edge_regex)
                while (edge != None):
                    edges[(vertex_name, edge["dest"])] = edge["cond"]
                    edge = self.accept(Parser.edge_regex)
                self.accept(Parser.fi_regex)
            elif (self.accept(Parser.skip_regex) != None):
                # self-loop with "skip"
                edges[(vertex_name, vertex_name)] = '1'
            else:
                raise ParseException("Expected 'if' or 'skip' but got %s" % self.instring[self.pos])
            vertex = self.accept(Parser.vertex_regx)
        self.accept(Parser.end_regex)
        self.eat_whitespace()
        if (self.pos != len(self.instring)):
            raise ParseException("Input not fully parsed. Remainder: %s" % self.instring[self.pos:])
        return edges

class ParseException(Exception):
    pass

def parse(promela):
    parser = Parser(promela)
    return parser.parse()

def find_states(edges):
    states = set()
    initial = set()
    accept = set()
    for (f,t) in edges.keys():
        states.add(f)
        states.add(t)
    for state in states:
        if state.startswith("accept"):
            accept.add(state)
        if state.endswith("init"):
            initial.add(state)
    return (list(states), list(initial), list(accept))

def find_symbols(formula):
    regex = re.compile(r"[a-z]+[a-z0-9]*")
    matches = regex.findall(formula)
    symbols = list()
    for match in matches:
        symbols += [match]
    symbols = list(set(symbols))
    symbols.sort()
    return symbols
