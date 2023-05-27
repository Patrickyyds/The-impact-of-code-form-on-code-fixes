import tokenize

source_code = '''
def add(a, b):
    return a + b
'''

tokens = tokenize.generate_tokens(source_code.splitlines(True).__iter__().__next__)
for token in tokens:
    print(token)