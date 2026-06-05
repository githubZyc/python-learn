"""
结构化输出
在某些情况下，您可能希望智能体以特定格式返回输出。LangChain 通过 response_format 参数提供结构化输出策略。

ToolStrategy
ToolStrategy 使用人工工具调用生成结构化输出。这适用于任何支持工具调用的模型：
"""
import os

from langchain.agents.structured_output import ToolStrategy, ProviderStrategy
from langchain_qwq import ChatQwen
from pydantic import BaseModel

from langchain.agents import create_agent
from agent.learn_01.learn_agent_tool import qw_llm


class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str


qw_llm = ChatQwen(model="qwen-plus", temperature=0.9, base_url=(os.environ.get('DASHSCOPE_BASE_URL') or ""))

"""
ToolStrategy
ToolStrategy 使用人工工具调用生成结构化输出。这适用于任何支持工具调用的模型：

    ProviderStrategy
ProviderStrategy 使用模型提供商的原生结构化输出生成。这更可靠，但仅适用于支持原生结构化输出的提供商（例如 OpenAI）
"""

agent = create_agent(model=qw_llm, tools=[],
                     response_format=ProviderStrategy(ContactInfo))

result = agent.invoke({
    "messages": [{"role": "user", "content": "从以下内容提取联系信息：John Doe, john@example.com, (555) 123-4567"}]
})
response_ = result["structured_response"]
print(response_)
