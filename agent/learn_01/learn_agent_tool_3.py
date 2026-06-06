"""
工具
许多 AI 应用程序通过自然语言与用户交互。
然而，某些用例要求模型使用结构化输入直接与外部系统（例如 API、数据库 或 文件系统）对接。

工具 是 代理（agents） 调用来执行操作的组件。
它们通过允许模型通过定义明确的输入和输出与世界交互来扩展模型的功能。
工具封装了一个可调用的函数及其输入架构（schema）。
这些可以传递给兼容的 聊天模型（chat models），让模型决定是否以及使用什么参数来调用工具。
在这些场景中，工具调用 使模型能够生成符合指定输入架构的请求。

服务器端工具使用 (Server-side tool use)

某些聊天模型（例如 OpenAI、Anthropic 和 Gemini）具有 内置工具，这些工具在服务器端执行，例如网络搜索和代码解释器。
请参阅 提供商概览（provider overview） 了解如何使用您的特定聊天模型访问这些工具。

创建工具 (Create tools)
基本工具定义 (Basic tool definition)
创建工具最简单的方法是使用 @tool 装饰器。
默认情况下，函数的 文档字符串（docstring）会成为工具的描述，帮助模型理解何时使用它：
"""
from langchain.tools import tool


# 类型提示 是必需的，因为它们定义了工具的输入架构。
# 文档字符串应该信息丰富且简洁，以帮助模型理解工具的用途。

@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    return f"Found {limit} results for '{query}'"


# 自定义工具名称 (Custom tool name)
# 默认情况下，工具名称来自函数名称。当您需要更具描述性的名称时，可以覆盖它：
@tool("web_search")  # Custom name
def search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"


print(search.name)  # web_search

"""
自定义工具描述 (Custom tool description)
覆盖自动生成的工具描述，以提供更清晰的模型指导：
"""


@tool("calculator",
      description="Performs arithmetic calculations. Use this for any math problems.")
def calculator(expression: str) -> str:
    """Evaluate mathematical expressions."""
    return str(eval(expression))
