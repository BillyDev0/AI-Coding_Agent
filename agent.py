from planner import planner
from executor_tools import executor_tools
from tools import read_file,write_file
from evaluator import evaluator
from logger import logger

tools=[
    read_file,
    write_file
]


def main(prompt):
    history_plan=[]

    iterasi=0
    while iterasi<=5:
        plan=planner(prompt,history_plan,tools)
        logger.info(f"OUTPUT PLANNER: {plan}")
        history_plan.append(plan)

        step_state=executor_tools(plan)
        logger.info(f"STATE STEP: {step_state}")

        feedback_evaluator=evaluator(step_state,tools)
        logger.info(f"OUTPUT EVALUATOR: {feedback_evaluator}")
        
        if feedback_evaluator.status=="done":
           result=feedback_evaluator.final_result
           break
        iterasi+=1

    return result
            

        

prompt=input("Prompt: ")
print(main(prompt))