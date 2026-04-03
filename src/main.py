


from src.graph import get_content_writer_graph


def TestMultiAgentContentWriter():
    config = {"configurable": {"thread_id": "session-1"}}
    # Test 1: SEO Blog
    print("=" * 60)
    print("TEST 1: SEO BLOG REQUEST")
    print("=" * 60)

    input_1 = {"user_input": "Write a detailed blog post about AI in healthcare", "route": "", "output": "", "messages": []}
    graph = get_content_writer_graph()

    for step in graph.stream(input_1, config):
        for node_name, node_output in step.items():
            print(f"\n--- Node: {node_name} ---")
            if node_name == "router":
                print(f"🧭 Route: {node_output['route']}")
            elif node_name in ["tools", "x_tools"]:
                for msg in node_output.get("messages", []):
                    print(f"🔧 Tool Result: {str(msg.content)[:200000]}...")
            else:
                if node_output.get("output"):
                    print(f"✅ Final Output:\n{node_output['output'][:500000]}...")
                else:
                    last = node_output["messages"][-1]
                    if hasattr(last, "tool_calls"):
                        for tc in last.tool_calls:
                            print(f"🤖 Agent requesting: {tc['name']}({tc['args']})")

    
def TestXBlogWriter():
    # Test 2: X Post
    print("=" * 60)
    print("TEST 2: X POST REQUEST")
    print("=" * 60)

    input_2 = {"user_input": "Write a tweet about our new product launch", "route": "", "output": "", "messages": []}

    for step in graph.stream(input_2, config):
        for node_name, node_output in step.items():
            print(f"\n--- Node: {node_name} ---")
            if node_name == "router":
                print(f"🧭 Route: {node_output['route']}")
            elif node_name in ["tools", "x_tools"]:
                for msg in node_output.get("messages", []):
                    print(f"🔧 Tool Result: {str(msg.content)[:200000]}...")
            else:
                if node_output.get("output"):
                    print(f"✅ Final Output:\n{node_output['output'][:5000000]}...")
                else:
                    last = node_output["messages"][-1]
                    if hasattr(last, "tool_calls"):
                        for tc in last.tool_calls:
                            print(f"🤖 Agent requesting: {tc['name']}({tc['args']})")

    
def TestGeneralWriter():
    # Test 3:
    print("=" * 60)
    print("TEST 3")
    print("=" * 60)

    input_3 = {"user_input": "What was my recent ask?", "route": "", "output": "", "messages": []}

    for step in graph.stream(input_3, config):
        for node_name, node_output in step.items():
            print(f"\n--- Node: {node_name} ---")
            if node_name == "router":
                print(f"🧭 Route: {node_output['route']}")
            elif node_name in ["tools", "x_tools"]:
                for msg in node_output.get("messages", []):
                    print(f"🔧 Tool Result: {str(msg.content)[:200000]}...")
            else:
                if node_output.get("output"):
                    print(f"✅ Final Output:\n{node_output['output'][:5000000]}...")
                else:
                    last = node_output["messages"][-1]
                    if hasattr(last, "tool_calls"):
                        for tc in last.tool_calls:
                            print(f"🤖 Agent requesting: {tc['name']}({tc['args']})")


if __name__ == "__main__":
    TestMultiAgentContentWriter()