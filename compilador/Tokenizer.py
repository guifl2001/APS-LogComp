from SymbolTable import *
from Token import *
import sys
from PrePro import *


class Tokenizer:

    def __init__ (self, source):
        self.source = source
        self.position = 0
        self.next = Token(type(source), source)
        self.commands = {
                                "Println": "PRINT",
                                "Scanln": "SCAN",
                                "if": "IF",
                                "else": "ELSE",
                                "for": "FOR",
                                "var": "VAR",
                                "int": "INT",
                                "string": "STRING",
                                "Guardiola": "PLUS",
                                "Mourinho": "MINUS",
                                "Bellingham": "MULT",
                                "Camavinga": "DIV",
                                "Win": "GREATER",
                                "Loss": "LESS",
                                "Draw": "EQUALITY",
                            }
        self.tokens = {
                            "(": "OPENP",
                            ")": "CLOSEP",
                            "=": "EQUAL",
                            "\n": "NEWLINE",
                            "||": "OR",
                            "&&": "AND",
                            "!": "NOT",
                            ";": "SEMICOLON",
                            "{": "OPENB",
                            "}": "CLOSEB",
                            ".": "DOT",
                        }

    def skipSpaces(self):
        while self.position < len(self.source) and self.source[self.position].isspace() and self.source[self.position] != "\n":
            self.position += 1

    def selectNext(self):
        self.skipSpaces()
        if self.position < len(self.source):
            token = self.source[self.position]
            token2 = self.source[self.position: self.position+2]
            if token == ",":
                raise Exception("Invalid token")
            if token.isdigit():
                number = ""
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    number += self.source[self.position]
                    self.position += 1
                self.next = Token("INT", int(number))
            elif token2 in self.tokens:
                self.next = Token(self.tokens[token2], token2)
                self.position += 2
            elif token in self.tokens:
                self.next = Token(self.tokens[token], token)
                self.position += 1
            elif token == '"':
                string = ""
                self.position += 1
                while self.position < len(self.source) and self.source[self.position] != '"':
                    string += self.source[self.position]
                    self.position += 1
                if self.source[self.position] != '"':
                    raise Exception("String not closed")
                self.position += 1
                self.next = Token("STRING", string)
            else:
                variable = ""
                while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_") and variable not in self.commands:
                    variable += self.source[self.position]
                    self.position += 1
                if variable in self.commands:
                    self.next = Token(self.commands[variable], None)
                else:
                    if variable != "":
                        self.next = Token("ID", variable)
                    else:
                        self.next = Token("EOF", 0)
        else:
            self.next = Token("EOF", 0)


def main():
    parentheses = 0
    if len(sys.argv) != 2:
        print("Uso: python3 tokenizer.py <arquivo>")
        return

    filename = sys.argv[1]

    try:
        with open(filename, "r") as file:
            source = file.read()
            source = PrePro.filter(source)

    except FileNotFoundError:
        print(f"Arquivo '{filename}' não encontrado.")


if __name__ == "__main__":
    main()
