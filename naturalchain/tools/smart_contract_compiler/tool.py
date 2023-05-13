import json
from pathlib import Path
from typing import Optional, Type

import solcx
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class SmartContractCompilerToolInput(BaseModel):
    path_to_sol_file: str = Field(
        description="The path to the .sol file containing the smart contract code"
    )


class SmartContractCompilerTool(BaseTool):
    name = "SmartContractCompiler"
    description = "Useful for compiling EVM-compatible smart contracts a path to a .sol file. Returns the path to the .bin file."
    args_schema: Type[BaseModel] = SmartContractCompilerToolInput

    def _run(
        self,
        path_to_sol_file: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        # Read the Solidity source code
        compiler_output = solcx.compile_files(
            [path_to_sol_file],
            output_values=["abi", "bin-runtime", "bin"],
        )
        abi = compiler_output[list(compiler_output.keys())[0]]["abi"]
        abi_json_path = Path(path_to_sol_file.replace(".sol", "-abi.json"))
        with abi_json_path.open("w") as f:
            json.dump(abi, f, indent=4)

        bin_str = compiler_output[list(compiler_output.keys())[0]]["bin"]
        bin_path = Path(path_to_sol_file.replace(".sol", "-bin"))
        with bin_path.open("w") as f:
            f.write(bin_str)

        return str(bin_path)

    async def _arun(
        self,
        description: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("This tool does not support async mode.")


if __name__ == "__main__":
    tool = SmartContractCompilerTool()
    oz_path = "/Users/miguel/Developer/projects/naturalchain/smart_contracts/smart_contract_2023-05-12-22-11-09.sol"
    no_oz_path = "/Users/miguel/Developer/projects/naturalchain/smart_contracts/smart_contract_2023-05-12-14-27-27.sol"
    tool._run(path_to_sol_file=oz_path)
