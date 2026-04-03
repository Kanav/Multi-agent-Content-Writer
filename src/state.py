from typing import TypedDict, Literal, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class CopyWriter(TypedDict):
  user_input: str           # The original user request
  route: Literal["seo_blog_writer", "x_blog_writer", "general"]  # Router's decision
  output: str               # Final output from the selected agent
  messages: Annotated[list[BaseMessage], add_messages]


if __name__ == "__main__":
    # Example usa
    example_copywriter_data = CopyWriter(
        user_input="Write a blog post about the benefits of AI in healthcare.",
        route="seo_blog_writer",
        output="AI in healthcare can improve diagnostics, personalize treatment, and enhance patient care...",
        messages=[
            # Example messages that would be added to the graph
        ]
    )
    print(example_copywriter_data)
