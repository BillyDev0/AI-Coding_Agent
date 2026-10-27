from planner import planner
from executor_tools import executor_tools
from tools import read_file,write_file,chatbot
from evaluator import evaluator
from logger import logger
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

tools=[
    read_file,
    write_file,
    chatbot
]

def straming_model(output,source):
    template = """Kamu adalah asisten yang menjawab pengguna secara natural, sederhana, dan langsung ke inti.

Aturan:
1. Jika menerima output program, jelaskan artinya dengan bahasa yang mudah dipahami tanpa mengarang informasi.
2. Hindari kalimat kaku seperti "Berdasarkan output tersebut", "Dari program tersebut dapat disimpulkan", "Output program menunjukkan bahwa".
3. Jangan menebak fakta yang tidak tersedia.
4. Jika output berasal dari tools chatbot, teruskan output tersebut kepada pengguna tanpa mengubah, menjelaskan ulang, atau menambahkan respons apa pun.
5. Jika sumber output tidak diketahui, perlakukan sebagai output program biasa.

Sumber output:
{source}

Output:
{output}

Jawab sesuai aturan di atas."""

    set_model=ChatOllama(
             model="qwen2.5:7b",
             temperature=0.1,
             top_p=0.1,
         )
    prompt=ChatPromptTemplate.from_template(template)

    chain=prompt|set_model
    for chunk in chain.stream({'output':output,'source':source}):
        print(chunk.content, end="", flush=True)

    print()


def run_agent(prompt,list_result_tools):
    history_plan=[]
    list_feedback=[]
    iterasi=0
   

    while iterasi<=5:
        feedback_evaluator= list_feedback if list_feedback else None
        result_tools= list_result_tools if list_result_tools else None

        plan=planner(prompt,history_plan,tools,feedback_evaluator,result_tools)
        history_plan.append(plan)
        logger.info(f"OUTPUT PLANNER: {plan}")

        step_state=executor_tools(plan)
        list_result_tools.append(step_state)
        logger.info(f"STATE STEP: {step_state}")
        for i in step_state.step_state:
             if i.tools=='chatbot':
                  return i.result,"chatbot"

        result_evaluator=evaluator(step_state,list_feedback)
        list_feedback.append(result_evaluator)
        logger.info(f"OUTPUT EVALUATOR: {result_evaluator}")

        if result_evaluator.status=="done":
            result=result_evaluator.final_result
            return result,"program"
        
        while len(list_result_tools) >= 4:
            list_result_tools.pop(0)

        iterasi+=1

    else:
        return "Gagal menyelesaikan instruksi setelah N iterasi","program"

    
    
def main():
    while True:
            list_result_tools=[]
            try:
                prompt=input('masukan prompt (ketik "quit" jika sudah): ')
                if prompt == 'quit':
                    print('PROGRAM SELESAI')
                    break
                if prompt == '':
                    continue

                result_agent,source=run_agent(prompt,list_result_tools)
                straming_model(result_agent,source)

            except KeyboardInterrupt:
                print("Program dihentikan oleh pengguna melalui keyboard.")

            except EOFError:
                print("Input tidak tersedia.")
    

if __name__=="__main__":
        main()

