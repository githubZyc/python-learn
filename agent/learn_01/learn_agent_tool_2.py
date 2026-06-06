"""
工具赋予智能体执行行动的能力。智能体超越了简单的仅模型工具绑定，实现了：

序列中的多个工具调用（由单个提示触发）
适当的并行工具调用
基于先前结果的动态工具选择
工具重试逻辑和错误处理
工具调用之间的状态持久化


模型可以请求调用执行任务的工具，例如从数据库获取数据、搜索网络或运行代码。工具是以下内容的配对：

架构，包括工具的名称、描述和/或参数定义（通常是 JSON 架构）
要执行的函数或协程
注意
您可能会听到“函数调用”一词。我们将此与“工具调用”互换使用。

要使您定义的工具可供模型使用，您必须使用 bind_tools() 绑定它们。在后续调用中，模型可以根据需要选择调用任何绑定的工具。

一些模型提供商提供内置工具，可通过模型或调用参数启用（例如 ChatOpenAI、ChatAnthropic）。请查看相应的提供商参考以了解详细信息。

提示
有关创建工具的详细信息和其他选项，请参阅工具指南。


绑定用户定义的工具时，模型的响应包括请求执行工具。当将模型与代理分开使用时，您需要执行请求的操作并将结果返回给模型以用于后续推理。请注意，当使用代理时，代理循环将为您处理工具执行循环。

下面展示了一些使用工具调用的常见方法。


"""
from langchain import tools
#
from langchain.tools import tool

from agent.learn_01.learn_chat_model_01 import model


#
#
@tool
def get_weather(location: str) -> str:
    """获取某个位置的天气。"""
    return f"{location} 天气晴朗。"


#
# model_with_tools = model.bind_tools([get_weather])  # [!code highlight]
#
# response = model_with_tools.invoke("波士顿的天气怎么样？")
# for tool_call in response.tool_calls:
#     # 查看模型发出的工具调用
#     print(f"工具：{tool_call['name']}")
#     print(f"参数：{tool_call['args']}")
"""
工具执行循环
当模型返回工具调用时，您需要执行工具并将结果传递回模型。这会创建一个对话循环，模型可以使用工具结果生成其最终响应。LangChain 包含代理抽象来为您处理此协调。
"""
# 将（可能多个）工具绑定到模型
model_with_tools = model.bind_tools(tools=[get_weather], parallel_tool_calls=True)
#
# # 步骤 1：模型生成工具调用
# messages = [{"role": "user", "content": "波士顿的天气怎么样？"}]
# ai_msg = model_with_tools.invoke(messages)
# messages.append(ai_msg)
# print(f"messages is",messages)
#
# # 步骤 2：执行工具并收集结果
# for tool_call in ai_msg.tool_calls:
#     # 使用生成的参数执行工具
#     tool_result = get_weather.invoke(tool_call)
#     messages.append(tool_result)
#     print(f"for tool_call in ai_msg.tool_calls:messages is",messages)
# # 步骤 3：将结果传递回模型以获取最终响应
# final_response = model_with_tools.invoke(messages)
# print(final_response.text)
# # "波士顿当前天气为 72°F，晴朗。"

"""
流式传输工具调用
在流式传输响应时，工具调用通过 ToolCallChunk 逐步构建。
这允许您在生成工具调用时查看它们，而不是等待完整响应。
"""

# for chunk in model_with_tools.stream(
#         "波士顿和东京的天气怎么样？"
# ):
#     # 工具调用块逐步到达
#     for tool_chunk in chunk.tool_call_chunks:
#         if name := tool_chunk.get("name"):
#             print(f"工具：{name}")
#         if id_ := tool_chunk.get("id"):
#             print(f"ID：{id_}")
#         if args := tool_chunk.get("args"):
#             print(f"参数：{args}")


gathered = None
for chunk in model_with_tools.stream("波士顿的天气怎么样？"):
    gathered = chunk if gathered is None else gathered + chunk
    print(gathered.tool_calls)
