class SymbolTable:
    def __init__(self):
        self.table = dict()
        self.position = 0

    def getter(self, identifier):
        return self.table[identifier]

    def create(self, identifier, type):
        if identifier in self.table.keys():
            raise Exception("variable already exists")
        else:
            self.position += 4
            self.table[identifier] = (None, type, self.position)

    def setter(self, identifier, value):
        if identifier not in self.table.keys():
            raise Exception("variable not declared")
        if self.table[identifier][1] == "INT":
          if type(value) == int:
            self.table[identifier] = (value, "INT", self.table[identifier][2])
        elif self.table[identifier][1] == "STRING":
          if type(value) == str:
            self.table[identifier] = (value, "STRING", self.table[identifier][2])
        else:
          raise Exception("Type mismatch")
