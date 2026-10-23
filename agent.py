from planner import planner
from executor_tools import executor_tools
from tools import read_file,write_file
from evaluator import evaluator
from logger import logger
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

tools=[
    read_file,
    write_file
]


def run_agent():
    history_plan=[]
    list_feedback=[]
    list_result_tools=[]
    iterasi=0
    while True:
        try:
            prompt=input('masukan prompt (ketik "quit" jika sudah): ')
            if prompt == 'quit':
                print('PROGRAM SELESAI')
                break
            if prompt == '':
                continue

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
                    iterasi=0
                    break
                while len(list_result_tools) >= 4:
                    list_result_tools.pop(0)

                iterasi+=1

            else:
                print("Gagal menyelesaikan instruksi setelah N iterasi")
        except KeyboardInterrupt:
                    print("Program dihentikan oleh pengguna melalui keyboard.")

def straming_model(output):
    template="""Jelaskan output program berikut kepada pengguna.
Gunakan hanya informasi yang tersedia.
Jangan menebak penyebab, status, atau detail yang tidak disebutkan.
Jika informasinya tidak cukup, katakan bahwa informasi tersebut tidak tersedia.

Output program:
{output}"""

    set_model=OllamaLLM(
             model="qwen2.5:7b",
             temperature=0.1,
             top_p=0.1,
         )
    prompt=ChatPromptTemplate.from_template(template)

    chain=prompt|set_model
    for chunk in chain.stream({'output':output}):
         print(chunk, end='', flush=True)
    
    
def handle_streaming(chunk):
    for chunks in chunk:
         print(chunks)
     
def main():
    result_agent=run_agent()
    streaming=straming_model(result_agent)
    handle_streaming(streaming)
    



if __name__=="__main__":
        main()
