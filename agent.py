from planner import planner
from executor_tools import executor_tools
from tools import read_file,write_file
from evaluator import evaluator
from logger import logger

tools=[
    read_file,
    write_file
]


def main():
    history_plan=[]
    iterasi=0
    list_feedback=[]
    list_result_tools=[]
    while True:
        prompt=input('masukan prompt (ketik "quit" jika sudah): ')
        if prompt == 'quit':
            print('PROGRAM SELESAI')
            break
        while iterasi<=5:
            feedback_evaluator= list_feedback if list_feedback else None
            result_tools= list_result_tools if list_result_tools else None

            plan=planner(prompt,history_plan,tools,feedback_evaluator,result_tools)
            history_plan.append(plan)
            logger.info(f"OUTPUT PLANNER: {plan}")

            step_state=executor_tools(plan)
            list_result_tools.append(step_state)
            logger.info(f"STATE STEP: {step_state}")

            result_evaluator=evaluator(step_state,tools,list_feedback)
            list_feedback.append(result_evaluator)
            logger.info(f"OUTPUT EVALUATOR: {result_evaluator}")

            if result_evaluator.status=="done":
                result=result_evaluator.final_result
                print(result)
                break
            while len(list_result_tools) >= 4:
                list_result_tools.pop(0)

            iterasi+=1

main()
