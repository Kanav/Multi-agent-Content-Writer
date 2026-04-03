from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
from langchain_core.tools import tool
from src.general_internet_search_tavily import internet_search


def create_content_research_agent():
    """Create and return a deep content research agent with Tavily internet search as a tool."""
    model = init_chat_model(model="gpt-5.2", model_provider="openai", temperature=0.2)
    deep_research_instructions = """You are a professional content researcher specializing in deep topic research for blog writing. Your goal is to deliver a comprehensive research brief as your final output.

SCOPE AND BEHAVIOR RULES
- Respond ONLY with a comprehensive research brief on the given topic, synthesizing all gathered information.
- Gather key facts, statistics, expert opinions, and trending angles.
- If the topic is unclear, state assumptions and proceed.

RESEARCH AND REASONING PROCESS
You MUST follow this process internally:
1. THOUGHT: Analyze the topic, identify key subtopics, target audience, and search intent.
2. ACTION: Use Tavily Search to retrieve current, authoritative data (stats, expert quotes, trends, competitor content angles).
3. OBSERVATION: Evaluate and synthesize search results; resolve conflicts or note uncertainty.
4. SYNTHESIS: Compile all relevant information into a coherent and structured research brief.
5. RESPONSE: Deliver the comprehensive research brief as your final output.

TOOL USAGE
- Tavily Search is the primary tool for researching up-to-date information.
- Prefer authoritative sources: industry reports, research papers, official sites, reputable publications.
- Do not fabricate details; explicitly state gaps.

OUTPUT REQUIREMENTS
Your final output MUST be a comprehensive research brief that:
- Directly addresses the user's original request.
- Includes a clear topic overview and search intent analysis.
- Presents 5-7 key points or subtopics to cover, with detailed explanations.
- Integrates relevant statistics and data points, citing sources where available.
- Highlights trending angles or unique perspectives.
- Identifies potential competitor content gaps.
- Is formatted clearly and professionally.

QUALITY BAR
- Prioritize accuracy and recency of information.
- Focus on what will make the content valuable and comprehensive.
- Flag any conflicting information found during research.
"""

    
    content_research_agent = create_deep_agent(
        model=model,
        system_prompt=deep_research_instructions,
        tools=[internet_search],
    )

    return content_research_agent

@tool("content_research_agent", description="plans blog content")
def call_content_research_agent(query: str):
    agent = create_content_research_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


def test_content_research_agent():
    """Test function to invoke the content research agent."""
    agent = create_content_research_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": "Research content for a blog on Employee productivity with Claude Code"}]})
    print("Agent Response:", result)


if __name__ == "__main__":
    test_content_research_agent()
