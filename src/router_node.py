from langchain.messages import HumanMessage, SystemMessage, AIMessage

router_instructions = """
  You are a smart router. Your job is to classify the user's request.

  If the user wants a long-form blog post, article, or detailed content → respond with: seo_blog_writer
  If the user wants a short tweet, X post, or social media content → respond with: x_blog_writer
  If the user's request is a general question, greeting, or anything NOT related to content writing → respond with: general

  Respond with ONLY one word: either seo_blog_writer, x_blog_writer, or general"""
from src.llm_setup import get_llm
from src.state import CopyWriter


def router_node(state: CopyWriter):
    """Route user input to the appropriate content generation agent."""
    llm = get_llm()

    messages = [
        SystemMessage(content=router_instructions),
        HumanMessage(content=state.get("user_input", ""))
    ]

    result = llm.invoke(messages)
    route = result.content.strip().lower()

    # Persist user input into messages for history tracking
    return {
        "route": route,
        "messages": [HumanMessage(content=state.get("user_input", ""))],
    }

if __name__ == "__main__":
    test_cases = [
        "Write a detailed blog post about AI in healthcare",
        "Write a tweet about our new product launch",
        "Create an in-depth article on climate change",
        "Make a short X post announcing our funding round",
        "Hi, how are you?",
    ]
    for test in test_cases:
        state = {"user_input": test, "route": "", "output": ""}
        result = router_node(state)
        print(f"Input: {test}\nRoute: {result['route']}\n")