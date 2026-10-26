from langchain_core.tools import tool
from pathlib import Path
import os
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

@tool
def read_file(path:str):
    """Read the contents of a specified file from the project so the agent can inspect its code.
    Membaca isi file dari project.

Description:
1. Baca seluruh isi file jika baru pertama kali memeriksa file dan belum memahami struktur atau alur kodenya.
2. Jangan membaca ulang bagian yang sama jika hasil sebelumnya masih tersedia dan relevan.

Tujuan: memberikan konteks kode yang cukup untuk analisis tanpa mengirimkan isi file yang tidak diperlukan.
"""
    PROJECT_ROOT=Path.cwd()
    target_path=Path(path).resolve()

    if not target_path.is_relative_to(PROJECT_ROOT):
        return f"ERROR: path '{path}' berada di luar project root yang diizinkan"

    if not target_path.exists():
        return f"ERROR: file '{path}' tidak ditemukan."

    if not target_path.is_file():
        return f"ERROR: '{path}' bukan file."
    
    try:
        return target_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return f"ERROR: file '{path}' tidak bisa dibaca sebagai teks (kemungkinan binary)."


@tool
def write_file(path: str, content: str, kebutuhan: str=["create new file","execution code"]):
    """Membuat file baru atau memperbarui file yang sudah ada di workspace.

Gunakan tool ini untuk menambahkan, memperbaiki, menghapus, atau mengubah kode.

Aturan perubahan:
- Kirim seluruh isi kode terbaru melalui argumen `content`.
- Pertahankan kode yang tidak berkaitan dengan permintaan user.
- Jangan mengubah bagian lain di luar kebutuhan user.
- Jika memperbaiki kode, output hanya bagian kode yang berubah.
- Jika tidak ada perubahan, jelaskan bahwa file tidak berubah.
- Pastikan output sesuai dengan perubahan yang benar-benar diterapkan.

`kebutuhan`: Jenis kebutuhan penulisan file.
  - `"create new file"`: Membuat file baru dan mengembalikan seluruh isi file.
  - `"execution code"`: Memperbarui kode yang sudah ada dan mengembalikan hasil perubahan sesuai goal user.
"""

    PROJECT_ROOT = Path.cwd()
    target_path=Path(path).resolve()

    if kebutuhan == "execution code":
        if not target_path.is_relative_to(PROJECT_ROOT):
            return f"ERROR: path '{path}' berada di luar project root yang diizinkan"

        if not target_path.exists():
            return f"ERROR: file '{path}' tidak ditemukan."

        if not target_path.is_file():
            return f"ERROR: '{path}' bukan file."
    
    try:
        with open(target_path,"w") as f:
            f.write(content)

        return target_path.read_text(encoding="utf-8")
        
    except Exception as e:
        return f"ERROR: {e}"

@tool
def chatbot(goal:str):
    """
Gunakan tools ini untuk menangani sapaan dan percakapan ringan dengan user.
'goal'= berisi prompt user ke agent, bukan hal lain.
"""

    template = """Kamu adalah tools chatbot untuk AI Coding Agent.

Tugas:
1. Menanggapi sapaan pengguna secara natural dan ramah.
2. Menjawab percakapan ringan yang masih berkaitan dengan AI Coding Agent.
3. Menolak pertanyaan yang tidak berkaitan dengan AI Coding Agent, pemrograman, atau penggunaan tools agent.
4. Jika pertanyaan di luar konteks, jelaskan secara singkat bahwa pertanyaan tersebut di luar ruang lingkup tugasmu dan arahkan pengguna kembali ke AI Coding Agent.
5. Jangan menjawab pertanyaan di luar konteks, meskipun kamu mengetahui jawabannya.
6. Gunakan bahasa yang sederhana, natural, dan langsung ke inti.
7. Jangan mengarang informasi atau mengklaim kemampuan yang tidak dimiliki.

Pesan pengguna:
{input}

Berikan respons sesuai aturan di atas."""

    set_model=GoogleGenerativeAI(
             model="gemini-3.1-flash-lite"
         )
    prompt=ChatPromptTemplate.from_template(template)

    chain=prompt|set_model
    result=chain.invoke({'input':goal})
    return result
    

def get_tools_schema(tools):
    schemas = []

    for tool in tools:
        schemas.append({
            "name": tool.name,
            "description": tool.description,
            "args_schema": tool.args_schema.model_json_schema()
        })
   
    return schemas


def list_files() -> str:
    path=Path.cwd().resolve()
    hasil = []

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", ".venv"}]

        for nama in dirs:
            hasil.append(os.path.join(root, nama) + "/")

        for nama in files:
            hasil.append(os.path.join(root, nama))

    return "\n".join(hasil)
