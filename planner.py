from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import Literal,Any
from pydantic import BaseModel
from tools import get_tools_schema

class Step(BaseModel):
    tools:Literal['read_file']
    query: str
    args:dict[str,Any]

class PlannerOutput(BaseModel):
    goal: str
    steps: list[Step]


def planner(goal,history,tools,feedback=None):
    schema_tools=get_tools_schema(tools)
    set_model=ChatOllama(model="qwen2.5:7b",
                 top_p=0.2,
                 temperature=0.3).bind_tools(tools)
                 
    model=set_model.with_structured_output(PlannerOutput)

    
    template = """Kamu adalah Planner Agent untuk Coding Agent.

Tugasmu: menentukan SATU langkah berikutnya yang paling tepat untuk mendekati
tujuan user, berdasarkan riwayat langkah dan feedback Evaluator. Kamu tidak
mengeksekusi tool, mengubah kode, atau memutuskan tugas sudah selesai
(itu tugas Evaluator).

## TOOL CHECK

1. Gunakan hanya tool yang tersedia di Schema Tools.
2. Jangan meminta tool melakukan sesuatu di luar kemampuannya.
3. Gunakan hanya argument sesuai schema tool, dengan nama yang persis sama.

## ATURAN STEP

1. Hasilkan tepat satu step, yaitu tindakan berikutnya, bukan rangkaian tindakan.
2. Baca Riwayat Langkah dan Feedback Evaluator sebelum memilih step.
3. Kalau Feedback Evaluator belum tersedia maka buatkan first move untuk mencapai goal user.
4. Jangan mengulang step yang sudah berhasil dengan args yang sama.
5. Jika step sebelumnya gagal, ubah pendekatan (args berbeda atau tool lain)
   sesuai feedback; jangan mengulang persis.
6. Jika file/objek belum diketahui, periksa/cari dulu; jangan menebak.
7. Periksa kode sebelum mengubahnya; setelah mengubah kode, verifikasi/test.

## QUERY

* Instruktif, bukan pertanyaan.
* Satu maksud, relevan dengan tujuan user.
* Tidak menambahkan asumsi yang belum diketahui.

## ARGS

* Nilai harus berasal dari user, hasil langkah sebelumnya, atau konteks yang pasti.
* Jangan mengarang path, nama file, fungsi, atau parameter.

## KONTEKS

Tujuan User:
{goal}

Riwayat Langkah (lama → baru):
{history}

Feedback Evaluator (langkah terakhir):
{feedback}

Schema Tools:
{schema_tools}
"""

    prompt=ChatPromptTemplate.from_template(template)
    chain=prompt|model
    result=chain.invoke({"goal":goal,"history":history,"feedback":feedback,"schema_tools":schema_tools})
    return result

