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

    # 调用 DashScope API 获取响应
    response = Generation.call(
        api_key=os.getenv('sk-9fdaf5b5b2814c8380e47b427087618d'),
        model="qwen-plus",
        messages=messages,
        result_format="message"
    )

    if response.status_code == 200:
        # 获取 API 的回复并添加到对话历史中
        assistant_reply = response.output.choices[0].message.content
        messages.append({'role': 'assistant', 'content': assistant_reply})
        return assistant_reply
    else:
        return f"HTTP返回码：{response.status_code}, 错误码：{response.code}, 错误信息：{response.message}"


# 示例交互
while True:
    user_input = input("用户: ")

    # 获取 AI 回复
    reply = get_response(user_input)

    print("助手:", reply)

    # 如果对话结束，退出循环
    if "感谢您的咨询，再见" in reply:
        break
