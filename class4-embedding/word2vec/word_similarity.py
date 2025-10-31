# -*-coding: utf-8 -*-
# 先运行 word_seg进行中文分词，然后再进行word_similarity计算
# 将Word转换成Vec，然后计算相似度 
from gensim.models import word2vec
import multiprocessing
import os

print("=" * 60)
print("Word2Vec 模型训练与相似度计算 (三国演义)")
print("=" * 60)

# 如果目录中有多个文件，可以使用PathLineSentences
segment_folder = './three_kingdoms/segment'
print(f"从目录 {segment_folder} 加载训练数据...")

# 切分之后的句子合集
sentences = word2vec.PathLineSentences(segment_folder)

print("\n训练第一个模型 (vector_size=100, window=3, min_count=1):")
print("-" * 40)

# 设置模型参数，进行训练
model = word2vec.Word2Vec(sentences, vector_size=100, window=3, min_count=1)

# 计算词语相似度
print("词语相似度计算结果:")
try:
    liu_guan_similarity = model.wv.similarity('刘备', '关羽')
    print(f"'刘备' 与 '关羽' 的相似度: {liu_guan_similarity:.4f}")
except KeyError as e:
    print(f"词语 {e} 在词汇表中未找到")

try:
    cao_cao_mengde = model.wv.similarity('曹操', '曹孟德')
    print(f"'曹操' 与 '曹孟德' 的相似度: {cao_cao_mengde:.4f}")
except KeyError as e:
    print(f"词语 {e} 在词汇表中未找到")

print("\n最相似词语计算结果:")
try:
    similar_words = model.wv.most_similar(positive=['刘备', '关羽'], negative=['曹操'], topn=5)
    print("基于向量运算 '刘备' + '关羽' - '曹操' 的最相似词语:")
    for word, similarity in similar_words:
        print(f"  - {word}: {similarity:.4f}")
except KeyError as e:
    print(f"词语 {e} 在词汇表中未找到")

print("\n训练第二个模型 (vector_size=128, window=5, min_count=5):")
print("-" * 40)

# 重新训练模型（因为sentences生成器只能遍历一次）
sentences = word2vec.PathLineSentences(segment_folder)
model2 = word2vec.Word2Vec(sentences, vector_size=128, window=5, min_count=5, workers=multiprocessing.cpu_count())

print(f"模型词汇表大小: {len(model2.wv.key_to_index)} 个词语")

# 确保模型目录存在
os.makedirs('./models', exist_ok=True)

# 保存模型
model2.save('./models/word2Vec.model')

# 保存词向量
model2.wv.save_word2vec_format('./models/word2Vec.bin', binary=True)
print(f"\n模型已保存到 './models/word2Vec.model'")
print(f"词向量已保存到 './models/word2Vec.bin'")

# 显示模型信息
print(f"\n模型参数信息:")
print(f"- 向量维度: {model2.wv.vector_size}")
print(f"- 窗口大小: {model2.window}")
print(f"- 最小词频: {model2.min_count}")
print(f"- 训练轮数: {model2.epochs}")
print(f"- 词汇表大小: {len(model2.wv.key_to_index)} 个词语")

print("\n第二个模型的词语相似度计算结果:")
try:
    liu_guan_similarity_2 = model2.wv.similarity('刘备', '关羽')
    print(f"'刘备' 与 '关羽' 的相似度: {liu_guan_similarity_2:.4f}")
except KeyError as e:
    print(f"词语 {e} 在词汇表中未找到")

try:
    cao_cao_mengde_2 = model2.wv.similarity('曹操', '曹孟德')
    print(f"'曹操' 与 '曹孟德' 的相似度: {cao_cao_mengde_2:.4f}")
except KeyError as e:
    print(f"词语 {e} 在词汇表中未找到")

print("\n第二个模型的最相似词语计算结果:")
try:
    similar_words_2 = model2.wv.most_similar(positive=['刘备', '关羽'], negative=['曹操'], topn=5)
    print("基于向量运算 '刘备' + '关羽' - '曹操' 的最相似词语:")
    for word, similarity in similar_words_2:
        print(f"  - {word}: {similarity:.4f}")
except KeyError as e:
    print(f"词语 {e} 在词汇表中未找到")

print("\n" + "=" * 60)
print("相似度计算完成")
print("=" * 60)

# 额外的相似度计算示例
print("\n其他词语相似度示例 (三国演义):")
test_pairs = [
    ('刘备', '刘玄德'),
    ('诸葛亮', '孔明'),
    ('赵云', '赵子龙'),
    ('张飞', '张翼德'),
    ('孙权', '孙仲谋'),
    ('周瑜', '周公瑾'),
    ('司马懿', '司马仲达')
]

for word1, word2 in test_pairs:
    try:
        similarity = model2.wv.similarity(word1, word2)
        print(f"'{word1}' 与 '{word2}' 的相似度: {similarity:.4f}")
    except KeyError as e:
        print(f"词语 {e} 在词汇表中未找到，无法计算 '{word1}' 与 '{word2}' 的相似度")

# 查找与特定词语最相似的词语列表
print(f"\n与 '诸葛亮' 最相似的10个词语:")
try:
    most_similar = model2.wv.most_similar('诸葛亮', topn=10)
    for i, (word, similarity) in enumerate(most_similar, 1):
        print(f"{i:2d}. {word}: {similarity:.4f}")
except KeyError:
    print("词语 '诸葛亮' 在词汇表中未找到")