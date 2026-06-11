import os

from langchain_qwq import ChatQwen
from dotenv import load_dotenv
from typing import List, Dict

# 加载 .env 文件中的环境变量
load_dotenv()


class HelloAgentsLLM:
    """
   为本书 "Hello Agents" 定制的LLM客户端。
   它用于调用任何兼容OpenAI接口的服务，并默认使用流式响应。
   """

    def __init__(self, model: str = None, api_key: str = None, base_url: str = None, timeout: int = None):
        """
       初始化客户端。优先使用传入参数，如果未提供，则从环境变量加载。
       """
        self.model = model or os.getenv("LLM_MODEL_ID")
        api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        base_url = base_url or os.getenv("DASHSCOPE_BASE_URL")
        timeout = timeout or int(os.getenv("DASHSCOPE_TIMEOUT", 60))
        if not all([self.model, api_key, base_url]):
            raise ValueError("请提供有效的模型ID、API密钥和基础URL")
        self.client = ChatQwen(model=self.model, api_key=api_key, base_url=base_url, timeout=timeout)

    def think(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
        """
        调用大语言模型进行思考，并返回其响应。
        """
        print(f"🧠 正在调用 {self.model} 模型...")
        try:
            # 将消息转换为 LangChain 格式
            from langchain_core.messages import HumanMessage, SystemMessage

            langchain_messages = []
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "system":
                    langchain_messages.append(SystemMessage(content=content))
                elif role == "user":
                    langchain_messages.append(HumanMessage(content=content))
                else:
                    langchain_messages.append(HumanMessage(content=content))

            # 使用 LangChain 的 stream 方法进行流式调用
            response_stream = self.client.stream(langchain_messages)

            # 处理流式响应
            print("✅ 大语言模型响应成功:")
            collected_content = []
            for chunk in response_stream:
                if chunk.content:
                    print(chunk.content, end="", flush=True)
                    collected_content.append(chunk.content)
            print()  # 在流式输出结束后换行
            return "".join(collected_content)

        except Exception as e:
            print(f"❌ 调用LLM API时发生错误: {e}")
            return None


# --- 客户端使用示例 ---
if __name__ == '__main__':
    try:
        llmClient = HelloAgentsLLM()

        exampleMessages = [
            {"role": "system", "content": "You are a helpful assistant that writes Python code."},
            {"role": "user", "content": "写一个快速排序算法"}
        ]

        print("--- 调用LLM ---")
        responseText = llmClient.think(exampleMessages)
        if responseText:
            print("\n\n--- 完整模型响应 ---")
            print(responseText)

    except ValueError as e:
        print(e)
