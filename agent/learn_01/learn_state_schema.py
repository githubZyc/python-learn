"""
通过 state_schema 定义状态
使用 state_schema 参数作为快捷方式，定义仅在工具中使用的自定义状态。
"""
import os

from langchain.agents import AgentState, create_agent
from langchain_core.tools import tool
from langchain_qwq import ChatQwen

from agent.learn_01.format_print_util import message_format


@tool
def tool1(user_preferences: dict) -> str:
    """
    获取用户偏好。
    """
    return f"用户偏好：{user_preferences}"


@tool
def tool2(user_preferences: dict) -> str:
    """
    获取用户偏好。
    """
    return f"用户偏好：{user_preferences}"


class CustomState(AgentState):
    user_preferences: dict


llm_chat_qwen = ChatQwen(model="qwen-plus", temperature=0.9, base_url=(os.environ.get('DASHSCOPE_BASE_URL') or ""))

agent = create_agent(
    llm_chat_qwen,
    tools=[tool1, tool2],
    state_schema=CustomState
)
# 智能体现在可以跟踪消息之外的额外状态
result = agent.invoke({
    "messages": [{"role": "user", "content": "我更喜欢技术性解释"}],
    "user_preferences": {"style": "technical", "verbosity": "detailed"},
})

message_format(result)
