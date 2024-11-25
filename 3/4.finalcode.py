import os
import numpy as np
import faiss
from llama_index.embeddings.dashscope import (
    DashScopeEmbedding,
    DashScopeTextEmbeddingModels,
    DashScopeTextEmbeddingType,
)
from llama_index.vector_stores.faiss import FaissVectorStore
from dashscope import Generation

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

# 存储文本数据对应的原始内容
text_data = []

# 逐行读取文件并进行向量化处理
with open(file_path, 'r', encoding='utf-8') as file:
    batch = []  # 用于存储当前批次的文本数据

    for line_number, line in enumerate(file, 1):
        batch.append(line.strip())  # 去掉每行末尾的换行符

        if len(batch) == batch_size:
            # 向量化当前批次的文本
            result_embeddings = embedder.get_text_embedding_batch(batch)

            for i, (line, embedding) in enumerate(zip(batch, result_embeddings)):
                if embedding is not None:
                    # 将向量添加到 FAISS 索引
                    embedding_array = np.array(embedding, dtype='float32').reshape(1, -1)
                    faiss_index.add(embedding_array)

                    # 保存原始文本数据
                    text_data.append(line)

            batch = []  # 清空批次，准备下一个

    # 处理最后剩下的行
    if batch:
        result_embeddings = embedder.get_text_embedding_batch(batch)

        for i, (line, embedding) in enumerate(zip(batch, result_embeddings)):
            if embedding is not None:
                # 将向量添加到 FAISS 索引
                embedding_array = np.array(embedding, dtype='float32').reshape(1, -1)
                faiss_index.add(embedding_array)

                # 保存原始文本数据
                text_data.append(line)

# 将 faiss 索引保存到本地文件
index_file = 'index_file.index'
faiss.write_index(faiss_index, index_file)

print(f"FAISS index 已保存到文件: {index_file}")

# 存储对话历史
messages = [
    {'role': 'system',
     'content': 'You are a helpful assistant. Please answer only based on the shoe store knowledge base.'}
]


def get_response(user_input):
    # 向消息列表添加用户输入
    messages.append({'role': 'user', 'content': user_input})

    # 检查用户是否希望结束对话
    if "再见" in user_input or "结束" in user_input or "拜拜" in user_input:
        return "感谢您的咨询，再见"

    # 1. 将用户输入转化为向量
    user_embedding = embedder.get_text_embedding(user_input)

    # 2. 在 FAISS 索引中进行查询，获取最相似的文本
    if user_embedding is not None:
        user_embedding_array = np.array(user_embedding, dtype='float32').reshape(1, -1)
        D, I = faiss_index.search(user_embedding_array, k=3)  # 获取最相似的 3 个文本

        # 输出最相似的文本内容
        top_results = [text_data[i] for i in I[0]]
        print(f"找到最相似的文本：")
        for result in top_results:
            print(result)

        # 将最相似的文本作为 context 来更新对话
        messages.append({'role': 'system', 'content': 'Below are the most relevant responses to the user input.'})
        for result in top_results:
            messages.append({'role': 'system', 'content': result})

        # 3. 调用私域的 API 获取响应，启用流式输出
        responses = Generation.call(
            api_key=os.getenv('PRIVATE_API_KEY'),  # 使用私域 API 密钥
            model="qwen-plus",
            messages=messages,
            result_format="message",
            stream=True,  # 启用流式输出
            incremental_output=True  # 启用增量式流式输出
        )

        assistant_reply = ""
        print("流式输出内容为：")
        for response in responses:
            chunk_content = response.output.choices[0].message.content
            assistant_reply += chunk_content
            print(chunk_content, end='', flush=True)

        # 更新对话历史
        messages.append({'role': 'assistant', 'content': assistant_reply})

        return assistant_reply

    return "抱歉，无法理解您的问题，请确保问题与鞋店知识库相关。"


# 示例交互
while True:
    user_input = input("用户: ")

    # 获取 AI 回复
    reply = get_response(user_input)

    # 输出 AI 回复
    print(f"助手: {reply}")

    # 如果对话结束，退出循环
    if "感谢您的咨询，再见" in reply:
        break
