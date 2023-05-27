import sys
import os
import re
import codecs

from tokenization import tokenize


def tokenize_training_camel_underscore(input_file, output_file):
    fp = codecs.open(input_file, 'r', 'utf-8')
    wp = codecs.open(output_file, 'w', 'utf-8')
    for i, l in enumerate(fp.readlines()):
        rem_ctx, add = l.split('\t')
        rem, ctx = rem_ctx.split('<CTX>')
        rem, ctx, add = rem.strip(), ctx.strip(), add.strip()

        rem = ' '.join(tokenize(rem))
        ctx = ' '.join(tokenize(ctx))
        add = ' '.join(tokenize(add))
        wp.write(rem + ' <CTX> ' + ctx + '\t' + add + '\n')
    fp.close()
    wp.close()


if __name__ == '__main__':
    tokenize_training_camel_underscore(
        input_file='training_src.txt',
        output_file='training_token.txt'
    )
    tokenize_training_camel_underscore(
        input_file='validation_src.txt',
        output_file='validation_token.txt'
    )

