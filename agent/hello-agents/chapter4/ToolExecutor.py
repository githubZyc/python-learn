"""
当智能体需要使用多种工具时（例如，除了搜索，还可能需要计算、查询数据库等），我们需要一个统一的管理器来注册和调度这些工具。
为此，我们创建一个 ToolExecutor 类。

"""
from typing import List, Dict, Any
from serp_tool import serp_search


class ToolExecutor:
    """
    一个工具执行器，负责管理和执行工具。
    """

    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def registerTool(self, name: str, description: str, func: callable):
        """
        注册一个工具。
        :param name: 工具名称
        :param description: 工具描述
        :param func: 工具函数
        """

        if name in self.tools:
            print(f"警告:工具 '{name}' 已存在，将被覆盖。")
        self.tools[name] = {
            "name": name,
            "description": description,
            "func": func
        }
        print(f"已注册工具: {name}")

    def getTool(self, name: str) -> callable:
        """
        获取一个工具。
        :param name: 工具名称
        :return: 工具函数
        """
        return self.tools[name]["func"]

    def getAvailableTools(self) -> str:
        """
        获取所有可用工具的格式化描述字符串。
        """
        return "\n".join([
            f"- {name}: {info['description']}"
            for name, info in self.tools.items()
        ])


# --- 工具初始化与使用示例 ---
if __name__ == "__main__":
    # 1 初始化工具执行器
    toolExecutor = ToolExecutor()
    # 2 注册我们的实战搜索工具
    search_desc = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    toolExecutor.registerTool("serp_search", search_desc, serp_search)
    # 3. 打印可用的工具
    print("\n--- 可用的工具 ---")
    print(toolExecutor.getAvailableTools())
    # 4. 智能体的Action调用，这次我们问一个实时性的问题
    print("\n--- 执行 Action: Search['英伟达最新的GPU型号是什么'] ---")
    tool_name = "serp_search"
    tool_input = "英伟达最新的GPU型号是什么"

    tool_function = toolExecutor.getTool(tool_name)

    if tool_function:
        observation = tool_function(tool_input)
        print("--- 观察 (Observation) ---")
        print(observation)
    else:
        print(f"错误:未找到名为 '{tool_name}' 的工具。")
