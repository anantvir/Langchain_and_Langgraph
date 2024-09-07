import operator
from typing import Annotated, TypedDict, Union

from langchain_core.agents import AgentAction, AgentFinish


class AgentState(TypedDict):
    input: str
    agent_outcome: Union[AgentAction, AgentFinish, None]

    # operator.add adds the new value of intermediate_steps to existing value
    # old value of intermediate_steps -> goes as input to a node -> new value of intermediate_steps calculated
    # -> new value added to existing value of intermediate_steps -> node returns new state with updated value of intermediate_steps
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]
