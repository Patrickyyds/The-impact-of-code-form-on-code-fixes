from gensim.models import Word2Vec
import ast


# 读取代码文件并转换为AST树
def read_file(file_path):
    with open(file_path, 'r') as f:
        code = ast.parse(f.read())
    return code


# 提取AST中的标识符
def extract_identifiers(node):
    if isinstance(node, ast.Name):
        return [node.id]
    else:
        return sum([extract_identifiers(n) for n in ast.iter_child_nodes(node)], [])


# 构建标识符序列并存储到磁盘上
def build_identifier_sequences(root_node, file_path):
    identifiers = extract_identifiers(root_node)
    with open(file_path, 'w') as f:
        for item in identifiers:
            f.write("%s\n" % item)


# 训练Word2Vec模型并返回训练后的KeyedVectors对象
def train_word2vec(file_path):
    sentences = Word2Vec.Text8Corpus(file_path)
    model = Word2Vec(sentences, size=30, window=5, min_count=1, workers=4)
    return model.wv


def get_embedding(identifier, wv):
    try:
        return wv[identifier]
    except KeyError:
        return None


def get_embedding_vector(root_node):
    build_identifier_sequences(root_node, 'identifiers.txt')
    # 训练Word2Vec模型并获取训练后的KeyedVectors对象
    wv = train_word2vec('identifiers.txt')
    # 获取标识符的嵌入向量
    embedding = get_embedding('identifier', wv)
    return embedding
