from decouple import config
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI

from naturalchain.tools.smart_contract_writer.tool import SmartContractWriterTool
from naturalchain.tools.smart_contract_compiler.tool import SmartContractCompilerTool
from naturalchain.tools.smart_contract_deployer.tool import SmartContractDeployerTool

OPENAI_API_KEY = config("OPENAI_API_KEY")


def get_smart_contract_agent(
    verbose: bool = False,
    model_name: str = "gpt-3.5-turbo",
    temperature: float = 0.0,
):
    return initialize_agent(
        tools=[
            SmartContractWriterTool(),
            SmartContractCompilerTool(),
            SmartContractDeployerTool(),
        ],
        llm=ChatOpenAI(temperature=temperature, openai_api_key=OPENAI_API_KEY, model_name=model_name),  # type: ignore
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=verbose,
    )
