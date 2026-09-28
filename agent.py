from planner import planner
from executor_tools import executor_tools
from tools import read_file
from logger import logger

tools=[
    read_file
]

def main(prompt):
    plan=planner(prompt,tools)
    logger.info(f'RESULT PLANNER: {plan}')

    result_executor=executor_tools(plan)
    logger.info(f"RESULT EXECUTOR: {result_executor}")

    return result_executor

prompt=input("Prompt: ")
print(main(prompt))