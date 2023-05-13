import json
from pathlib import Path
from typing import Optional, Type

import solcx
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import List, Dict


def get_remappings(
    libs: List[str],
    relative_path: str = "node_modules",
) -> Dict[str, str]:
    home_path = Path.home()
    return {
        f"@{lib}": str((home_path / f"{relative_path}/@{lib}").absolute())
        for lib in libs
    }


def find_main_contract(
    compiler_output: Dict[str, Dict[str, Dict[str, str]]],
    original_file_name: str,
) -> str:
    main_file_contracts: List[str] = []
    for file_name, file_data in compiler_output.items():
        if original_file_name in file_name:
            main_file_contracts.append(file_name)
    max_len_bin = ""
    main_contract = None
    for main_file_contract in main_file_contracts:
        if compiler_output[main_file_contract]["bin"]:
            if len(compiler_output[main_file_contract]["bin"]) > len(max_len_bin):
                max_len_bin = compiler_output[main_file_contract]["bin"]
                main_contract = main_file_contract

    if main_contract:
        return main_contract

    raise ValueError("No Main contract found.")


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
        home_path = Path.home()
        compiler_output = solcx.compile_files(
            [path_to_sol_file],
            output_values=["abi", "bin-runtime", "bin"],
            import_remappings=get_remappings(["openzeppelin", "chainlink"]),
        )

        sol_file_name = Path(path_to_sol_file).name
        main_contract = find_main_contract(compiler_output, sol_file_name)

        full_json_path = Path(path_to_sol_file.replace(".sol", ".json"))
        with full_json_path.open("w") as f:
            json.dump(compiler_output, f, indent=4)

        abi = compiler_output[main_contract]["abi"]
        abi_json_path = Path(path_to_sol_file.replace(".sol", "-abi.json"))
        with abi_json_path.open("w") as f:
            json.dump(abi, f, indent=4)

        bin_str = compiler_output[main_contract]["bin"]
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
