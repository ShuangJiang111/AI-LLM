# 导入相关库
from llama_index.embeddings.dashscope import (
    DashScopeEmbedding,
    DashScopeTextEmbeddingModels,
    DashScopeTextEmbeddingType,
)
from llama_index.vector_stores.faiss import FaissVectorStore
import faiss
import numpy as np

# 定义文件路径
file_path = 'D:/code/test code/AILLM_Project/3/运动鞋店铺知识库.txt'

# 批次大小（每次读取的行数）
batch_size = 5

# 创建 DashScopeEmbedding 对象
embedder = DashScopeEmbedding(
    model_name=DashScopeTextEmbeddingModels.TEXT_EMBEDDING_V2,
    text_type=DashScopeTextEmbeddingType.TEXT_TYPE_DOCUMENT,
)

# 创建 faiss 索引
d = 1536  # 向量的维度（根据模型返回的嵌入向量的维度来调整）
faiss_index = faiss.IndexFlatL2(d)

# 使用 FaissVectorStore
vector_store = FaissVectorStore(faiss_index=faiss_index)

# 使用 open() 来逐行读取文件并处理批次
with open(file_path, 'r', encoding='utf-8') as file:
    batch = []  # 用于存储当前批次的文本数据

    for line_number, line in enumerate(file, 1):
        batch.append(line.strip())  # 去掉每行末尾的换行符

        # 当达到批次大小时，处理该批次
        if len(batch) == batch_size:
            print(f"当前批次的行数: {len(batch)}")
            print("正在向量化当前批次的文本...")

            # 调用 DashScopeEmbedding 进行批次向量化
            result_embeddings = embedder.get_text_embedding_batch(batch)

            # 输出每个文本的向量化结果并将向量添加到 FAISS 索引
            for i, (line, embedding) in enumerate(zip(batch, result_embeddings)):
                if embedding is None:  # 如果向量化失败
                    print(f"第{i + 1}行: '{line}' 向量化失败。")
                else:
                    print(f"第{i + 1}行: '{line}' 向量化成功，向量维度: {len(embedding)}")
                    print(f"嵌入向量的前五个值: {embedding[:5]}")

                    # 将向量添加到 FAISS 索引中
                    embedding_array = np.array(embedding, dtype='float32').reshape(1, -1)  # 将嵌入向量转换为合适的形状
                    faiss_index.add(embedding_array)

            batch = []  # 清空批次，准备下一个

    # 处理最后剩下的行
    if batch:
        print(f"当前批次的行数: {len(batch)}")
        print("正在向量化最后一批文本...")

        result_embeddings = embedder.get_text_embedding_batch(batch)

        for i, (line, embedding) in enumerate(zip(batch, result_embeddings)):
            if embedding is None:
                print(f"第{i + 1}行: '{line}' 向量化失败。")
            else:
                print(f"第{i + 1}行: '{line}' 向量化成功，向量维度: {len(embedding)}")
                print(f"嵌入向量的前五个值: {embedding[:5]}")

                # 将向量添加到 FAISS 索引中
                embedding_array = np.array(embedding, dtype='float32').reshape(1, -1)  # 将嵌入向量转换为合适的形状
                faiss_index.add(embedding_array)

# 将 faiss 索引保存到本地文件
index_file = 'index_file.index'  # 指定保存的文件名
faiss.write_index(faiss_index, index_file)

print(f"FAISS index 已保存到文件: {index_file}")