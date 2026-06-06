"""
多模态
某些模型可以处理和返回非文本数据，如图像、音频和视频。您可以通过提供内容块将非文本数据传递给模型。
"""
from agent.learn_01.learn_chat_model_1 import model

response = model.invoke("创建一张猫的图片")
print(response.content_blocks)
# [
#     {"type": "text", "text": "这是一张猫的图片"},
#     {"type": "image", "base64": "...", "mime_type": "image/jpeg"},
# ]
