import re

class PrePro:
    @staticmethod
    def filter(code):
        code = re.sub(r"//.*", "", code)
        lines = code.split("\n")
        if re.search(r"\d\s+\d", code):
            raise Exception("Two numbers can't be separeted only by a space")
        code = "\n".join([line.lstrip("\t") for line in lines])
        return code
