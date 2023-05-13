from typing import List

from decouple import config
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool

OPENAI_API_KEY = config("OPENAI_API_KEY")


def get_structured_chat_agent_from_tools(
    tools: List[BaseTool],
    verbose: bool = False,
    model_name: str = "gpt-3.5-turbo",
    temperature: float = 0.0,
):
    return initialize_agent(
        tools=tools,
        llm=ChatOpenAI(temperature=temperature, openai_api_key=OPENAI_API_KEY, model_name=model_name),  # type: ignore
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=verbose,
    )
