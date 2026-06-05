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
# response = agent.invoke(
#     {
#         "messages": [{"role": "user", "content": "北京天气如何"}],
#         "context": Context(user_id="1")
#     },
#     config=config,
# )
#
# print(response)

# 注意，我们可以使用相同的 `thread_id` 继续对话。
response = agent.invoke(
    {"messages": [{"role": "user", "content": "谢谢！"}]},
    config=config,
    context=Context(user_id="1")
)

# ... existing code ...

print("=" * 60)
print("📊 LangGraph Agent 结构化输出")
print("=" * 60)

# 获取消息列表
messages = response.get("messages", [])

# 遍历所有消息
for i, msg in enumerate(messages):
    print(f"\n{'─' * 60}")
    print(f"📨 消息 [{i + 1}/{len(messages)}]")
    print(f"{'─' * 60}")

    # 消息类型
    msg_type = type(msg).__name__
    print(f"📌 类型: {msg_type}")

    # 消息内容
    if hasattr(msg, 'content'):
        print(f"💬 内容: {msg.content}")

    # HumanMessage 特有信息
    if msg_type == "HumanMessage":
        pass  # HumanMessage 通常只有内容

    # AIMessage 特有信息
    elif msg_type == "AIMessage":
        # 工具调用
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            print(f"\n🔧 工具调用:")
            for tool_call in msg.tool_calls:
                print(f"   • 工具名称: {tool_call.get('name', 'N/A')}")
                print(f"   • 参数: {tool_call.get('args', {})}")

        # 无效工具调用
        if hasattr(msg, 'invalid_tool_calls') and msg.invalid_tool_calls:
            print(f"\n⚠️  无效工具调用: {len(msg.invalid_tool_calls)}")

        # Token 使用统计
        if hasattr(msg, 'usage_metadata') and msg.usage_metadata:
            usage = msg.usage_metadata
            print(f"\n📈 Token 使用统计:")
            print(f"   • 输入 Tokens: {usage.get('input_tokens', 'N/A')}")
            print(f"   • 输出 Tokens: {usage.get('output_tokens', 'N/A')}")
            print(f"   • 总计 Tokens: {usage.get('total_tokens', 'N/A')}")

            # 输入 token 详情
            input_details = usage.get('input_token_details', {})
            if input_details:
                print(f"   • 缓存读取: {input_details.get('cache_read', 0)}")

        # 响应元数据
        if hasattr(msg, 'response_metadata') and msg.response_metadata:
            metadata = msg.response_metadata
            print(f"\n🔍 响应元数据:")
            print(f"   • 模型: {metadata.get('model_name', 'N/A')}")
            print(f"   • 提供商: {metadata.get('model_provider', 'N/A')}")
            print(f"   • 完成原因: {metadata.get('finish_reason', 'N/A')}")
            print(f"   • 响应 ID: {metadata.get('id', 'N/A')}")

            # Token 详情
            token_usage = metadata.get('token_usage', {})
            if token_usage:
                print(f"\n   📊 详细 Token 统计:")
                print(f"      - 完成 Tokens: {token_usage.get('completion_tokens', 'N/A')}")
                print(f"      - 提示 Tokens: {token_usage.get('prompt_tokens', 'N/A')}")
                print(f"      - 总 Tokens: {token_usage.get('total_tokens', 'N/A')}")

                # 缓存信息
                prompt_details = token_usage.get('prompt_tokens_details', {})
                if prompt_details:
                    cached = prompt_details.get('cached_tokens', 0)
                    print(f"      - 缓存 Tokens: {cached}")

print(f"\n{'=' * 60}")
print(f"✅ 共处理 {len(messages)} 条消息")
print(f"{'=' * 60}")
