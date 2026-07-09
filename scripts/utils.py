# scripts/utils.py
import os

def ensure_folder(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def get_output_path(folder: str, filename: str):
    ensure_folder(folder)
    return os.path.join(folder, filename)
