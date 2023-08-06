from typing import Any, Dict, List, Optional

import pyspark
from langchain.llms.base import BaseLLM
from langchain.callbacks.base import BaseCallbackManager
from langchain.agents.agent import AgentExecutor
from langchain.agents.agent_toolkits.spark.base import _validate_spark_connect_df, _validate_spark_df
from langchain.tools.python.tool import PythonAstREPLTool
from langchain.agents.mrkl.base import ZeroShotAgent
from langchain.chains.llm import LLMChain


PREFIX = """
You are working with a list of spark dataframes in Python. The name of the dataframes are `{dataframe_names}`.
You should use the tools below to answer the question posed of you:"""

SUFFIX = """
This is the result of `print(df.first())`:
{dataframe_names}

Begin!
Question: {input}
{agent_scratchpad}"""


def create_multiple_spark_dataframes_agent(
    llm: BaseLLM,
    dataframes_dict: Dict[str, pyspark.sql.DataFrame],
    callback_manager: Optional[BaseCallbackManager] = None,
    prefix: str = PREFIX,
    suffix: str = SUFFIX,
    input_variables: Optional[List[str]] = None,
    verbose: bool = False,
    return_intermediate_steps: bool = False,
    max_iterations: Optional[int] = 15,
    max_execution_time: Optional[float] = None,
    early_stopping_method: str = "force",
    agent_executor_kwargs: Optional[Dict[str, Any]] = None,
    **kwargs: Dict[str, Any],
) -> AgentExecutor:
    """Construct a spark agent from an LLM and dataframe."""

    valid_dataframes = all([_validate_spark_df(df) for df in dataframes_dict.values()])
    valid_spark_connect = all([_validate_spark_connect_df(df) for df in dataframes_dict.values()])

    if not valid_dataframes and not valid_spark_connect:
        raise ValueError("Spark is not installed. run `pip install pyspark`.")

    prefix = PREFIX.format(dataframe_names="`, `".join([f"{key}" for key in dataframes_dict.keys()]))
    
    suffix = SUFFIX.format(
        dataframe_names=", ".join([f"{{{key}}}" for key in dataframes_dict.keys()]),
        input="{input}",
        agent_scratchpad="{agent_scratchpad}",
    )

    if input_variables is None:
        input_variables = list(dataframes_dict.keys()) + ["input", "agent_scratchpad"]
    
        
    tools = [PythonAstREPLTool(locals=dataframes_dict)]

    prompt = ZeroShotAgent.create_prompt(
        tools, prefix=prefix, suffix=suffix, input_variables=input_variables
    )

    promp_opts = {key: str(value.first()) for key, value in dataframes_dict.items()}
    partial_prompt = prompt.partial(**promp_opts)
    llm_chain = LLMChain(
        llm=llm,
        prompt=partial_prompt,
        callback_manager=callback_manager,
    )
    tool_names = [tool.name for tool in tools]
    agent = ZeroShotAgent(
        llm_chain=llm_chain,
        allowed_tools=tool_names,
        callback_manager=callback_manager,
        **kwargs,
    )
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        callback_manager=callback_manager,
        verbose=verbose,
        return_intermediate_steps=return_intermediate_steps,
        max_iterations=max_iterations,
        max_execution_time=max_execution_time,
        early_stopping_method=early_stopping_method,
        **(agent_executor_kwargs or {}),
    )