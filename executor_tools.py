from tools import read_file
from typing import Literal,Any
from pydantic import BaseModel

mapping_tools={
    "read_file":read_file
}


class StepState(BaseModel):
    step_number: int
    tools: str
    query: str
    args: dict[str, Any]
    status: Literal["success", "failed"]
    result: Any = None
    error: Any = None

class Executor_State(BaseModel):
    goal:str
    step_state:list[StepState]
    total_steps: int

def executor_tools(plan):
    state_step=[]

    for i,item in enumerate(plan.steps,start=1):
        tools=item.tools
        query_plan=item.query
        args=item.args

        run_tools=mapping_tools[tools]

        result_tools=run_tools.invoke(args)

        if "ERROR" in result_tools:
            result_state=None
            status='failed'
            error=result_tools

        else:
            result_state=result_tools
            status='success'
            error=None

        state=StepState(
                step_number=i,
                tools=tools,
                query=query_plan,
                args=args,
                status=status,
                result=result_state,
                error=error
            )

        state_step.append(state)

    return Executor_State(
        goal=plan.goal,
        step_state=state_step,
        total_steps=len(plan.steps)
    )

          
