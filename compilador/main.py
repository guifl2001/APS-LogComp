import sys
from Parser import *
from SymbolTable import *

with open(sys.argv[1], 'r') as f:
    input = f.read()


def main():
    AST = Parser().run(input)
    symbol_table = SymbolTable()
    asm_code = Asm(code="", filename=sys.argv[1])
    for node in AST:
        node.evaluate(symbol_table, asm_code)
    asm_code.generate()

if __name__ == "__main__":
    main()
