import json
from tkinter import messagebox

def carregar_json(caminho):
    try:
        with open(caminho, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_json(caminho, dados):
    with open(caminho, 'w') as f:
        json.dump(dados, f, indent=4)
