import sys
import os
import re
import codecs

IDENTIFIER_DATA_DIR = os.path.abspath(__file__)[: os.path.abspath(__file__).rindex('/') + 1]
sys.path.append(IDENTIFIER_DATA_DIR + '../../src/dataloader/')

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
    tokenize_training_camel_underscore(
        input_file='training_src.txt',
        output_file='training_token.txt'
    )
    tokenize_training_camel_underscore(
        input_file='validation_src.txt',
        output_file='validation_token.txt'
    )
