from langchain_core.tools import tool
from pathlib import Path
import os
from typing import Literal

@tool
def read_file(path:str):
    """Read the contents of a specified file from the project so the agent can inspect its code.
    Membaca isi file dari project.

Description:
1. Baca seluruh isi file jika baru pertama kali memeriksa file dan belum memahami struktur atau alur kodenya.
2. Jangan membaca ulang bagian yang sama jika hasil sebelumnya masih tersedia dan relevan.

Tujuan: memberikan konteks kode yang cukup untuk analisis tanpa mengirimkan isi file yang tidak diperlukan.
"""
    PROJECT_ROOT = Path("project_test").resolve()
    target_path=(PROJECT_ROOT/path).resolve()

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

    PROJECT_ROOT = Path("project_test").resolve()
    target_path=(PROJECT_ROOT/path).resolve()

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

    
def get_tools_schema(tools):
    schemas = []

    for tool in tools:
        schemas.append({
            "name": tool.name,
            "description": tool.description,
            "args_schema": tool.args_schema.model_json_schema()
        })
   
    return schemas


def list_files(path: str = ".") -> str:
    hasil = []

    for nama in os.listdir(path):
        hasil.append(nama)

    return "\n".join(hasil)