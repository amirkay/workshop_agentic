"""
LangGraph multi-agent system for fitness coaching
"""
import os
from typing import Literal, List, Annotated
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.types import Command
from langchain.tools import tool

from dotenv import load_dotenv
load_dotenv()

from core.prompts import NUTRITIONIST_PROMPT, TRAINER_PROMPT, MASTERMIND_PROMPT
from core.tools import calculate_maintenance_calories, create_workout_plan

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-5-nano-2025-08-07",
    temperature=0,
)

def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END


def call_model_wrapper(model_with_tools, system_prompt: str):
    def call_model(state: MessagesState):
        messages = state["messages"]

        if not any(isinstance(m, SystemMessage) for m in messages):
            messages = [SystemMessage(content=system_prompt)] + messages

        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    return call_model


def create_agent(
    model: ChatOpenAI,
    tools: list,
    system_prompt: str,
):
    """
    Generic helper to create a LangGraph agent with tools
    """
    model_with_tools = model.bind_tools(
        tools=tools,
        parallel_tool_calls=False
    )

    workflow = StateGraph(MessagesState)

    workflow.add_node(
        "agent",
        call_model_wrapper(model_with_tools, system_prompt)
    )
    workflow.add_node("tools", ToolNode(tools=tools))

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue, ["tools", END])
    workflow.add_edge("tools", "agent")

    return workflow.compile()


nutritionist_agent = create_agent(
    model=llm,
    tools=[calculate_maintenance_calories],
    system_prompt=NUTRITIONIST_PROMPT,
)

trainer_agent = create_agent(
    model=llm,
    tools=[create_workout_plan],
    system_prompt=TRAINER_PROMPT,
)


# Tool wrappers that call the worker agents so they can be passed as tools
@tool
def nutritionist_tool(query: str) -> str:
    """Call the nutritionist agent with a simple query and return its final text."""
    initial_state = {"messages": [HumanMessage(content=query)]}
    result = nutritionist_agent.invoke(initial_state)

    final_response = ""
    for msg in reversed(result.get("messages", [])):
        if isinstance(msg, AIMessage) and not msg.tool_calls:
            final_response = msg.content
            break

    return final_response


@tool
def trainer_tool(query: str) -> str:
    """Call the trainer agent with a simple query and return its final text."""
    initial_state = {"messages": [HumanMessage(content=query)]}
    result = trainer_agent.invoke(initial_state)

    final_response = ""
    for msg in reversed(result.get("messages", [])):
        if isinstance(msg, AIMessage) and not msg.tool_calls:
            final_response = msg.content
            break

    return final_response



mastermind_agent = create_agent(
        model=llm,
        tools=[nutritionist_tool, trainer_tool],
        system_prompt=MASTERMIND_PROMPT,
    )


def extract_tool_logs(messages: List[BaseMessage]) -> List[str]:
    """
    Extract readable logs from tool calls for UI display
    """
    logs = []

    for msg in messages:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            for call in msg.tool_calls:
                logs.append(
                    f"🔧 Tool called: `{call['name']}`\n"
                    f"Arguments: {call['args']}"
                )

    return logs




def run_agent(user_message: str):
    initial_state = {
        "messages": [HumanMessage(content=user_message)]
    }

    result = mastermind_agent.invoke(initial_state, {"recursion_limit": 5})
    messages = result["messages"]

    final_answer = ""
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and not msg.tool_calls:
            final_answer = msg.content
            break

    logs = extract_tool_logs(messages)

    return final_answer, logs


