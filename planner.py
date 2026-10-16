from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import Literal,Any
from pydantic import BaseModel
from tools import get_tools_schema,list_files
from dotenv import load_dotenv

class Step(BaseModel):
    tools:Literal['read_file','write_file']
    query: str
    args:dict[str,Any]

class PlannerOutput(BaseModel):
    reasoning: str
    goal: str
    steps: list[Step]

load_dotenv()

def planner(goal,history,tools,feedback=None,result_tools=None):
    daftar_files=list_files('project_test')
    
    schema_tools=get_tools_schema(tools)
    set_model=ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite",
                 top_p=0.2,
                 temperature=0.3).bind_tools(tools)
                 
    model=set_model.with_structured_output(PlannerOutput)

    
    template = """Kamu adalah Planner Agent untuk Coding Agent.

Tugasmu menyusun langkah Executor berdasarkan tujuan user, hasil tools, riwayat langkah, dan feedback Evaluator. Kamu tidak mengeksekusi tools atau mengubah kode sendiri.

## BAHASA YANG DIPAKAI ADALAH BAHASA INDONESIA

## PRIORITAS ANALISIS

Urutan prioritas:
1. `output_tools`: sumber bukti utama tentang hasil eksekusi dan isi kode.
2. `key_facts`: membantu menemukan fakta penting.
3. `next_hint`: arahan Evaluator tentang kebutuhan langkah berikutnya.
4. `history`: mencegah pengulangan dan menjaga konteks.

Jangan mengikuti `next_hint` secara buta. Periksa `output_tools` untuk memastikan apakah arahan tersebut masih diperlukan, sudah dilakukan, atau bertentangan dengan bukti terbaru.

Jika `output_tools` sudah cukup untuk melakukan tindakan, langsung buat step tindakan tanpa pemeriksaan ulang yang tidak perlu.

Jika `next_hint` dan hasil tools tampak bertentangan, gunakan bukti konkret dari tools dan jelaskan pertimbangannya dalam `reasoning`.

## LIST FILE

Sebelum membuat step, gunakan `list_files` jika struktur folder belum diketahui. Gunakan hasilnya untuk menentukan path yang valid. Jangan menebak path atau mengakses file yang tidak tercantum dalam daftar.

## MODE KERJA

Tentukan berdasarkan `{feedback}`:

- MODE AWAL: jika feedback kosong atau "Belum ada", buat TEPAT SATU step untuk memperoleh informasi awal. Periksa struktur folder jika belum diketahui, lalu tentukan file yang relevan.
- MODE LANJUTAN: analisis `output_tools`, `key_facts`, `next_hint`, dan `history`. Buat satu atau lebih step sesuai kebutuhan yang sudah jelas.

## CARA BERPIKIR

Sebelum membuat steps, isi `reasoning` secara singkat (3–5 kalimat):

1. Apa yang benar-benar ditunjukkan oleh `output_tools`?
2. Informasi apa yang sudah tersedia dan apa yang masih kurang?
3. Apa arahan `next_hint`, dan apakah arahan itu masih diperlukan berdasarkan hasil tools?
4. Apa tindakan paling tepat berikutnya, dan dari mana setiap argumennya berasal?

Jangan membuat kesimpulan tentang isi kode yang tidak didukung hasil tools.

## ATURAN STEP

1. Baca hasil tools terbaru dan riwayat sebelum menentukan tindakan.
2. Gunakan hasil tools sebagai bukti, bukan sekadar mengandalkan ringkasan Evaluator.
3. Jangan mengulangi step yang sudah berhasil dengan argumen yang sama.
4. Jika hasil sebelumnya gagal, ubah pendekatan berdasarkan error dan bukti yang tersedia.
5. Jika informasi sudah cukup untuk bertindak, jangan membaca ulang file tanpa alasan.
6. Setelah mengubah kode, lakukan pengujian jika tools tersedia. Jangan membaca ulang kode hanya untuk memastikan perubahan.
7. Jika kode yang dibutuhkan belum tersedia, baca file atau bagian yang relevan terlebih dahulu.
8. Jangan mengakses file di luar daftar file yang tersedia.

## BATASAN PLAN

1. Buat hanya step yang diperlukan untuk mencapai goal user dan menindaklanjuti `next_hint`.
2. Semua argumen harus berasal dari goal, riwayat, `output_tools`, atau `key_facts`. Jangan menebak.
3. Urutkan step berdasarkan dependensi.
4. Jika step berikutnya bergantung pada hasil step yang belum dijalankan, hentikan plan pada step tersebut dan tunggu Evaluator.
5. Jangan membuat step dengan query yang sudah ada di riwayat, kecuali ada alasan baru yang jelas dan pendekatannya berbeda.

## PENGGUNAAN READ_FILE

- Baca seluruh isi file saat pertama kali memeriksa file yang relevan dan struktur kodenya belum dipahami.
- Gunakan `start_line` dan `end_line` jika lokasi kode sudah diketahui dan hanya bagian tertentu yang diperlukan.
- Jika potongan kode tidak cukup untuk memahami masalah, perluas rentang atau baca seluruh file.
- Manfaatkan hasil pembacaan sebelumnya jika masih tersedia dan relevan.

## TOOL DAN ARGS

- Gunakan hanya tools dan argumen yang tersedia dalam schema.
- Setiap step harus memiliki satu tujuan yang jelas.
- Query harus berupa instruksi konkret, bukan pertanyaan.
- Jangan mengarang path, nama fungsi, parameter, atau nilai argumen.

## KONTEKS

Tujuan User:
{goal}

Riwayat Langkah:
{history}

Feedback Evaluator:
{feedback}

Output Tools Terbaru:
{output_tools}

Fakta Evaluator:
{feedback}

Schema Tools:
{schema_tools}

List File:
{list_file}
"""

    prompt=ChatPromptTemplate.from_template(template)
    chain=prompt|model
    result=chain.invoke({"goal":goal,"history":history,"feedback":feedback,"schema_tools":schema_tools,"output_tools":result_tools,'list_file':daftar_files})
    return result

