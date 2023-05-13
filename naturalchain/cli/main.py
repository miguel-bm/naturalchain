import enum

import click
import typer
from langchain.agents import AgentExecutor
from rich.console import Console
from rich.traceback import install
from typing_extensions import Annotated

from naturalchain.agents.structured_chat import get_structured_chat_agent_from_tools
from naturalchain.tools import (
    CoinInformationRetrieverTool,
    IdentifyContractTool,
    PythonCalculatorTool,
    RPCTool,
    SignTransactionTool,
    SmartContractCompilerTool,
    SmartContractDeployerTool,
    SmartContractWriterTool,
)

install(suppress=[click])
app = typer.Typer()


class StructuredChatAgent(str, enum.Enum):
    full = "full"
    smart_contract = "smart-contract"
    information_retrieval = "information-retrieval"


FULL_TOOLSET = [
    PythonCalculatorTool(),
    RPCTool(),
    IdentifyContractTool(),
    SignTransactionTool(),
    CoinInformationRetrieverTool(),
    SmartContractWriterTool(),
    SmartContractCompilerTool(),
    SmartContractDeployerTool(),
]

SMART_CONTRACT_TOOLSET = [
    SmartContractWriterTool(),
    SmartContractCompilerTool(),
    SmartContractDeployerTool(),
]

RETRIEVAL_TOOLSET = [
    PythonCalculatorTool(),
    RPCTool(),
    IdentifyContractTool(),
    CoinInformationRetrieverTool(),
]

TOOLSET_MAP = {
    StructuredChatAgent.full: FULL_TOOLSET,
    StructuredChatAgent.smart_contract: SMART_CONTRACT_TOOLSET,
    StructuredChatAgent.information_retrieval: RETRIEVAL_TOOLSET,
}


def get_agent(
    agent_type: StructuredChatAgent,
    verbose: bool,
    model_name: str,
    temperature: float,
) -> AgentExecutor:
    if agent_type not in StructuredChatAgent:
        raise ValueError(f"Invalid agent type: {agent_type}")
    toolset = TOOLSET_MAP[agent_type]
    agent = get_structured_chat_agent_from_tools(
        tools=toolset,
        verbose=verbose,
        model_name=model_name,
        temperature=temperature,
    )
    return agent


@app.command(name="query")
def query_command(
    query: Annotated[
        str, typer.Argument(..., help="Your query or task for the NaturalChain agent")
    ],
    agent: Annotated[
        StructuredChatAgent,
        typer.Option(
            help="Specify which agent to use (default or smart_contract)",
        ),
    ] = StructuredChatAgent.full,
    model_name: Annotated[
        str,
        typer.Option(
            help="Specify which model to use (gpt-3.5-turbo or gpt-4)",
        ),
    ] = "gpt-3.5-turbo",
    temperature: Annotated[
        float,
        typer.Option(
            help="Specify the temperature for the model (default 0.0)",
        ),
    ] = 0.0,
    verbose: Annotated[bool, typer.Option(help="Display verbose output")] = False,
):
    """
    NaturalChain agent CLI
    """
    console = Console()
    try:
        agent_instance = get_agent(agent, verbose, model_name, temperature=temperature)
        response = agent_instance.run(query)
        typer.echo(response)
    except Exception as e:
        console.print_exception(max_frames=0)


@app.command(name="chat")
def chat_command(
    agent: Annotated[
        StructuredChatAgent,
        typer.Option(
            help="Specify which agent to use (default or smart_contract)",
        ),
    ] = StructuredChatAgent.full,
    model_name: Annotated[
        str,
        typer.Option(
            help="Specify which model to use (gpt-3.5-turbo or gpt-4)",
        ),
    ] = "gpt-3.5-turbo",
    temperature: Annotated[
        float,
        typer.Option(
            help="Specify the temperature for the model (default 0.0)",
        ),
    ] = 0.0,
    verbose: Annotated[bool, typer.Option(help="Display verbose output")] = False,
) -> None:
    console = Console()
    typer.echo(
        "You are now chatting with the NaturalChain agent. Type 'exit' to finish the chat."
    )
    agent_instance = get_agent(agent, verbose, model_name, temperature=temperature)
    try:
        while True:
            query = typer.prompt("You")
            if query == "exit":
                break
            response = agent_instance.run(query)
            typer.echo(f"NaturalChain: {response}")
    except Exception as e:
        console.print_exception(max_frames=0)


if __name__ == "__main__":
    app()
