from src.state import CopyWriter
# Conditional edges — check if agent wants more tools or is done
def seo_should_continue(state: CopyWriter):
    last_msg = state["messages"][-1]
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "tools"
    return "end"

def x_should_continue(state: CopyWriter):
    last_msg = state["messages"][-1]
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "x_tools"
    return "end"

def route_decision(state: CopyWriter):
    return state["route"]