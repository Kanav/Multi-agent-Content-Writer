from langgraph.graph import StateGraph
from langgraph.graph.state import END
from src.conditional_edges import route_decision, seo_should_continue, x_should_continue
from src.general_node import general_node
from src.seo_blog_writer_node import seo_blog_writer_node, seo_tool_node
from src.state import CopyWriter
from src.router_node import router_node
from src.x_blog_writer_node import x_blog_writer_node, x_tool_node
from langgraph.checkpoint.memory import MemorySaver
from IPython.display import display, Image

def graph():
    workflow = StateGraph(CopyWriter)
    workflow.add_node("router", router_node)
    workflow.add_node("seo_blog_writer", seo_blog_writer_node)
    workflow.add_node("x_blog_writer", x_blog_writer_node)
    workflow.add_node("tools", seo_tool_node)
    workflow.add_node("x_tools", x_tool_node)
    workflow.add_node("general", general_node)

    workflow.set_entry_point("router")

    workflow.add_conditional_edges("router", route_decision, {
    "seo_blog_writer": "seo_blog_writer",
    "x_blog_writer": "x_blog_writer",
    "general": "general",
})
    
    # SEO agent ↔ tools loop
    workflow.add_conditional_edges("seo_blog_writer", seo_should_continue, {"tools": "tools", "end": END})
    workflow.add_edge("tools", "seo_blog_writer")

    # X agent ↔ tools loop
    workflow.add_conditional_edges("x_blog_writer", x_should_continue, {"x_tools": "x_tools", "end": END})
    workflow.add_edge("x_tools", "x_blog_writer")

    workflow.add_edge("general", END)

    memory = MemorySaver()

    graph = workflow.compile(checkpointer=memory)
    return graph


if __name__ == "__main__":
    graph = graph()
    # Generate the PNG data
    png_data = graph.get_graph().draw_mermaid_png()

    # Save it to a file
    with open("graph.png", "wb") as f:
        f.write(png_data)

    # Optionally display it in a notebook
    display(Image(filename="graph.png"))



