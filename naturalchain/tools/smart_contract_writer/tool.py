from pathlib import Path
from typing import Optional, Type

from decouple import config
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from naturalchain.utils import (
    extract_first_code_block,
    preprocess_solidity_code,
    save_to_text_file,
    get_datetime_string,
)

SYSTEM_MESSAGE = "You are a world class smart contract developer that creates EVM-compatible Solidity code given a description of a desired Smart Contract."
HUMAN_MESSAGE_TEMPLATE = (
    "Please write the code for a smart contract in Solidity that conforms to the following description. "
    "Use Open Zeppelin libraries if appropriate. Comment the contract using natspec. "
    "Description:\n"
    "{description}\n\n"
    "Output a single code block within backticks containing the Solidity code."
)


smart_contract_writer_chain = LLMChain(
    llm=ChatOpenAI(openai_api_key=config("OPENAI_API_KEY")),  # type: ignore
    prompt=ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(SYSTEM_MESSAGE),
            HumanMessagePromptTemplate.from_template(HUMAN_MESSAGE_TEMPLATE),
        ]
    ),
)


class SmartContractWriterToolInput(BaseModel):
    description: str = Field(
        description="A detailed description of the smart contract, including its purpose, its functions, and its variables"
    )


class SmartContractWriterTool(BaseTool):
    name = "SmartContractWriter"
    description = "Useful for writing EVM-compatible smart contracts given a description. Returns the path to the .sol file."
    args_schema: Type[BaseModel] = SmartContractWriterToolInput

    def _run(
        self,
        description: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        chain_result = smart_contract_writer_chain.run(description)
        code_block = extract_first_code_block(chain_result)
        code_block = preprocess_solidity_code(code_block)

        output_path = Path("smart_contracts")
        output_path.mkdir(exist_ok=True, parents=True)
        file_name = f"smart_contract_{get_datetime_string()}.sol"

        save_to_text_file(code_block, output_path, file_name)
        absolute_path_str = str((output_path / file_name).absolute())
        return absolute_path_str

    async def _arun(
        self,
        description: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("This tool does not support async mode.")
