class Tokenizer:
    def __init__(self):
        pass

    def tokenize(self, text):
        self.text = text
        self.new_text = ""
        self.alphab = """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,?!&;"""
        self.num = "1234567890"
        for tok in self.text:
            if tok not in self.alphab and tok not in self.alphab.upper() and tok not in self.num and tok != " ":
                tok = ""
            self.new_text += tok
        self.new_text = self.new_text.split()
        return self.new_text
