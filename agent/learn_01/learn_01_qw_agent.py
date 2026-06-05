import os
from dataclasses import dataclass

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_qwq import ChatQwen
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolRuntime

b = load_dotenv()
print(f"是否加载成功：{b}")
print(f"DASHSCOPE_API_KEY: {os.environ.get('DASHSCOPE_API_KEY')}")

SYSTEM_PROMPT = \
    """你是一位擅长用双关语表达的专家天气预报员。
    你可以使用两个工具：
    
    - get_weather_for_location：用于获取特定地点的天气
    - get_user_location：用于获取用户的位置
    
    如果用户询问天气，请确保你知道具体位置。如果从问题中可以判断他们指的是自己所在的位置，请使用 get_user_location 工具来查找他们的位置。
    """


@dataclass
class Context:
    """
    上下文信息
    """
    user_id: str


# 定义响应格式
@dataclass
class ResponseFormat:
    """代理的响应模式。"""
    # 带双关语的回应（始终必需）
    punny_response: str
    # 天气的任何有趣信息（如果有）
    weather_conditions: str | None = None


# 定义工具
@tool
def get_weather_for_location(location: str) -> str:
    """
    获取特定地点的天气
    """
    return f"{location}今天天气不错"


@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """根据用户 ID 获取用户信息。"""
    user_id = runtime.context.user_id
    return "北京" if user_id == "1" else "SF"


llm_chat_qwen = ChatQwen(
    model="qwen-plus",
    temperature=0.9,
    base_url=(os.environ.get('DASHSCOPE_BASE_URL') or ""),
)

# 设置记忆
checkpointer = InMemorySaver()

# 创建代理
agent = create_agent(
    model=llm_chat_qwen,
    tools=[get_user_location, get_weather_for_location],
    system_prompt=SYSTEM_PROMPT,
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer
)

# 运行代理
# `thread_id` 是给定对话的唯一标识符。
config = {"configurable": {"thread_id": "1"}}
response = agent.invoke(
    {
        "messages": [{"role": "user", "content": "北京天气如何"}],
        "context": Context(user_id="1")
    },
    config=config,
)

print(response['structured_response'])

# 注意，我们可以使用相同的 `thread_id` 继续对话。
response = agent.invoke(
    {"messages": [{"role": "user", "content": "谢谢！"}]},
    config=config,
    context=Context(user_id="1")
)

print(response['structured_response'])
