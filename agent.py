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
    list_feedback=[]
    list_result_tools=[]
    
    while iterasi<=2:
        feedback_evaluator= list_feedback if list_feedback else None
        result_tools= list_result_tools if list_result_tools else None

        plan=planner(prompt,history_plan,tools,feedback_evaluator,result_tools)
        history_plan.append(plan)
        logger.info(f"OUTPUT PLANNER: {plan}")

        list_result_tools.clear()

        step_state=executor_tools(plan)
        list_result_tools.append(step_state)
        if "ERROR" in step_state:
            return step_state
        logger.info(f"STATE STEP: {step_state}")

        result_evaluator=evaluator(step_state,tools,list_feedback)
        list_feedback.append(result_evaluator)
        logger.info(f"OUTPUT EVALUATOR: {result_evaluator}")

        if result_evaluator.status=="done":
            result=result_evaluator.final_result
            return result
        
        iterasi+=1

 
while True:
    prompt=input('masukan prompt (ketik "close" jika sudah): ')
    if prompt == 'close':
        print('PROGRAM SELESAI')
        break
    print(main(prompt))
