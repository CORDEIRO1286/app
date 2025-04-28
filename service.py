import json
from tkinter import messagebox
from data import carregar_json, salvar_json
from models import CTe

def cadastrar_cte(remetente_var, codBarra_var, numero_var, placa_var, motorista_var, data_var):
    remetente = remetente_var.get().upper()
    codigo_barras = codBarra_var.get()
    numero_cte = numero_var.get()
    placa = placa_var.get()
    nome = motorista_var.get()
    data_saida = data_var.get()

    novo_cte = CTe(remetente, codigo_barras, numero_cte, placa, nome, data_saida)
    dados = carregar_json('dados_cte.json')
    dados.append(novo_cte.__dict__)
    salvar_json('dados_cte.json', dados)

    remetente_var.set("")
    codBarra_var.set("")
    numero_var.set("")
    placa_var.set("")
    motorista_var.set("")
    messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")

def consultar_cte(app):
    from relatorio import Relatorio
    rel = Relatorio(app)
    placa = app.placa_var.get()
    numero_cte = app.numero_var.get()
    remetente = app.remente_var.get()
    if numero_cte == "" and placa == "" and remetente != "":
        rel.buscar_cliente(remetente)
    elif numero_cte != "" and placa == "" and remetente == "":
        rel.buscar_cte(numero_cte)
    elif placa != "" and numero_cte == "" and remetente == "":
        rel.buscar_placa(placa)

def atualizar_cte(numero_var, placa_var, motorista_var):
    numero_cte = numero_var.get()
    dados = carregar_json('dados_cte.json')
    for cte in dados:
        if cte['numero_cte'] == numero_cte:
            cte['placa'] = placa_var.get()
            cte['nome'] = motorista_var.get()
            cte['data_entrega'] = cte['data_saida']
            salvar_json('dados_cte.json', dados)
            messagebox.showinfo("Sucesso", "Atualização realizada com sucesso!")
            return
    messagebox.showerror("Erro", "CTe não encontrado para atualização.")

def verificar_existente(numero_cte):
    dados = carregar_json('dados_cte.json')
    return any(cte['numero_cte'] == numero_cte for cte in dados)

def preencher_motorista(placa_var, motorista_var):
    placa = placa_var.get()
    if len(placa) == 7 and placa[3] != "-":
        placa = placa[:3].upper() + "-" + placa[3:].upper()
        try:
            with open('placa.json', 'r') as f:
                data = json.load(f)
            motorista = data.get(placa.upper(), "Motorista não encontrado")
        except:
            motorista = "Motorista não encontrado"
        motorista_var.set(motorista)
        placa_var.set(placa)
