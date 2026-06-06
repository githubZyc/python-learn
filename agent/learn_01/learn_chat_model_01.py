"""
模型可以通过两种方式使用：

与代理一起使用 - 创建代理时可动态指定模型。
独立使用 - 模型可直接调用（在代理循环之外），用于文本生成、分类或提取等任务，而无需代理框架。
同一模型接口在两种上下文中均适用，这为您提供了从简单开始并根据需要扩展到更复杂基于代理的工作流程的灵活性。

初始化模型
在 LangChain 中开始使用独立模型的最简单方法是使用 init_chat_model 从您选择的提供商初始化一个模型（以下示例）：

关键方法
方法	说明
Invoke	模型接受消息作为输入，并在生成完整响应后输出消息。
Stream	调用模型，但实时流式传输生成的输出。
Batch	将多个请求批量发送给模型，以实现更高效的处理。


参数
聊天模型接受可用于配置其行为的一组参数。支持的参数集因模型和提供商而异，但标准参数包括：

参数	类型	必填	说明
model	string	是	您想使用的特定模型的名称或标识符。
api_key	string	否	用于向模型提供商进行身份验证的密钥。通常在注册访问模型时颁发。通常通过设置环境变量访问。
temperature	number	否	控制模型输出的随机性。值越高，响应越具创造性；值越低，响应越确定性。
timeout	number	否	在取消请求之前等待模型响应的最大时间（秒）。
max_tokens	number	否	限制响应中的令牌总数，有效控制输出长度。
max_retries	number	否	如果因网络超时或速率限制等问题而失败，系统将重新发送请求的最大尝试次数。
"""
import os
import asyncio
from langchain_qwq import ChatQwen

model = ChatQwen(
    model="qwen-plus",
    temperature=0.7,
    timeout=30,
    max_tokens=1000,
    base_url=(os.environ.get('DASHSCOPE_BASE_URL') or ""),
)
# print(model)
# print(model.invoke("为什么鹦鹉有五颜六色的羽毛？"))
from langchain.messages import HumanMessage, AIMessage, SystemMessage

conversation = [
    {"role": "system", "content": "你是一个将英语翻译成法语的有用助手。"},
    {"role": "user", "content": "翻译：我喜欢编程。"},
    {"role": "assistant", "content": "J'adore la programmation."},
    {"role": "user", "content": "翻译：我喜欢构建应用程序。"}
]

# response = model.invoke(conversation)
# print(response)  # AIMessage("J'adore créer des applications.")

# for chunk in model.stream("为什么鹦鹉有五颜六色的羽毛？"):
#     print(chunk.text, end="|", flush=True)

# for chunk in model.stream("天空是什么颜色？"):
#     for block in chunk.content_blocks:
#         if block["type"] == "reasoning" and (reasoning := block.get("reasoning")):
#             print(f"推理：{reasoning}")
#         elif block["type"] == "tool_call_chunk":
#             print(f"工具调用块：{block}")
#         elif block["type"] == "text":
#             print(block["text"])
#         else:
#             ...

# full = None  # None | AIMessageChunk
# for chunk in model.stream("天空是什么颜色？"):
#     full = chunk if full is None else full + chunk
#     print(full.text)

# 天空
# 天空是
# 天空通常
# 天空通常是蓝色
# ...

# print(full.content_blocks)
# [{"type": "text", "text": "天空通常是蓝色..."}]


"""
高级流式传输主题
“自动流式传输”聊天模型
LangChain 通过在某些情况下自动启用流式传输模式来简化从聊天模型进行流式传输，即使您未显式调用流式传输方法。这在您使用非流式传输的 invoke 方法但仍希望流式传输整个应用程序（包括聊天模型的中间结果）时特别有用。

例如，在 LangGraph 代理 中，您可以在节点内调用 model.invoke()，但如果在流式传输模式下运行，LangChain 将自动委托给流式传输。

工作原理

当您 invoke() 一个聊天模型时，如果 LangChain 检测到您正在尝试流式传输整个应用程序，它将自动切换到内部流式传输模式。对于使用 invoke 的代码，结果是相同的；然而，在聊天模型流式传输时，LangChain 将负责在 LangChain 的回调系统中调用 on_llm_new_token 事件。

回调事件允许 LangGraph 的 stream() 和 astream_events() 实时显示聊天模型的输出。

流式传输事件
LangChain 聊天模型还可以使用 astream_events() 流式传输语义事件。

这简化了基于事件类型和其他元数据的过滤，并在后台聚合完整消息。请参阅以下示例。

"""

# async def stream_events():
#     async for event in model.astream_events("你好"):
#
#         if event["event"] == "on_chat_model_start":
#             print(f"输入：{event['data']['input']}")
#
#         elif event["event"] == "on_chat_model_stream":
#             print(f"令牌：{event['data']['chunk'].text}")
#
#         elif event["event"] == "on_chat_model_end":
#             print(f"完整消息：{event['data']['output'].text}")
#
#         else:
#             pass
#
# asyncio.run(stream_events())


"""
Batch
将一组独立请求批量处理给模型可以显著提高性能并降低成本，因为处理可以并行进行
"""
# responses = model.batch([
#     "为什么鹦鹉有五颜六色的羽毛？",
#     "飞机是如何飞行的？",
#     "什么是量子计算？"
# ])
# for response in responses:
#     print(response)

"""
默认情况下，batch() 仅返回整个批次的最终输出。
如果您希望在每个单独输入完成生成时接收输出，可以使用 batch_as_completed() 流式传输结果：

for response in model.batch_as_completed([
    "为什么鹦鹉有五颜六色的羽毛？",
    "飞机是如何飞行的？",
    "什么是量子计算？"
]):
    print(response)
注意
使用 batch_as_completed() 时，结果可能无序到达。
每个结果包括输入索引，以便根据需要匹配和重建原始顺序。
提示
在使用 batch() 或 batch_as_completed() 处理大量输入时，您可能希望控制最大并行调用数。这可以通过在 RunnableConfig 字典中设置 max_concurrency 属性来完成。

model.batch(
    list_of_inputs,
    config={
        'max_concurrency': 5,  # 限制为 5 个并行调用
    }
)
"""
