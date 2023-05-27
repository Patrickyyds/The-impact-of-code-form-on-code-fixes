import ast
import codecs

from tokenization import tokenize

# 将 AST 节点转化成 CFG 符号
def to_cfg_node(node):
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Constant):
        return str(node.value)
    elif isinstance(node, ast.Attribute):
        return to_cfg_node(node.value) + '.' + node.attr
    elif isinstance(node, ast.Call):
        args = ','.join([to_cfg_node(arg) for arg in node.args])
        return to_cfg_node(node.func) + '(' + args + ')'
    elif isinstance(node, ast.BinOp):
        left = to_cfg_node(node.left)
        op = to_cfg_node(node.op)
        right = to_cfg_node(node.right)
        return '(' + left + op + right + ')'
    elif isinstance(node, ast.UnaryOp):
        op = to_cfg_node(node.op)
        operand = to_cfg_node(node.operand)
        return op + '(' + operand + ')'
    else:
        return ''


# 将代码段转化成 CFG 形式
def to_cfg(input_file, output_file):
    fp = codecs.open(input_file, 'r', 'utf-8')
    wp = codecs.open(output_file, 'w', 'utf-8')
    for i, l in enumerate(fp.readlines()):
        rem_ctx, add = l.split('\t')
        rem, ctx = rem_ctx.split('<CTX>')
        rem, ctx, add = rem.strip(), ctx.strip(), add.strip()

        rem_tree = ast.parse(rem)
        rem_cfg = ' '.join([to_cfg_node(node) for node in ast.walk(rem_tree)])
        ctx_tree = ast.parse(ctx)
        ctx_cfg = ' '.join([to_cfg_node(node) for node in ast.walk(ctx_tree)])
        add_tree = ast.parse(add)
        add_cfg = ' '.join([to_cfg_node(node) for node in ast.walk(add_tree)])

        wp.write(rem_cfg + ' <CTX> ' + ctx_cfg + '\t' + add_cfg + '\n')

    fp.close()
    wp.close()


if __name__ == '__main__':
    to_cfg(
        input_file='training_src.txt',
        output_file='training_cfg.txt'
    )

    to_cfg(
        input_file='validation_src.txt',
        output_file='validation_cfg.txt'
    )
