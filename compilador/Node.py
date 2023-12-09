from abc import ABC
from SymbolTable import SymbolTable

class Node(ABC):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    i = 0

    @staticmethod
    def new_id():
        Node.i += 1
        return Node.i

    def evaluate(self, symbol_table: SymbolTable, asm_code):
        pass

class BinOp(Node):
    def evaluate(self, symbol_table: SymbolTable, asm_code):
        right_result = self.children[1].evaluate(symbol_table, asm_code)
        asm_code.write(f"MOV EAX, {right_result[0]}")
        asm_code.write("PUSH EAX")
        left_result = self.children[0].evaluate(symbol_table, asm_code)
        asm_code.write(f"MOV EAX, {left_result[0]}")
        asm_code.write("POP EBX")

        if self.value == "DOT":
            result = (str(left_result[0]) + str(right_result[0]), "STRING", "")

        elif left_result[1] == right_result[1]:
            if self.value == "PLUS":
                asm_code.write("ADD EAX, EBX")
                result = (left_result[0] + right_result[0], "INT", "")
            elif self.value == "MINUS":
                asm_code.write("SUB EAX, EBX")
                result = (left_result[0] - right_result[0], "INT", "")
            elif self.value == "MULT":
                asm_code.write("IMUL EBX")
                result = (left_result[0] * right_result[0], "INT", "")
            elif self.value == "DIV":
                if right_result[0] == 0:
                    raise ZeroDivisionError("Division by zero")
                asm_code.write("IDIV EBX")
                result = (left_result[0] // right_result[0], "INT", "")
            elif self.value == "EQUALITY":
                asm_code.write("CMP EAX, EBX")
                asm_code.write("CALL binop_je")
                if left_result[0] == right_result[0]:
                    result = (1, "INT", "")
                else:
                    result = (0, "INT", "")
            elif self.value == "AND":
                asm_code.write("AND EAX, EBX")
                if left_result[0] and right_result[0]:
                    result = (1, "INT", "")
                else:
                    result = (0, "INT", "")
            elif self.value == "OR":
                asm_code.write("OR EAX, EBX")
                if left_result[0] or right_result[0]:
                    result = (1, "INT", "")
                else:
                    result = (0, "INT", "")
            elif self.value == "GREATER":
                asm_code.write("CMP EAX, EBX")
                asm_code.write("CALL binop_jg")
                if left_result[0] > right_result[0]:
                    result = (1, "INT", "")
                else:
                    result = (0, "INT", "")
            elif self.value == "LESS":
                asm_code.write("CMP EAX, EBX")
                asm_code.write("CALL binop_jl")
                if left_result[0] < right_result[0]:
                    result = (1, "INT", "")
                else:
                    result = (0, "INT", "")
        else:
            raise Exception("Invalid operator")
        return result

class UnOp(Node):
    def evaluate(self, symbol_table: SymbolTable, asm_code):
        child_result = self.children[0].evaluate(symbol_table, asm_code)
        if child_result[1] != "INT":
            raise Exception("Type mismatch")

        if self.value == "PLUS":
            return (child_result[0], "INT", "")
        elif self.value == "MINUS":
            return (-child_result[0], "INT", "")
        elif self.value == "NOT":
            return (not child_result[0], "INT", "")
        else:
            raise Exception("Invalid operator")

class IntVal(Node):
    def evaluate(self, symbol_table: SymbolTable, asm_code):
        asm_code.write(f"MOV EAX, {self.value}")
        return (self.value, "INT", "")

class StringVal(Node):
    def evaluate(self, symbol_table: SymbolTable, asm_code):
        return (self.value, "STRING", "")

class NoOp(Node):
    def evaluate(self, symbol_table: SymbolTable, asm_code):
        pass


class Assign(Node):
    def evaluate(self, symbol_table: SymbolTable, asm_code):
        asm_code.write(
            f"MOV [EBP-{symbol_table.getter(self.children[0].value)[2]}], EAX")
        symbol_table.setter(self.children[0].value, self.children[1].evaluate(symbol_table, asm_code)[0])

class Block(Node):
    def evaluate(self, symbol_table: SymbolTable, asm_code):
        for child in self.children:
            child.evaluate(symbol_table, asm_code)


class Print(Node):
     def evaluate(self, symbol_table: SymbolTable, asm_code):
        self.children[0].evaluate(symbol_table, asm_code)
        asm_code.write("PUSH EAX")
        asm_code.write("PUSH formatout")
        asm_code.write("call printf")
        asm_code.write("ADD ESP, 8")


class Identifier(Node):
    def evaluate(self, symbol_table: SymbolTable, asm_code):
        asm_code.write(f"MOV EAX, [EBP-{symbol_table.getter(self.value)[2]}]")
        return symbol_table.getter(self.value)


class ForLoop(Node):
    def evaluate(self, symbol_table: SymbolTable, asm_code):
        current_i = Node.new_id()
        loop_start_label = f"LOOP_{current_i}"
        exit_label = f"EXIT_{current_i}"

        self.children[0].evaluate(symbol_table, asm_code)
        asm_code.write(f"{loop_start_label}:")
        condition_temp = Node.new_id()
        self.children[1].evaluate(symbol_table, asm_code)
        asm_code.write(f"MOV [EBP-{condition_temp}], EBX")
        asm_code.write(f"CMP DWORD [EBP-{condition_temp}], 5")
        asm_code.write(f"JE {exit_label}")
        self.children[3].evaluate(symbol_table, asm_code)
        self.children[2].evaluate(symbol_table, asm_code)
        asm_code.write(f"JMP {loop_start_label}")
        asm_code.write(f"{exit_label}:")


class If(Node):
    def evaluate(self, symbol_table: SymbolTable, asm_code):
        current_i = Node.new_id()
        asm_code.write(f"IF_{current_i}:")
        self.children[0].evaluate(symbol_table, asm_code)
        asm_code.write("CMP EAX, False")
        asm_code.write(f"JE ELSE_{current_i}")
        self.children[1].evaluate(symbol_table, asm_code)
        asm_code.write(f"JMP END_IF_{current_i}")
        asm_code.write(f"ELSE_{current_i}:")
        asm_code.write(f"END_IF_{current_i}:")


class IfElse(Node):
    def evaluate(self, symbol_table: SymbolTable, asm_code):
        current_i = Node.new_id()
        asm_code.write(f"IF_{current_i}:")
        self.children[0].evaluate(symbol_table, asm_code)
        asm_code.write("CMP EAX, False")
        asm_code.write(f"JE ELSE_{current_i}")
        self.children[1].evaluate(symbol_table, asm_code)
        asm_code.write(f"JMP END_IF_{current_i}")
        asm_code.write(f"ELSE_{current_i}:")
        self.children[2].evaluate(symbol_table, asm_code)
        asm_code.write(f"END_IF_{current_i}:")

class Scan(Node):
    def evaluate(self, symbol_table: SymbolTable, asm_code):
        scanint = int(input())
        asm_code.write(f"PUSH {scanint}")
        asm_code.write("PUSH formatin")
        asm_code.write("call scanf")
        asm_code.write("ADD ESP, 8")
        asm_code.write(f"MOV EAX, DWORD [ {scanint} ]")
        return (scanint, "INT", "")

class VarDec(Node):
    def evaluate(self, symbol_table: SymbolTable, asm_code):
        asm_code.write("PUSH DWORD 0")
        symbol_table.create(self.children[0], self.value)
        if len(self.children) > 1:
            symbol_table.setter(self.children[0], self.children[1].evaluate(symbol_table, asm_code)[0])
