import os
from openai import OpenAI

# 初始化客户端
client = OpenAI(
    api_key='sk-9fdaf5b5b2814c8380e47b427087618d',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 对话历史
conversation_history = [
    {'role': 'system', 'content': 'You are a helpful assistant.'}
]

while True:
    # 获取用户输入
    user_input = input("Yao: ")

    # 检查用户是否表达了结束对话的意思
    if '再见' in user_input or '结束' in user_input or '拜拜' in user_input:
        print("感谢您的咨询，再见")
        break

    # 添加用户输入到对话历史
    conversation_history.append({'role': 'user', 'content': user_input})

    # 调用API生成流式回复
    completion = client.chat.completions.create(
        model="qwen-plus",  # 选择的模型
        messages=conversation_history,
        stream=True  # 启用流式输出
        )

    full_reply = ""

    # 流式输出每个数据块
    for chunk in completion:
        full_reply += chunk.choices[0].delta.content
        print(chunk.choices[0].delta.content)
    # 将助手的完整回复添加到对话历史中
    print(f"完整内容为：{full_reply}")

