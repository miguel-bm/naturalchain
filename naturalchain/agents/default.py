from decouple import config
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from naturalchain.tools.smart_contract_writer.tool import SmartContractWriterTool
from naturalchain.tools.calculator.tool import PythonCalculatorTool

OPENAI_API_KEY = config("OPENAI_API_KEY")


naturalchain_agent = initialize_agent(
    tools=[
        SmartContractWriterTool(),
        PythonCalculatorTool(),
    ],
    llm=ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY),  # type: ignore
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
