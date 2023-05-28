import re

import javalang

COMPOSED_SYMBOLS = ['<<', '>>', '==', '!=', '>=', '<=', '&&', '||', '++', '--', '-=', '+=', '*=', '/=', '%=', '&=',
                    '|=', '^=', '<<=', '>>=', '->', '<-', '::']

PYTHON_SYMBOLS = ['or', 'and']

java_code = '''
public class Example {
    public static void main(String[] args) {
        if (model != null) {
            // code here
        }
    }
}
'''


def extract_strings(string):
    # FIXME Does not work for s.append(',').append(',') return [',', ').append(', ',']
    matches = re.sub(r'"([^"]*)"', " SSSTRINGSS ", string)
    matches = re.sub(r"'([^']*)'", " SSSTRINGSS ", matches)
    return matches


def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    cam_toks = [m.group(0) for m in matches]
    results = []
    for tok in cam_toks:
        results.append(tok)
        results.append('CaMeL')
    if results:
        results.pop()
    return results


def number_split(identifier):
    match = re.findall('\d+|\D+', identifier)
    return match


def remove_integer(tokens):
    for idx, tok in enumerate(tokens):
        if tok.isdigit():
            try:
                if int(tok) > 1:
                    if int(tok) != 8 and int(tok) != 16 and int(tok) != 32 and int(tok) != 64:
                        tokens[idx] = '$NUMBER$'
            except:
                tokens[idx] = tok
    return tokens


def get_strings_numbers(string):
    # FIXME Does not work for s.append(',').append(',') return [',', ').append(', ',']
    matches1 = re.findall(r'(?<=\")(.*?)(?=\")', string)
    matches2 = re.findall(r"(?<=\')(.*?)(?=\')", string)
    strings = matches1 + matches2
    numbers = re.findall(r'\d+', string)
    return strings, numbers


def ast_node(string):
    final_ast_list = []
    string_replaced = extract_strings(string)
    split_ast = re.split(r'([\W_])', string_replaced)
    split_ast = list(filter(lambda a: a not in [' ', '', '"', "'", '\t', '\n'], split_ast))
    flag = False

    tokens = javalang.tokenizer.tokenize(java_code)
    parser = javalang.parser.Parser(tokens)

    ast_tree = parser.parse_member_declaration()
    # Special symbols
    for idx, ast in enumerate(split_ast):
        if idx < len(split_ast) - 1:
            reconstructed_ast = ast + split_ast[idx + 1]
            if reconstructed_ast in COMPOSED_SYMBOLS:
                final_ast_list.append(reconstructed_ast)
                flag = True
            elif not flag:
                final_ast_list.append(ast)
            elif flag:
                flag = False
        else:
            final_ast_list.append(ast)
    # Camel Case
    no_camel = []
    for ast in final_ast_list:
        camel_asts = camel_case_split(ast)
        for idx, camel_tok in enumerate(camel_asts):
            no_camel.append(camel_tok)

    # number split
    asts = []
    for ast in no_camel:
        number_sep = number_split(ast)
        for num in number_sep:
            asts.append(num)
    asts = remove_integer(asts)
    for idx, ast in enumerate(asts):
        if ast == 'SSSTRINGSS':
            if idx > 0 and asts[idx - 1] == '$STRING$':
                return []
            else:
                asts[idx] = '$STRING$'

    return asts


def token2statement(token_list, numbers, strings):
    flag_string_statements = 0
    ### if strings and numbers format of statement is [n1s1, n1s2, n1s3, n2s1, n2,s2, ...]
    if "$STRING$" in token_list and "$NUMBER$" in token_list:
        statements = [""] * len(strings) * len(numbers)
        flag_string_statements = 3
    elif "$NUMBER$" in token_list:
        statements = [""] * len(numbers)
        flag_string_statements = 2
    elif "$STRING$" in token_list:
        statements = [""] * len(strings)
        flag_string_statements = 1
    else:
        statements = [""]
    for i, token in enumerate(token_list):
        if i < len(token_list) - 1:
            # if token_list[i] == "or" or "and":
            #    for s in range(0, len(statements)):
            #        statements[s] += " " + token + " "
            if token_list[i] == "return":
                if token_list[i + 1].isdigit() or token_list[i + 1] == "$NUMBER$":
                    for s in range(0, len(statements)):
                        statements[s] += token + " "
                elif token_list[i + 1] == "CaMeL":
                    for s in range(0, len(statements)):
                        statements[s] += token
                elif token_list[i + 1] == ".":  # no space
                    for s in range(0, len(statements)):
                        statements[s] += token
                elif token_list[i + 1] == "(":  # Actually it does not seem to be needed.
                    for s in range(0, len(statements)):
                        statements[s] += " " + token
                elif token_list[i + 1] == "_":  # no space
                    for s in range(0, len(statements)):
                        statements[s] += token
                else:
                    for s in range(0, len(statements)):
                        statements[s] += token + " "

            elif token_list[i] == "$STRING$":
                if flag_string_statements == 3:
                    for s in range(0, len(statements)):
                        if "'" not in strings[s % len(strings)]:
                            statements[s] += "'" + strings[s % len(strings)] + "'"
                        else:
                            statements[s] += '"' + strings[s % len(strings)] + '"'
                elif flag_string_statements == 1:
                    for s in range(0, len(statements)):
                        if "'" not in strings[s]:
                            statements[s] += "'" + strings[s] + "'"
                        else:
                            statements[s] += '"' + strings[s] + '"'
                else:
                    for s in range(0, len(statements)):
                        statements[s] += "'DEFAULT'"

            elif token_list[i] == "$NUMBER$":
                if flag_string_statements == 3:
                    count = 0
                    # print("len_statemnt", len(statements))
                    for s in range(0, len(numbers)):
                        # print("s: ", len(numbers))
                        # print(len(statements))
                        # print(len(numbers)* len(strings) - 1 )
                        for stringlen in range(s, s + len(strings)):
                            statements[count] += numbers[s]
                            count += 1
                            # print("Count: ", count)

                elif flag_string_statements == 2:
                    for s in range(0, len(statements)):
                        statements[s] += numbers[s]
                else:
                    # use default number 2 (0 and 1 are specific tokens)
                    statements[s] += 2
            elif token_list[i] == "CaMeL":  # no space
                pass
            elif token_list[i] == '*':
                for s in range(0, len(statements)):
                    statements[s] += token
            elif token_list[i] == ".":  # no space
                for s in range(0, len(statements)):
                    statements[s] += token
            elif token_list[i].isdigit():  # no space in general
                if token_list[i + 1] == 'or' or token_list[i + 1] == 'and':
                    for s in range(0, len(statements)):
                        statements[s] += token + ' '
                else:
                    for s in range(0, len(statements)):
                        statements[s] += token

            elif token_list[i] == "_":  # no space
                for s in range(0, len(statements)):
                    statements[s] += token

            else:  # Default case"
                if token_list[i + 1] == "CaMeL":  # no space
                    for s in range(0, len(statements)):
                        statements[s] += token
                elif token_list[i + 1] == ".":  # no space
                    for s in range(0, len(statements)):
                        statements[s] += token
                elif token_list[i + 1] == "(":  # Actually it does not seem to be needed.
                    for s in range(0, len(statements)):
                        statements[s] += token
                elif token_list[i + 1] == "_":  # no space
                    for s in range(0, len(statements)):
                        statements[s] += token
                elif token_list[i + 1].isdigit() or token_list[i + 1] == "$NUMBER$":  # no space
                    if token_list[i + 1] == 'or' or token_list[i + 1] == 'and':
                        for s in range(0, len(statements)):
                            statements[s] += token + " "
                    else:
                        for s in range(0, len(statements)):
                            statements[s] += token
                else:
                    for s in range(0, len(statements)):
                        statements[s] += token + " "
        else:  # no space after the last statement
            for s in range(0, len(statements)):
                statements[s] += token
    return statements

