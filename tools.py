from langchain_core.tools import tool
from pathlib import Path
@tool
def read_file(path:str):
    """Read the contents of a specified file from the project so the agent can inspect its code.

Description:
- Tool ini HANYA membaca dan mengembalikan seluruh isi file.
- Tool ini TIDAK melakukan pencarian, filtering, atau analisis isi file.
- Jika ingin mencari bagian tertentu dari file, gunakan tool lain yang memang mendukung pencarian.
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
        result=target_path.read_text()
        return result
    
    except UnicodeDecodeError:
        return f"ERROR: file '{path}' tidak bisa dibaca sebagai teks (kemungkinan binary)."


def get_tools_schema(tools):
    schemas = []

    for tool in tools:
        schemas.append({
            "name": tool.name,
            "description": tool.description,
            "args_schema": tool.args_schema.model_json_schema()
        })
   
    return schemas

@tool
def write_file(path: str, content: str):
    """
    Membuat file baru atau memperbarui isi file yang sudah ada di workspace.
    
    Gunakan tool ini ketika kode perlu ditambahkan, diperbaiki, atau diubah.
    Pastikan path file sesuai dengan file yang ingin dimodifikasi.
    """