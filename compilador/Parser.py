from Tokenizer import *
from PrePro import *
from SymbolTable import SymbolTable
import Node
from Asm import *

class Parser:

    def parse_expression(self):
        left = self.parse_term()
        while self.tokenizer.next.type == "PLUS" or self.tokenizer.next.type == "MINUS" or self.tokenizer.next.type == "DOT":
            op = self.tokenizer.next.type
            self.tokenizer.selectNext()
            right = self.parse_term()
            left = Node.BinOp(op, [left, right])
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.tokenizer.next.type == "MULT" or self.tokenizer.next.type == "DIV":
            op = self.tokenizer.next.type
            self.tokenizer.selectNext()
            right = self.parse_factor()
            left = Node.BinOp(op, [left, right])
        return left

    def parse_factor(self):
        result = None
        if self.tokenizer.next.type == "INT":
            value = self.tokenizer.next.value
            result = Node.IntVal(value, [])
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "INT" or self.tokenizer.next.type == "STRING" or self.tokenizer.next.type == "ID":
                raise Exception("Invalid token")
        elif self.tokenizer.next.type == "STRING":
            value = self.tokenizer.next.value
            result = Node.StringVal(value, [])
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "STRING":
                raise Exception("Invalid token")
        elif self.tokenizer.next.type == "ID":
            identifier = self.tokenizer.next.value
            result = Node.Identifier(identifier, [])
            self.tokenizer.selectNext()
        elif self.tokenizer.next.type == "PLUS" or self.tokenizer.next.type == "MINUS" or self.tokenizer.next.type == "NOT":
            op = self.tokenizer.next.type
            self.tokenizer.selectNext()
            operation = self.parse_factor()
            result = Node.UnOp(op, [operation])
        elif self.tokenizer.next.type == "OPENP":
            self.tokenizer.selectNext()
            result = self.parse_boolExpr()
            if self.tokenizer.next.type != "CLOSEP":
                raise Exception("Invalid token")
            self.tokenizer.selectNext()
        elif self.tokenizer.next.type == "SCAN":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "OPENP":
                self.tokenizer.selectNext()
                result = Node.Scan("SCAN", [])
                if self.tokenizer.next.type != "CLOSEP":
                    raise Exception("Invalid token")
                self.tokenizer.selectNext()
            else:
                raise Exception("Invalid token")
        elif self.tokenizer.next.type == "EOF":
            pass
        else:
            raise Exception("Invalid token")

        return result


    def parse_statement(self):
        result = 0
        if self.tokenizer.next.type == "PRINT":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "OPENP":
                self.tokenizer.selectNext()
                print_result = self.parse_boolExpr()
                result = Node.Print("print", [print_result])
                if self.tokenizer.next.type != "CLOSEP":
                    raise Exception("Invalid token")
                self.tokenizer.selectNext()
                if self.tokenizer.next.type != "EOF" and self.tokenizer.next.type != "NEWLINE":
                    raise Exception("Invalid token")
                self.tokenizer.selectNext()
            else:
                raise Exception("Invalid token")
        elif self.tokenizer.next.type == "IF":
            self.tokenizer.selectNext()
            condition = self.parse_boolExpr()
            block = self.parse_block()
            if self.tokenizer.next.type == "ELSE":
                self.tokenizer.selectNext()
                else_block = self.parse_block()
                result = Node.IfElse("ifelse", [condition, block, else_block])
                if self.tokenizer.next.type == "NEWLINE":
                    self.tokenizer.selectNext()
            else:
                result = Node.If("if", [condition, block])
                self.tokenizer.selectNext()
        elif self.tokenizer.next.type == "FOR":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "ID":
                identifier = self.tokenizer.next.value
                result = Node.Identifier(identifier, [])
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "EQUAL":
                    self.tokenizer.selectNext()
                    initial_value = Node.Assign("EQUAL", [result, self.parse_boolExpr()])
                    if self.tokenizer.next.type == "SEMICOLON":
                        self.tokenizer.selectNext()
                        condition = self.parse_boolExpr()
                        if self.tokenizer.next.type == "SEMICOLON":
                            self.tokenizer.selectNext()
                            if self.tokenizer.next.type == "ID":
                                identifier = self.tokenizer.next.value
                                result = Node.Identifier(identifier, [])
                                self.tokenizer.selectNext()
                                if self.tokenizer.next.type == "EQUAL":
                                    self.tokenizer.selectNext()
                                    final_value = Node.Assign("EQUAL", [result, self.parse_boolExpr()])
                                    block = self.parse_block()
                                    result = Node.ForLoop("for", [initial_value, condition, block, final_value])
                                    if self.tokenizer.next.type == "NEWLINE" and self.tokenizer.next.type == "EOF":
                                        self.tokenizer.selectNext()
                                    if self.tokenizer.next.type == "NEWLINE":
                                        self.tokenizer.selectNext()
                                    else:
                                        raise Exception("Invalid token")
                                else:
                                    raise Exception("Invalid token")
                            else:
                                raise Exception("Invalid token")
                        else:
                            raise Exception("Invalid token")
                    else:
                        raise Exception("Invalid token")
                else:
                    raise Exception("Invalid token")
        elif self.tokenizer.next.type == "VAR":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "ID":
                name = self.tokenizer.next.value
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "INT" or self.tokenizer.next.type == "STRING":
                    vartype = self.tokenizer.next.type
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "NEWLINE":
                        result = Node.VarDec(vartype, [name])
                        self.tokenizer.selectNext()
                    elif self.tokenizer.next.type == "EQUAL":
                        self.tokenizer.selectNext()
                        result = Node.VarDec(vartype, [name, self.parse_boolExpr()])
                    else:
                        raise Exception("Invalid token")
        elif self.tokenizer.next.type == "ID":
              name = self.tokenizer.next.value
              result = Node.Identifier(name, [])
              self.tokenizer.selectNext()
              if self.tokenizer.next.type == "EQUAL":
                  self.tokenizer.selectNext()
                  result = Node.Assign("EQUAL", [result, self.parse_boolExpr()])
                  self.tokenizer.selectNext()
              elif self.tokenizer.next.type == "EQUALITY" or self.tokenizer.next.type == "GREATER" or self.tokenizer.next.type == "LESS":
                  self.tokenizer.selectNext()
                  result = Node.Assign("EQUAL", [result, self.parse_boolExpr()])
                  self.tokenizer.selectNext()
              else:
                  raise Exception("Invalid token")
        elif self.tokenizer.next.type == "NEWLINE":
            self.tokenizer.selectNext()
            result = Node.NoOp("NoOp", [])
        else:
            raise Exception("Invalid token")
        return result

    def parse_program(self):
        result = []
        while self.tokenizer.next.type != "EOF":
            result.append(self.parse_statement())
        return result


    def parse_block(self):
        results = []
        if self.tokenizer.next.type == "OPENB":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "NEWLINE":
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "CLOSEB":
                    node = Node.NoOp("NoOp", [])
                else:
                    node = self.parse_statement()
                results.append(node)
                result = Node.Block("block", results)
            else:
                raise Exception("Invalid token")
            if self.tokenizer.next.type == "CLOSEB":
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "ID":
                    raise Exception("Invalid token")
                return result
            else:
                raise Exception("Invalid token")
        else:
            raise Exception("Invalid token")

    def relExpr(self):
        left = self.parse_expression()
        if self.tokenizer.next.type == "EQUALITY" or self.tokenizer.next.type == "GREATER" or self.tokenizer.next.type == "LESS":
            op = self.tokenizer.next.type
            self.tokenizer.selectNext()
            right = self.parse_expression()
            left = Node.BinOp(op, [left, right])
        return left

    def parse_boolTerm(self):
        left = self.relExpr()
        while self.tokenizer.next.type == "AND":
            op = self.tokenizer.next.type
            self.tokenizer.selectNext()
            right = self.relExpr()
            left = Node.BinOp(op, [left, right])
        return left

    def parse_boolExpr(self):
        left = self.parse_boolTerm()
        while self.tokenizer.next.type == "OR":
            op = self.tokenizer.next.type
            self.tokenizer.selectNext()
            right = self.parse_boolTerm()
            left = Node.BinOp(op, [left, right])
        return left

    def run(self, code):
        parentheses = 0
        self.tokenizer = Tokenizer(PrePro.filter(code))
        self.tokenizer.selectNext()

        tokenizer = Tokenizer(PrePro.filter(code))

        while tokenizer.next.type != "EOF":
            if tokenizer.next.type == "OPENP":
                parentheses += 1
            if tokenizer.next.type == "CLOSEP":
                parentheses -= 1
            tokenizer.selectNext()
        if parentheses != 0:
            raise Exception("Parentheses not closed")

        return self.parse_program()
