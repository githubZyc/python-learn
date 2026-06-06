"""
消息是 LangChain 中模型上下文的基本单位。
它们代表模型的输入和输出，携带内容和元数据，用于在与 LLM 交互时表示对话状态。
消息是包含以下内容的对象：

角色 - 标识消息类型（例如 system、user）
内容 - 表示消息的实际内容（例如文本、图像、音频、文档等）
元数据 - 可选字段，例如响应信息、消息 ID 和令牌使用情况
LangChain 提供了一种标准消息类型，可在所有模型提供商之间工作，
确保无论调用哪个模型都能保持一致的行为。

"""
from langchain_core.messages import SystemMessage, HumanMessage

from agent.learn_01.learn_chat_model_1 import model

SystemMessage(content="你是一个助手")
HumanMessage(content="翻译：我喜欢编程。")

invoke = model.invoke([SystemMessage(content="你是一个助手"), HumanMessage(content="翻译：我喜欢编程。")])
print(invoke)
