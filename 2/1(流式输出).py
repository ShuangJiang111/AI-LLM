import os
from dashscope import Generation

# 存储对话历史
messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'}
]


def get_response(user_input):
    # 向消息列表添加用户输入
    messages.append({'role': 'user', 'content': user_input})

    # 检查用户是否希望结束对话
    if "再见" in user_input or "结束" in user_input or "拜拜" in user_input:
        return "感谢您的咨询，再见"

    # 调用 DashScope API 获取响应，启用流式输出
    responses = Generation.call(
        api_key=os.getenv('sk-9fdaf5b5b2814c8380e47b427087618d'),
        model="qwen-plus",
        messages=messages,
        result_format="message",
        stream=True,  # 启用流式输出
        incremental_output=True  # 启用增量式流式输出
    )

    assistant_reply = ""
    print("流式输出内容为：")
    for response in responses:
        # 每次接收到新部分时，将其添加到助手的回复中
        chunk_content = response.output.choices[0].message.content
        assistant_reply += chunk_content
        # 实时输出接收到的内容
        print(chunk_content, end='', flush=True)

    # 更新对话历史
    messages.append({'role': 'assistant', 'content': assistant_reply})

    return assistant_reply


# 示例交互
while True:
    user_input = input("用户: ")

    # 获取 AI 回复
    reply = get_response(user_input)

    # 如果对话结束，退出循环
    if "感谢您的咨询，再见" in reply:
        break
