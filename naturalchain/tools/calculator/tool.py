from typing import Any, Optional

from pydantic import Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool
from langchain.utilities import PythonREPL


def _get_default_python_repl() -> PythonREPL:
    return PythonREPL(_globals=globals(), _locals=None)


class PythonCalculatorTool(BaseTool):
    name = "PythonCalculator"
    description = (
        "Use this to solve mathematical computations. "
        "Input should be in valid python syntax, like `234**1.2 + 4`."
    )
    python_repl: PythonREPL = Field(default_factory=_get_default_python_repl)
    sanitize_input: bool = True

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        """Use the tool."""
        if self.sanitize_input:
            query = query.strip().strip("```").strip("`")

        printed_query = f"print({query})"
        return self.python_repl.run(printed_query)

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        """Use the tool asynchronously."""
        raise NotImplementedError("Calculator does not support async")
