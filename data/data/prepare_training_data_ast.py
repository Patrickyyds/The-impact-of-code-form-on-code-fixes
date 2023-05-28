import ast
import sys
import os
import re
import codecs


def to_ast_node(code):
    tree = ast.parse(code)
    return ast.dump(tree)


def ast_training_camel_underscore(input_file, output_file):
    fp = codecs.open(input_file, 'r', 'utf-8')
    wp = codecs.open(output_file, 'wb')
    for i, l in enumerate(fp.readlines()):
        rem, ctx = l.split('<CTX>')
        rem, ctx = rem.strip(), ctx.strip()

        rem = ' '.join(to_ast_node(rem))
        ctx = ' '.join(to_ast_node(ctx))

        wp.write(rem + b'<CTX>' + ctx + b'<CTX>' + '\n')
    fp.close()
    wp.close()


def clean_training_bpe(bpe_file):
    fp = codecs.open(bpe_file, 'r', 'utf-8')
    lines = fp.readlines()
    fp.close()
    wp = codecs.open(bpe_file, 'w', 'utf-8')
    for l in lines:
        l = re.sub('@@ 	@@ ', '\t', l)
        l = re.sub('<@@ CT@@ X@@ >', ' <CTX> ', l)
        wp.write(l)
    wp.close()


if __name__ == '__main__':
    ast_training_camel_underscore(
        input_file='training_src.txt',
        output_file='training_ast.txt'
    )
    ast_training_camel_underscore(
        input_file='validation_src.txt',
        output_file='validation_ast.txt'
    )
