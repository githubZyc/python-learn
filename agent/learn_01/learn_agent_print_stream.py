"""
流式传输
我们已经看到如何使用 invoke 调用智能体以获取最终响应。
如果智能体执行多个步骤，这可能需要一段时间。
为了显示中间进度，我们可以随着消息的发生而流式传回。
"""
import os

from langchain.agents import create_agent
from langchain_qwq import ChatQwen

llm_chat_qwen = ChatQwen(model="qwen-plus", temperature=0.9, base_url=(os.environ.get('DASHSCOPE_BASE_URL') or ""))
agent \
    = create_agent(model=llm_chat_qwen)
# agent.invoke({"messages": [{"role": "user", "content": "写一个武林外史200字"}], "stream": True})

"""
原因是 stream_mode="values" 每次返回的是完整状态快照，不是逐 token 增量。要实现逐字打印效果，需要用 stream_mode="messages" 并配合 end="" 逐块拼接输出：
关键区别：
stream_mode:行为:输出效果:"values":每步返回完整状态快照
整条消息一次性输出
"messages":逐 token 增量返回:逐字打印（打字机效果）
三个要点：
stream_mode="messages" — 返回 (chunk, metadata) 元组，
chunk 是逐 token 的增量
metadata["langgraph_node"] == "model" 
— 过滤只输出模型节点的 token，避免重复输出工具调用结果
end="", flush=True — 不换行、立即刷新缓冲区，实现逐字打印效果
"""

for chunk, metadata in agent.stream({
    "messages": [{"role": "user", "content": "写一个武林外史200字"}]
}, stream_mode="messages"):
    # 跳过非内容块
    if chunk.content and metadata["langgraph_node"] == "model":
        print(chunk.content, end="", flush=True)
