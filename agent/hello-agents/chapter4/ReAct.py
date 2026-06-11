# ReAct 提示词模板
from IPython.core.debugger import prompt
from websockets.asyncio import messages

REACT_PROMPT_TEMPLATE = """
请注意，你是一个有能力调用外部工具的智能助手。

可用工具如下:
{tools}

请严格按照以下格式进行回应:

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一:
- `{{tool_name}}[{{tool_input}}]`:调用一个可用工具。
- `Finish[最终答案]`:当你认为已经获得最终答案时。
- 当你收集到足够的信息，能够回答用户的最终问题时，你必须在Action:字段后使用 Finish[最终答案] 来输出最终答案。

现在，请开始解决以下问题:
Question: {question}
History: {history}
"""

# 这个模板定义了智能体与LLM之间交互的规范：
#
# 角色定义： “你是一个有能力调用外部工具的智能助手”，设定了LLM的角色。
# 工具清单 ({tools})： 告知LLM它有哪些可用的“手脚”。
# 格式规约 (Thought/Action)： 这是最重要的部分，它强制LLM的输出具有结构性，使我们能通过代码精确解析其意图。
# 动态上下文 ({question}/{history})： 将用户的原始问题和不断累积的交互历史注入，让LLM基于完整的上下文进行决策

# ReActAgent 的核心是一个循环，它不断地“格式化提示词 -> 调用LLM -> 执行动作 -> 整合结果”，直到任务完成或达到最大步数限制。

from HelloAgentsLLM import HelloAgentsLLM
from ToolExecutor import ToolExecutor
from serp_tool import serp_search
import re


class ReAct:
    def __init__(self, llm: HelloAgentsLLM, toolExecutor: ToolExecutor, maxSteps=5):
        self.llm = llm
        self.toolExecutor = toolExecutor
        self.maxSteps = maxSteps
        self.history = []

    def run(self, question: str):
        """
       运行ReAct智能体来回答一个问题。
       """
        self.history = []
        current_step = 0
        while current_step < self.maxSteps:
            current_step += 1
            print(f"当前执行的步骤的第", {current_step}, "步")
            # 格式化提示词
            tool_desc = self.toolExecutor.getAvailableTools()
            print(f"可用工具:\n{tool_desc}")
            history_str = "\n".join(self.history)
            print(f"history_str:\n{history_str}")
            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=tool_desc,
                question=question,
                history=history_str)
            print(f"格式化后的提示词:\n{prompt}")
            messages = [{"role": "user", "content": prompt}]
            self_llm_client_think_response_text = self.llm.think(messages)
            if not self_llm_client_think_response_text:
                print("错误:LLM未能返回有效响应。")
                break
            thought, action = self._parse_output(self_llm_client_think_response_text)
            if thought: print(f"🤔 思考: {thought}")
            if not action: print("警告：未能解析出有效的Action，流程终止。"); break

            if action.startswith("Finish"):
                # 如果是Finish指令，提取最终答案并结束
                final_answer = self._parse_action_input(action)
                print(f"🎉 最终答案: {final_answer}")
                return final_answer

            tool_name, tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                self.history.append("Observation: 无效的Action格式，请检查。");
                continue

            print(f"🎬 行动: {tool_name}[{tool_input}]")
            tool_function = self.toolExecutor.getTool(tool_name)
            observation = tool_function(tool_input) if tool_function else f"错误：未找到名为 '{tool_name}' 的工具。"

            print(f"👀 观察: {observation}")
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")

        print("已达到最大步数，流程终止。")
        return None

    def _parse_output(self, text: str):
        # Thought: 匹配到 Action: 或文本末尾
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", text, re.DOTALL)
        # Action: 匹配到文本末尾
        action_match = re.search(r"Action:\s*(.*?)$", text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    def _parse_action(self, action_text: str):
        match = re.match(r"(\w+)\[(.*)\]", action_text, re.DOTALL)
        return (match.group(1), match.group(2)) if match else (None, None)

    def _parse_action_input(self, action_text: str):
        match = re.match(r"\w+\[(.*)\]", action_text, re.DOTALL)
        return match.group(1) if match else ""


if __name__ == "__main__":
    hello = HelloAgentsLLM()
    toolExecutor = ToolExecutor()
    # 2 注册我们的实战搜索工具
    search_desc = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    toolExecutor.registerTool("serp_search", search_desc, serp_search)
    agent = ReAct(hello, toolExecutor)
    agent.run("华为最新的手机是哪一款？它的主要卖点是什么？")
