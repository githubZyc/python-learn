"""
动态系统提示
对于需要根据运行时上下文或智能体状态修改系统提示的高级用例，您可以使用
[https://langchain-doc.cn/v1/python/langchain/middleware]
 中间件。

@dynamic_prompt 装饰器创建中间件，根据模型请求动态生成系统提示
"""
import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, dynamic_prompt
from langchain_core.tools import tool
from langchain_qwq import ChatQwen

from agent.learn_01.format_print_util import message_format

load_dotenv()


class Context(TypedDict):
    user_role: str


@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    """
    根据用户角色生成系统提示
    """
    context = request.runtime.context or {}
    user_role = context.get("user_role", "user")
    print(f"用户角色：{user_role}")

    base_prompt = "你是一个有帮助的助手。"

    if user_role == "expert":
        return f"{base_prompt} 提供详细的技术响应。"
    elif user_role == "beginner":
        return f"{base_prompt} 简单解释概念，避免使用行话。"

    return base_prompt


@tool
def get_user_message(user_role: str) -> str:
    """根据用户角色获取用户消息"""
    return f"用户角色：{user_role},如何学习python agent 开发"


qwen = ChatQwen(model="qwen-plus", temperature=0.9, base_url=(os.environ.get('DASHSCOPE_BASE_URL') or ""))
agent = create_agent(model=qwen, middleware=[user_role_prompt], tools=[get_user_message], context_schema=Context)
# 系统提示将根据上下文动态设置
result = agent.invoke(
    {"messages": [{"role": "user", "content": "解释机器学习"}]},
    context={"user_role": "expert"}
)
message_format(result)
