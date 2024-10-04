from typing import List, TypedDict, Union, Annotated, Tuple
from langchain_core.messages import BaseMessage
from langchain_core.agents import AgentAction, AgentFinish
import operator

class EntryGraphState(TypedDict):
    """
        represents state of the graph
    """
    user_query : str
    category : str = None
    sentiment : str = None
    current_conversation_history : List[BaseMessage] = None
    resolution_status : bool = None
    esclation_decision : bool = None

class PhoneGraphState(TypedDict):
    """
    Represents state of phone agent
    """
    user_query : str
    resolution_status : bool = None
    esclation_decision : bool = None
    phone_agent_outcome : Union[AgentAction, AgentFinish] = None # AgentAction consists of name of tool to run, inputs to that tool and intermediate steps taken so far
    phone_agent_intermediate_steps : Annotated[List[Tuple[AgentAction, str]], operator.add] = None # operator.add ensures intermediate_steps not overwritten instead its always appended to

class InternetGraphState(TypedDict):
    """
    Represents state of internet agent
    """
    user_query : str
    resolution_status : bool = None
    esclation_decision : bool = None
    internet_agent_outcome : Union[AgentAction, AgentFinish] = None
    internet_agent_intermediate_steps : Annotated[List[Tuple[AgentAction, str]], operator.add] = None # operator.add ensures intermediate_steps not overwritten instead its always appended to

class IotGraphState(TypedDict):
    """
    Represents state of iot agent
    """
    user_query : str
    resolution_status : bool = None
    esclation_decision : bool = None
    iot_agent_outcome : Union[AgentAction, AgentFinish] = None
    iot_agent_intermediate_steps : Annotated[List[Tuple[AgentAction, str]], operator.add] = None # operator.add ensures intermediate_steps not overwritten instead its always appended to







