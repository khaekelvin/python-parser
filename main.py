import re

# Define token regular expressions
TOKEN_REGEX = {
    "floatdcl": r"\bf\b",
    "intdcl": r"\bi\b",
    "print": r"\bp\b",
    "id": r"[a-z]+",  # Adjusted to match entire identifier
    "assign": r"=",
    "plus": r"\+",
    "minus": r"_",
    "inum": r"[0-9]+",
    "fnum": r"[0-9]+\.[0-9]+(?:[eE][-+]?[0-9]+)?",  # Adjusted to correctly match float numbers
}


# Tokenize the input program
def tokenize(program):
    tokens = []
    lines = program.split('\n')
    line_no = 1
    for line in lines:
        line = line.strip()  # remove leading and trailing whitespace
        if line:
            parts = re.split(r'\s+', line)  # split line into tokens based on whitespace
            for part in parts:
                for token_type, regex in TOKEN_REGEX.items():
                    match = re.match(regex, part)
                    if match:
                        if token_type == "id":
                            token_value = match.group().strip()  # strip leading and trailing spaces
                        else:
                            token_value = match.group()
                        tokens.append((token_type, token_value, line_no))
                        break
                else:
                    raise SyntaxError(f"Unexpected token '{part}' on line {line_no}")
        line_no += 1
        print(tokens, "\n")
    return tokens


# Parse the tokens according to the grammar
def parse(tokens):
    try:
        index = 0

        # Helper functions for parsing
        def match(token_type):
            nonlocal index
            if index < len(tokens) and tokens[index][0] == token_type:
                index += 1
                return True
            return False

        def expect(token_type):
            if not match(token_type):
                raise SyntaxError(f"Expected '{token_type}' but found '{tokens[index][0]}' on line {tokens[index][2]}")

        # Grammar rules
        def dcls():
            while match("floatdcl") or match("intdcl"):
                expect("id")

        def stmts():
            while match("id") or match("print"):
                if tokens[index-1][0] == "id" and match("assign"):
                    val()
                    expr()
                elif tokens[index-1][0] == "print":
                    expect("id")

        def expr():
            if match("plus") or match("minus"):
                val()
                expr()

        def val():
            if not match("id") and not match("inum") and not match("fnum"):
                raise SyntaxError("Expected identifier or number")

        # Start parsing
        dcls()
        stmts()

        if index < len(tokens):
            raise SyntaxError(f"Unexpected token '{tokens[index][1]}' on line {tokens[index][2]}")

        print("\n","Syntax analysis performed successfully and no errors were found." , "\n")

    except SyntaxError as e:
        print(f"Syntax error: {e}", "\n")

# Example usage
if __name__ == "__main__":
    file_path = "program.txt"
    try:
        with open(file_path, 'r') as file:
            program = file.read()
        tokens = tokenize(program)
        parse(tokens)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.", "\n")
