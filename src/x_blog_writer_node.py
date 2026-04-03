from src.state import CopyWriter
from src.llm_setup import get_llm
from src.general_internet_search_tavily import internet_search
from langchain.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import ToolNode
# X blog writer — uses messages for tool loop

x_tools = [internet_search]

def x_blog_writer_node(state: CopyWriter):
    llm = get_llm()
    x_writer_with_tools = llm.bind_tools(x_tools)
# X Blog Writer with tools
    x_blog_instructions = """
You are an expert X (Twitter) content writer with access to tools.

You have one tool:
1. internet_search_tool — Use this to find trending topics, viral headlines, and popular hashtags related to the user's request.

Workflow:
- First, use internet_search_tool to find trending topics and hashtags.
- Then, write an engaging, viral-worthy X post using those insights.

Rules:
- Keep it under 280 characters
- Use punchy, attention-grabbing language
- Include trending and relevant hashtags
- Add emojis where appropriate
- Make it shareable and engaging
"""
    if not state.get("messages"):
        messages = [
            SystemMessage(content=x_blog_instructions),
            HumanMessage(content=state["user_input"])
        ]
    else:
        messages = state["messages"]

    result = x_writer_with_tools.invoke(messages)

    if result.tool_calls:
        return {"messages": [*messages, result] if not state.get("messages") else [result]}
    else:
        return {"output": result.content, "messages": [result]}

def x_tool_node(state):
    return ToolNode(tools=x_tools)

if __name__ == "__main__":
    # Example usage
    state = CopyWriter(user_input="Write a viral X post about the benefits of meditation.")
    result = x_blog_writer_node(state)
    print(result)    