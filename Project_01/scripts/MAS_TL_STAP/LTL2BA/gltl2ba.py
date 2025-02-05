#!/usr/bin/env python3

import re
import sys
import argparse
import __main__

from os.path import abspath, dirname, join
from subprocess import Popen, PIPE

from graphviz import Digraph

from .boolean_formulas.parser import parse_guard

class Ltl2baParser:
    """
    Parser for ltl2ba output
    """
    prog_title = re.compile('^never\s+{\s+/\* (.+?) \*/$')
    prog_node = re.compile('^([^_]+?)_([^_]+?):$')
    prog_edge = re.compile('^\s+:: (.+?) -> goto (.+?)$')
    prog_skip = re.compile('^\s+(?:skip)$')
    prog_ignore = re.compile('(?:^\s+do)|(?:^\s+if)|(?:^\s+od)|'
                            '(?:^\s+fi)|(?:})|(?:^\s+false);?$')

    @staticmethod
    def parse(ltl2ba_output, ignore_title=True):
        graph = Graph()
        nodes = dict()
        edges = dict()
        src_node = None
        for line in ltl2ba_output.split('\n'):
            if Ltl2baParser.is_title(line):
                title = Ltl2baParser.get_title(line)
                if not ignore_title:
                    graph.title(title)
            elif Ltl2baParser.is_node(line):
                name, label, accepting = Ltl2baParser.get_node(line)
                src_node = name
                graph.node(name, label, accepting)
                nodes[name] = [label]
                if accepting: 
                    nodes[name].append('accept')
            elif Ltl2baParser.is_edge(line):
                dst_node, label = Ltl2baParser.get_edge(line)
                assert src_node is not None
                graph.edge(src_node, dst_node, label)
                edges[(src_node, dst_node)] = (label, parse_guard(label))
            elif Ltl2baParser.is_skip(line):
                assert src_node is not None
                graph.edge(src_node, src_node, '(1)')
                edges[(src_node, src_node)] = ('(1)', parse_guard('(1)'))
            elif Ltl2baParser.is_ignore(line):
                pass
            else:
                print("--{}--".format(line))
                raise ValueError("{}: invalid input:\n{}"
                                .format(Ltl2baParser.__name__, line))
        return graph, nodes, edges

    @staticmethod
    def is_title(line):
        return Ltl2baParser.prog_title.match(line) is not None

    @staticmethod
    def get_title(line):
        assert Ltl2baParser.is_title(line)
        return Ltl2baParser.prog_title.search(line).group(1)

    @staticmethod
    def is_node(line):
        return Ltl2baParser.prog_node.match(line) is not None

    @staticmethod
    def get_node(line):
        assert Ltl2baParser.is_node(line)
        prefix, label = Ltl2baParser.prog_node.search(line).groups()
        return (prefix + "_" + label, label, 
                True if prefix == "accept" else False)

    @staticmethod
    def is_edge(line):
        return Ltl2baParser.prog_edge.match(line) is not None

    @staticmethod
    def get_edge(line):
        assert Ltl2baParser.is_edge(line)
        label, dst_node = Ltl2baParser.prog_edge.search(line).groups()
        return (dst_node, label)

    @staticmethod
    def is_skip(line):
        return Ltl2baParser.prog_skip.match(line) is not None

    @staticmethod
    def is_ignore(line):
        return Ltl2baParser.prog_ignore.match(line) is not None


class Graph:
    """
    The graph for the Buchi
    """
    def __init__(self):
        self.dot = Digraph()

    def title(self, str):
        self.dot.graph_attr.update(label=str)

    def node(self, name, label, accepting=False):
        num_peripheries = '2' if accepting else '1'
        self.dot.node(name, label, shape='circle', peripheries=num_peripheries)

    def edge(self, src, dst, label):
        self.dot.edge(src, dst, label)

    def show(self):
        self.dot.render(view=True)

    def save_render(self, path, on_screen):
        self.dot.render(path, view=on_screen)

    def save_dot(self, path):
        self.dot.save(path)

    def __str__(self):
        return str(self.dot)


#=====================
# The core function
#=====================
def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--formula",
                        help="translate LTL into never claim", type=str)
    group.add_argument("-F", "--file",
                        help="like -f, but with the LTL formula stored in a "
                        "1-line file", type=argparse.FileType('r'))
    parser.add_argument("-d",
                        help="display automata (D)escription at each step",
                        action='store_true')
    parser.add_argument("-s",
                        help="computing time and automata sizes (S)tatistics",
                        action='store_true')
    parser.add_argument("-l",
                        help="disable (L)ogic formula simplification",
                        action='store_true')
    parser.add_argument("-p",
                        help="disable a-(P)osteriori simplification",
                        action='store_true')
    parser.add_argument("-o",
                        help="disable (O)n-the-fly simplification",
                        action='store_true')
    parser.add_argument("-c",
                        help="disable strongly (C)onnected components "
                        "simplification", action='store_true')
    parser.add_argument("-a",
                        help="disable trick in (A)ccepting conditions",
                        action='store_true')
    parser.add_argument("-g", "--graph",
                        help="display buchi automaton graph",
                        action='store_true')
    parser.add_argument("-G", "--output-graph",
                        help="save buchi automaton graph in pdf file",
                        type=argparse.FileType('w'))
    parser.add_argument("-t", "--dot",
                        help="print buchi automaton graph in DOT notation",
                        action='store_true')
    parser.add_argument("-T", "--output-dot",
                        help="save buchi automaton graph in DOT file",
                        type=argparse.FileType('w'))
    return parser.parse_args()

def get_ltl_formula(file, formula):
    assert file is not None or formula is not None
    if file:
        try:
            ltl = file.read()
        except Exception as e:
            eprint("{}: {}".format(__main__.__file__, str(e)))
            sys.exit(1)
    else:
        ltl = formula
    ltl = re.sub('\s+', ' ', ltl)
    if len(ltl) == 0 or ltl == ' ':
        eprint("{}: empty ltl formula.".format(__main__.__file__))
        sys.exit(1)
    return ltl

def run_ltl2ba(ltl_formula, args=None, dev='windows', mode='output'):
    script_dir = dirname(abspath(__file__))
    file = 'ltl2ba.exe'
    # file = 'ltl2ba' if dev == 'linux' else 'ltl2ba.exe'
    # 'ltl2ba' for linux and 'ltl2ba.exe' for windows
    ltl2ba = join(script_dir, file)  
    ltl2ba_args = [ltl2ba, "-f", ltl_formula]
    if args:
        ltl2ba_args += list("-{}".format(x) for x in "dslpoca"
                            if getattr(args, x))
    try:
        process = Popen(ltl2ba_args, stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
    except FileNotFoundError as e:
        eprint("{}: ltl2ba not found.\n".format(__main__.__file__))
        eprint("Please download ltl2ba from\n")
        eprint("\thttp://www.lsv.fr/~gastin/ltl2ba/ltl2ba-1.2b1.tar.gz\n")
        eprint("compile the sources and add the binary to your $PATH, e.g.\n")
        eprint("\t~$ export PATH=$PATH:path-to-ltlb2ba-dir\n")
        sys.exit(1)
    output = output.decode('utf-8')
    if mode == 'output':
        return output
    elif mode == 'debug':
        return output, err, exit_code

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def parse_promela(promela):
    prog = re.compile("^[\s\S\w\W]*?"
                    "(never\s+{[\s\S\w\W]+?})"
                    "[\s\S\w\W]+$")
    match = prog.search(promela)
    assert match, promela
    _, nodes, edges = Ltl2baParser.parse(match.group(1))
    return nodes, edges

def find_symbols(formula):
    regex = re.compile(r"[a-z]+[a-z0-9]*")
    matches = regex.findall(formula)
    symbols = list()
    for match in matches:
        symbols += [match]
    symbols = list(set(symbols))
    symbols.sort()
    return symbols


if __name__ == '__main__':
    # the main function
    args = parse_args()
    ltl = get_ltl_formula(args.file, args.formula)
    (output, err, exit_code) = run_ltl2ba(ltl, args=args, mode='debug')
    if exit_code != 1:
        print(output)
        if (args.graph or args.output_graph is not None
                or args.dot or args.output_dot is not None):
            prog = re.compile("^[\s\S\w\W]*?"
                            "(never\s+{[\s\S\w\W]+?})"
                            "[\s\S\w\W]+$")
            match = prog.search(output)
            assert match, output
            graph, _, _ = Ltl2baParser.parse(match.group(1))
            if args.output_graph is not None:
                graph.save_render(args.output_graph.name, args.graph)
                args.output_graph.close()
            elif args.graph:
                graph.show()
            if args.output_dot is not None:
                graph.save_dot(args.output_dot.name)
                args.output_dot.close()
            if args.dot:
                print(graph)
    else:
        eprint("{}: ltl2ba error:".format(__main__.__file__))
        eprint(output)
        sys.exit(exit_code)