from src.llm_setup import get_llm
from src.state import CopyWriter
from src.general_internet_search_tavily import internet_search
from src.deep_content_research_sub_agent import call_content_research_agent
from langchain.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import ToolNode

tools = [call_content_research_agent, internet_search]

def seo_blog_writer_node(state: CopyWriter):
    llm = get_llm()
    
    blog_writer_with_tools = llm.bind_tools(tools)
    seo_blog_instructions = """
You are an expert SEO blog writer with access to tools.

You have two tools:
1. research_tool — Use this to find content, references, and insights to enrich the blog.
2. internet_search_tool — Use this to check SEO keywords, trending terms, and optimize content.

Workflow:
- First, use research_tool to gather relevant content.
- Then, use internet_search_tool to find the best SEO keywords.
- Finally, write a well-structured, keyword-optimized blog post.

Include: compelling title, introduction, H2/H3 subheadings, structured paragraphs, and a CTA.
"""
    # First call: seed messages from user_input
    if not state.get("messages"):
        messages = [
            SystemMessage(content=seo_blog_instructions),
            HumanMessage(content=state["user_input"])
        ]
    else:
        messages = state["messages"]

    result = blog_writer_with_tools.invoke(messages)

    if result.tool_calls:
        return {"messages": [*messages, result] if not state.get("messages") else [result]}
    else:
        return {"output": result.content, "messages": [result]}
    

def seo_tool_node(state):
    return ToolNode(tools=tools)


if __name__ == "__main__":
    # Example usage
    state = CopyWriter(user_input="Write an SEO blog post about the benefits of meditation.")
    result = seo_blog_writer_node(state)
    print(result)
