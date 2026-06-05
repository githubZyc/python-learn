"""
通过中间件定义状态
当您的自定义状态需要被特定中间件钩子和附加到该中间件的工具访问时，使用中间件定义自定义状态。
"""
import os
from typing import Any

from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import AgentMiddleware
from langchain_core.tools import tool
from langchain_qwq import ChatQwen

from agent.learn_01.format_print_util import message_format
from agent.learn_01.learn_01_qw_agent import llm_chat_qwen


class CustomState(AgentState):
    user_preferences: dict


@tool
def t1(user_preferences: dict) -> str:
    """
    获取用户偏好。
    """
    return f"用户偏好：{user_preferences}"


@tool
def t2(user_preferences: dict) -> str:
    """
    获取用户偏好。
    """
    return f"用户偏好：{user_preferences}"


class CustomMiddleware(AgentMiddleware):
    """自定义中间件。"""
    state_schema = CustomState
    tools = [t1, t2]

    def before_model(self, state: CustomState, runtime) -> dict[str, Any] | None:
        ...


llm_chat_qwen = ChatQwen(model="qwen-plus", temperature=0.9, base_url=(os.environ.get('DASHSCOPE_BASE_URL') or ""))
agent = create_agent(model=llm_chat_qwen, tools=[], middleware=[CustomMiddleware()])

# 智能体现在可以跟踪消息之外的额外状态
result = agent.invoke({
    "messages": [{"role": "user", "content": "我更喜欢技术性解释"}],
    "user_preferences": {"style": "technical", "verbosity": "detailed"},
})

message_format(result)
