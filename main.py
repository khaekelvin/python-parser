import re

# Define keywords and operators
KEYWORDS = {"INT", "PRINT"}
OPERATORS = {"+", "-", "*", "/"}

# Define a class to represent tokens
class Token:
  def __init__(self, type, value, line_number):
    self.type = type
    self.value = value
    self.line_number = line_number

# Function to tokenize the input program
def tokenize(filename):
  tokens = []
  line_number = 1
  try:
    with open(filename, "r") as file:
      for line in file:
        # Strip leading/trailing whitespace and split
        words = line.strip().split()
        for word in words:
          if word in KEYWORDS:
            tokens.append(Token("KEYWORD", word, line_number))
          elif word in OPERATORS:
            tokens.append(Token("OPERATOR", word, line_number))
          elif word.isdigit():
            tokens.append(Token("INT", int(word), line_number))
          else:
            # Error: Invalid token
            return None, f"ERROR at Line {line_number}: Invalid token '{word}'"
          # Print token details for debugging (optional)
          # print(f"Line {line_number}: {word} - {token.type} ({token.value})")
        line_number += 1
  except FileNotFoundError:
    return None, f"Error: File '{filename}' not found."
  return tokens, None

# Function to parse the token list
def parse(tokens):
  errors = []
  # Check for program structure (INT, PRINT statements)
  for i, token in enumerate(tokens):
    if i == 0 and token.type != "INT":
      errors.append(f"ERROR at Line {token.line_number}: Program must start with an INT declaration.")
    elif i % 2 == 0 and token.type != "KEYWORD":
      errors.append(f"ERROR at Line {line_number}: Expected keyword after INT declaration.")
    elif i % 2 == 1 and token.type != "OPERATOR" and token.type != "INT":
      errors.append(f"ERROR at Line {line_number}: Expected expression after keyword.")
  if errors:
    return None, errors

  return True, None

# Specify the input file name
filename = "program.txt"  # Replace with your actual file name

# Tokenize and parse the program
tokens, error = tokenize(filename)
if error:
  print(error)
else:
  success, errors = parse(tokens)
  if success:
    print("Syntax analysis performed successfully and no errors were found.")
  else:
    for error in errors:
      print(error)
