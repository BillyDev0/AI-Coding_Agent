from tools import read_file,write_file
from typing import Literal,Any
from pydantic import BaseModel

mapping_tools={
    "read_file":read_file,
    "write_file":write_file
}


class StepState(BaseModel):
    step: int
    tools: str
    query: str
    args: dict[str, Any]
    status: Literal["success"]
    result: Any = None
    error: str | None = None

class full_step(BaseModel):
    goal:str
    total_step:int
    step_state:list[StepState]

def executor_tools(plan):
    list_state=[]
    for i,item in enumerate(plan.steps,1):
        tools=item.tools
        query_plan=item.query
        args=item.args

        run_tools=mapping_tools[tools]

        result_tools=run_tools.invoke(args)

        if "ERROR" in result_tools:
            error=result_tools
            return error

        else:
            result_state=result_tools
            status='success'
            error=None
        
        list_state.append(
            StepState(
                step=i,
                tools=tools,
                query=query_plan,
                args=args,
                status=status,
                result=result_state,
                error=error
            )
            )

    return full_step(
        goal=plan.goal,
        total_step=len(plan.steps),
        step_state=list_state
    )


    
          
