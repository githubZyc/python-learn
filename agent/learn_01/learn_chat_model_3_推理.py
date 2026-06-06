"""
推理
较新的模型能够执行多步推理以得出结论。这涉及将复杂问题分解为更小、更易管理的步骤。

如果底层模型支持，您可以显示此推理过程以更好地理解模型如何得出其最终答案。
"""
from agent.learn_01.learn_chat_model_1 import model

# for chunk in model.stream("为什么鹦鹉有五颜六色的羽毛？"):
#     reasoning_steps = [r for r in chunk.content_blocks if r["type"] == "reasoning"]
#     print(reasoning_steps if reasoning_steps else chunk.text)


response = model.invoke("为什么鹦鹉有五颜六色的羽毛？")
reasoning_steps = [b for b in response.content_blocks if b["type"] == "reasoning"]
print(" ".join(step["reasoning"] for step in reasoning_steps))
