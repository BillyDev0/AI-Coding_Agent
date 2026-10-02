from tools import read_file,write_file
from typing import Literal,Any
from pydantic import BaseModel

mapping_tools={
    "read_file":read_file,
    "write_file":write_file
}


class StepState(BaseModel):
    goal:str
    tools: str
    query: str
    args: dict[str, Any]
    status: Literal["success", "failed"]
    result: Any = None
    error: str | None = None


def executor_tools(plan):
    for item in plan.steps:
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

        return StepState(
                goal=plan.goal,
                tools=tools,
                query=query_plan,
                args=args,
                status=status,
                result=result_state,
                error=error
            )


    
          
