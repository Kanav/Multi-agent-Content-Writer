# General node — router handles it directly
from src.llm_setup import get_llm
from langchain.messages import HumanMessage, SystemMessage, AIMessage
from src.state import CopyWriter

def general_node(state: CopyWriter):
    llm = get_llm()
    # Build conversation history from persisted messages
    history = state.get("messages", [])

    system = SystemMessage(content="""You are a helpful assistant. You have access to the full conversation history.
    Answer the user's question briefly and clearly using context from previous messages if relevant.
    Let them know you specialize in SEO blog writing and X/Twitter post writing if they need content.""")

    # Add current user input to history
    messages = [system] + history + [HumanMessage(content=state["user_input"])]

    result = llm.invoke(messages)

    # Save to messages so checkpointer persists it
    return {
        "output": result.content,
        "messages": [
            HumanMessage(content=state["user_input"]),
            AIMessage(content=result.content)
        ]
    }

if __name__ == "__main__":
    # Example usage
    state = CopyWriter(user_input="What can you do?")
    result = general_node(state)
    print(result)