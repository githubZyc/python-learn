"""
工具赋予智能体执行行动的能力。智能体超越了简单的仅模型工具绑定，实现了：

序列中的多个工具调用（由单个提示触发）
适当的并行工具调用
基于先前结果的动态工具选择
工具重试逻辑和错误处理
工具调用之间的状态持久化
"""
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, wrap_tool_call, ModelRequest
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langchain_qwq import ChatQwen

load_dotenv()


@tool
def search(query: str) -> str:
    """
    搜索
    """
    return f"结果：{query}"


@tool
def get_weather_tool(city: str) -> str:
    """
    搜索
    """

    return f"：{city}天气非常好!"


@wrap_tool_call
def handler_tool_errors(request: ModelRequest, handler):
    """使用自定义消息处理工具执行错误。"""
    try:
        return handler(request)
    except Exception as e:
        # 向模型返回自定义错误消息
        return ToolMessage(
            content=f"工具错误：请检查您的输入并重试。({str(e)})",
            tool_call_id=request.tool_call["id"]
        )


qw_llm: ChatQwen = ChatQwen(model="qwen-plus", temperature=0.9, base_url=(os.environ.get('DASHSCOPE_BASE_URL') or ""))

agent = create_agent(model=qw_llm, tools=[search, get_weather_tool],
                     middleware=[handler_tool_errors])
invoke \
    = agent.invoke({"messages": [{"role": "user", "content": "郑州"}]})
print(invoke)
