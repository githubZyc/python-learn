"""Agent 消息格式化输出工具"""


def message_format(response: dict) -> None:
    """
    格式化打印 LangGraph Agent 的响应消息。

    Args:
        response: agent.invoke() 返回的响应字典，需包含 "messages" 键
    """
    print("=" * 60)
    print("📊 LangGraph Agent 结构化输出")
    print("=" * 60)

    # 获取消息列表
    messages = response.get("messages", [])

    # 遍历所有消息
    for i, msg in enumerate(messages):
        print(f"\n{'─' * 60}")
        print(f"📨 消息 [{i + 1}/{len(messages)}]")
        print(f"{'─' * 60}")

        # 消息类型
        msg_type = type(msg).__name__
        print(f"📌 类型: {msg_type}")

        # 消息内容
        if hasattr(msg, 'content'):
            print(f"💬 内容: {msg.content}")

        # HumanMessage 特有信息
        if msg_type == "HumanMessage":
            pass  # HumanMessage 通常只有内容

        # AIMessage 特有信息
        elif msg_type == "AIMessage":
            # 工具调用
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                print(f"\n🔧 工具调用:")
                for tool_call in msg.tool_calls:
                    print(f"   • 工具名称: {tool_call.get('name', 'N/A')}")
                    print(f"   • 参数: {tool_call.get('args', {})}")

            # 无效工具调用
            if hasattr(msg, 'invalid_tool_calls') and msg.invalid_tool_calls:
                print(f"\n⚠️  无效工具调用: {len(msg.invalid_tool_calls)}")

            # Token 使用统计
            if hasattr(msg, 'usage_metadata') and msg.usage_metadata:
                usage = msg.usage_metadata
                print(f"\n📈 Token 使用统计:")
                print(f"   • 输入 Tokens: {usage.get('input_tokens', 'N/A')}")
                print(f"   • 输出 Tokens: {usage.get('output_tokens', 'N/A')}")
                print(f"   • 总计 Tokens: {usage.get('total_tokens', 'N/A')}")

                # 输入 token 详情
                input_details = usage.get('input_token_details', {})
                if input_details:
                    print(f"   • 缓存读取: {input_details.get('cache_read', 0)}")

            # 响应元数据
            if hasattr(msg, 'response_metadata') and msg.response_metadata:
                metadata = msg.response_metadata
                print(f"\n🔍 响应元数据:")
                print(f"   • 模型: {metadata.get('model_name', 'N/A')}")
                print(f"   • 提供商: {metadata.get('model_provider', 'N/A')}")
                print(f"   • 完成原因: {metadata.get('finish_reason', 'N/A')}")
                print(f"   • 响应 ID: {metadata.get('id', 'N/A')}")

                # Token 详情
                token_usage = metadata.get('token_usage', {})
                if token_usage:
                    print(f"\n   📊 详细 Token 统计:")
                    print(f"      - 完成 Tokens: {token_usage.get('completion_tokens', 'N/A')}")
                    print(f"      - 提示 Tokens: {token_usage.get('prompt_tokens', 'N/A')}")
                    print(f"      - 总 Tokens: {token_usage.get('total_tokens', 'N/A')}")

                    # 缓存信息
                    prompt_details = token_usage.get('prompt_tokens_details', {})
                    if prompt_details:
                        cached = prompt_details.get('cached_tokens', 0)
                        print(f"      - 缓存 Tokens: {cached}")

    print(f"\n{'=' * 60}")
    print(f"✅ 共处理 {len(messages)} 条消息")
    print(f"{'=' * 60}")
