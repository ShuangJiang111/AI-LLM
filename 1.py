import os
from openai import OpenAI

# 初始化客户端
try:
    client = OpenAI(
        # 如果没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key='sk-9fdaf5b5b2814c8380e47b427087618d',
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    # 对话历史
    conversation_history = [
        {'role': 'system', 'content': 'You are a helpful assistant.'}
    ]

    while True:
        # 获取用户输入
        user_input = input("用户: ")

        # 检查用户是否表达了结束对话的意思
        if '再见' in user_input or '结束' in user_input or '拜拜' in user_input:
            print("感谢您的咨询，再见")
            break

        # 添加用户输入到对话历史
        conversation_history.append({'role': 'user', 'content': user_input})

        # 调用API生成回复
        completion = client.chat.completions.create(
            model="qwen-plus",  # 选择的模型
            messages=conversation_history

        )

        # 获取并显示AI的回复
        assistant_reply = completion.choices[0].message.content
        print("助手:", assistant_reply)

        # 将助手的回复添加到对话历史中
        conversation_history.append({'role': 'assistant', 'content': assistant_reply})

except Exception as e:
    print(f"错误信息：{e}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
