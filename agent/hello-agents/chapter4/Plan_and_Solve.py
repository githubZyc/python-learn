PLANNER_PROMPT_TEMPLATE = """
你是一个顶级的AI规划专家。你的任务是将用户提出的复杂问题分解成一个由多个简单步骤组成的行动计划。
请确保计划中的每个步骤都是一个独立的、可执行的子任务，并且严格按照逻辑顺序排列。
你的输出必须是一个Python列表，其中每个元素都是一个描述子任务的字符串。

问题: {question}
请严格按照以下格式输出你的计划,```python与```作为前后缀是必要的:
```python
["步骤1", "步骤2", "步骤3", ...]
```
"""

# 这个提示词通过以下几点确保了输出的质量和稳定性：
#
# 角色设定： “顶级的AI规划专家”，激发模型的专业能力。
# 任务描述： 清晰地定义了“分解问题”的目标。
# 格式约束： 强制要求输出为一个 Python 列表格式的字符串，这极大地简化了后续代码的解析工作，使其比解析自然语言更稳定、更可靠。
from HelloAgentsLLM import HelloAgentsLLM
import ast


class Planner:
    def __init__(self, llm: HelloAgentsLLM):
        self.llm = llm

    def plan(self, question: str) -> list[str]:
        """
        根据用户问题生成一个行动计划。
        """
        template_format \
            = PLANNER_PROMPT_TEMPLATE.format(question=question)
        # 调用大模型。根据消息生成计划
        # 为了生成计划，我们构建一个简单的消息列表
        messages = [
            {"role": "user", "content": template_format}
        ]

        print("--- 正在生成计划 ---")
        # 使用流式输出来获取完整的计划
        response_text = self.llm.think(messages=messages) or ""

        print(f"✅ 计划已生成:\n{response_text}")

        # 解析LLM输出的列表字符串
        try:
            # 找到```python和```之间的内容
            plan_str = response_text.split("```python")[1].split("```")[0].strip()
            # 使用ast.literal_eval来安全地执行字符串，将其转换为Python列表
            plan = ast.literal_eval(plan_str)
            return plan if isinstance(plan, list) else []
        except (ValueError, SyntaxError, IndexError) as e:
            print(f"❌ 解析计划时出错: {e}")
            print(f"原始响应: {response_text}")
            return []
        except Exception as e:
            print(f"❌ 解析计划时发生未知错误: {e}")
            return []


EXECUTOR_PROMPT_TEMPLATE = """
你是一位顶级的AI执行专家。你的任务是严格按照给定的计划，一步步地解决问题。
你将收到原始问题、完整的计划、以及到目前为止已经完成的步骤和结果。
请你专注于解决“当前步骤”，并仅输出该步骤的最终答案，不要输出任何额外的解释或对话。

# 原始问题:
{question}

# 完整计划:
{plan}

# 历史步骤与结果:
{history}

# 当前步骤:
{current_step}

请仅输出针对“当前步骤”的回答:
"""


class Executor:
    def __init__(self, llm: HelloAgentsLLM):
        self.llm = llm

    def execute(self, question: str, plan: list[str]) -> str:
        """
        根据计划执行任务。
        """
        history = ""  # 用于存储历史步骤和结果的字符串
        for i, step in enumerate(plan):
            print(f"\n-> 正在执行步骤 {i + 1}/{len(plan)}: {step}")
            prompt = EXECUTOR_PROMPT_TEMPLATE.format(question=question,
                                                     plan=plan,
                                                     history=history if history else "无",  # 如果是第一步，则历史为空
                                                     current_step=step)

            messages = [{"role": "user", "content": prompt}]
            response_text = self.llm.think(messages=messages) or ""
            # 更新历史记录，为下一步做准备
            history += f"步骤 {i + 1}: {step}\n结果: {response_text}\n\n"

            print(f"✅ 步骤 {i + 1} 已完成，结果: {response_text}")
        # 循环结束后，最后一步的响应就是最终答案
        final_answer = response_text
        return final_answer


# if __name__ == "__main__":
#     hello = HelloAgentsLLM()
#     planner = Executor(hello)
#     planner.execute("如何从零开始学习深度学习？", ["步骤1", "步骤2", "步骤3"])


# 现在已经分别构建了负责“规划”的 Planner 和负责“执行”的 Executor。
# 最后一步是将这两个组件整合到一个统一的智能体 PlanAndSolveAgent 中，并赋予它解决问题的完整能力。
# 我们将创建一个主类 PlanAndSolveAgent，它的职责非常清晰：接收一个 LLM 客户端，初始化内部的规划器和执行器，并提供一个简单的 run 方法来启动整个流程。

class PlanAndSolveAgent:
    def __init__(self, llm: HelloAgentsLLM):
        self.llm = llm
        self.planner = Planner(llm)
        self.executor = Executor(llm)

    def run(self, question: str):
        """
       运行智能体的完整流程:先规划，后执行。
       """
        print(f"\n--- 开始处理问题 ---\n问题: {question}")

        # 先开始规划
        plan = self.planner.plan(question)

        # 检查计划是否成功生成
        if not plan:
            print("\n--- 任务终止 --- \n无法生成有效的行动计划。")
            return

        # 检查计划是否成功生成
        if not plan:
            print("\n--- 任务终止 --- \n无法生成有效的行动计划。")
            return
            # 2. 调用执行器执行计划
        execute = self.executor.execute(question, plan)
        print(f"\n--- 任务完成 ---\n最终答案: {execute}")


# --- 5. 主函数入口 ---
if __name__ == '__main__':
    try:
        llm_client = HelloAgentsLLM()
        agent = PlanAndSolveAgent(llm_client)
        question = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"
        agent.run(question)
    except ValueError as e:
        print(e)

"""
/Users/zhengyanchuang/.local/bin/uv run /Volumes/files/workspace/python/learn/.venv/bin/python /Volumes/files/workspace/python/learn/agent/hello-agents/chapter4/Plan_and_Solve.py 

--- 开始处理问题 ---
问题: 一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？
--- 正在生成计划 ---
🧠 正在调用 qwen-plus 模型...
✅ 大语言模型响应成功:
```python
["计算周一卖出的苹果数量：15个", "计算周二卖出的苹果数量：15 × 2 = 30个", "计算周三卖出的苹果数量：30 − 5 = 25个", "将三天卖出的苹果数量相加：15 + 30 + 25 = 70个"]
```
✅ 计划已生成:
```python
["计算周一卖出的苹果数量：15个", "计算周二卖出的苹果数量：15 × 2 = 30个", "计算周三卖出的苹果数量：30 − 5 = 25个", "将三天卖出的苹果数量相加：15 + 30 + 25 = 70个"]
```

-> 正在执行步骤 1/4: 计算周一卖出的苹果数量：15个
🧠 正在调用 qwen-plus 模型...
✅ 大语言模型响应成功:
15
✅ 步骤 1 已完成，结果: 15

-> 正在执行步骤 2/4: 计算周二卖出的苹果数量：15 × 2 = 30个
🧠 正在调用 qwen-plus 模型...
✅ 大语言模型响应成功:
30
✅ 步骤 2 已完成，结果: 30

-> 正在执行步骤 3/4: 计算周三卖出的苹果数量：30 − 5 = 25个
🧠 正在调用 qwen-plus 模型...
✅ 大语言模型响应成功:
25
✅ 步骤 3 已完成，结果: 25

-> 正在执行步骤 4/4: 将三天卖出的苹果数量相加：15 + 30 + 25 = 70个
🧠 正在调用 qwen-plus 模型...
✅ 大语言模型响应成功:
70
✅ 步骤 4 已完成，结果: 70

--- 任务完成 ---
最终答案: 70

Process finished with exit code 0


"""

# 规划阶段： 智能体首先调用 Planner，成功地将复杂的应用题分解成了一个包含四个逻辑步骤的 Python 列表。这个结构化的计划为后续的执行奠定了基础。
# 执行阶段： Executor 严格按照生成的计划，一步一步地向下执行。在每一步中，它都将历史结果作为上下文，确保了信息的正确传递（例如，步骤2正确地使用了步骤1的结果“15个”，步骤3也正确使用了步骤2的结果“30个”）。
# 结果：整个过程逻辑清晰，步骤明确，最终智能体准确地得出了正确答案“70个”。
