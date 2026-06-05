"""
动态模型在 运行时 根据当前 状态 和上下文进行选择。这支持复杂的路由逻辑和成本优化。

要使用动态模型，请使用 @wrap_model_call 装饰器创建中间件，以修改请求中的模型：
"""
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import ModelResponse, ModelRequest, wrap_model_call
from langchain_qwq import ChatQwen

load_dotenv()

basic_model = ChatQwen(
    model="qwen-plus",
    temperature=0.9,
    base_url=(os.environ.get('DASHSCOPE_BASE_URL') or ""),
)

advanced_model = ChatQwen(
    model="qwen-plus-v2",
    temperature=0.9,
    base_url=(os.environ.get('DASHSCOPE_BASE_URL') or ""),
)


@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """根据对话复杂性选择模型。"""
    message_count = len(request.state["messages"])
    if message_count > 5:
        request = request.override(model=advanced_model)
    else:
        request = request.override(model=basic_model)
    return handler(request)


agent = create_agent(
    model=basic_model,  # 默认模型
    tools=[],
    middleware=[dynamic_model_selection]
)

invoke = agent.invoke({"messages": [{"role": "user", "content": "北京天气如何"}]})
print(invoke)
