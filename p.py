import os
from pathlib  import Path
def list_files() -> str:
    path = Path.cwd()
    hasil = []

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", ".venv"}]

        for nama in dirs:
            hasil.append(os.path.join(root, nama) + "/")

        for nama in files:
            hasil.append(os.path.join(root, nama))

    return "\n".join(hasil)

print(list_files())

