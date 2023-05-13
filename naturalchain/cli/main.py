import enum

import click
import typer
from langchain.agents import AgentExecutor
from rich.traceback import install
from typing_extensions import Annotated

from naturalchain.agents.default import get_naturalchain_agent
from naturalchain.agents.smart_contract_agent import get_smart_contract_agent
from rich.console import Console

install(suppress=[click])
app = typer.Typer()


class Agent(str, enum.Enum):
    default = "default"
    smart_contract = "smart-contract"


def get_agent(
    agent: Agent, verbose: bool, model_name: str, temperature: float
) -> AgentExecutor:
    if agent == Agent.default:
        return get_naturalchain_agent(
            verbose=verbose, model_name=model_name, temperature=temperature
        )
    elif agent == Agent.smart_contract:
        return get_smart_contract_agent(
            verbose=verbose, model_name=model_name, temperature=temperature
        )
    else:
        raise ValueError(f"Invalid agent: {agent}")


@app.command()
def main(
    query: Annotated[
        str, typer.Argument(..., help="Your query or task for the NaturalChain agent")
    ],
    agent: Annotated[
        Agent,
        typer.Option(
            help="Specify which agent to use (default or smart_contract)",
        ),
    ] = Agent.default,
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


if __name__ == "__main__":
    app()
