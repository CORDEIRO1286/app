import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from service import cadastrar_cte, consultar_cte, atualizar_cte, preencher_motorista
from utils import hoje_formatado
import time

class TransportFormApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de CTe")

        self.container = tk.Frame(root)
        self.container.pack(padx=50, pady=50)

        self.title = tk.Label(self.container, text="Dados de Transporte", font=("Arial", 16))
        self.title.grid(row=0, column=0, columnspan=2, pady=10)

        # Variáveis
        self.remente_var = tk.StringVar()
        self.codBarra_var = tk.StringVar()
        self.numero_var = tk.StringVar()
        self.placa_var = tk.StringVar()
        self.motorista_var = tk.StringVar()
        self.data_var = tk.StringVar(value=hoje_formatado())
        self.obs_var = tk.StringVar()
        self.horaAtual_var = tk.StringVar()

        # Campos de entrada
        self.remetente_entry = self.create_label_entry("Remetente:", 1, self.remente_var)
        self.codBarra_entry = self.create_label_entry("Código de Barras:", 2, self.codBarra_var)
        self.numero_entry = self.create_label_entry("Número de CTe:", 3, self.numero_var)
        self.placa_entry = self.create_label_entry("Placa:", 4, self.placa_var)
        self.motorista_entry = self.create_label_entry("Motorista:", 5, self.motorista_var, state='readonly')
        self.data_entry = self.create_label_entry("Data:", 6, self.data_var, state='readonly')
        self.obs_entry = self.create_label_entry("Obs:", 7, self.obs_var, state='readonly')

        # Botões
        self.button_atualizar = tk.Button(self.container, text="Atualizar", command=self.atualizar)
        self.button_atualizar.grid(row=9, column=0, padx=10, pady=10)

        self.button_consultar = tk.Button(self.container, text="Consultar", command=self.consultar)
        self.button_consultar.grid(row=9, column=1, padx=10, pady=10)

        self.button_cadastrar = tk.Button(self.container, text="Cadastrar", command=self.cadastrar)
        self.button_cadastrar.grid(row=9, column=2, padx=10, pady=10)
        self.hora_entry = self.create_label_entry("Hora Atual:", 11, self.horaAtual_var, state='readonly')

        # Lógica reativa
        self.codBarra_var.trace_add('write', self.extrair_cte)
        self.numero_var.trace_add('write', self.verificar_existente)
        self.placa_var.trace_add('write', lambda *args: preencher_motorista(self.placa_var, self.motorista_var))

        # Inicializa atualização da hora
        self.atualizar_hora()

    def create_label_entry(self, label_text, row, var, state='normal'):
        label = tk.Label(self.container, text=label_text)
        label.grid(row=row, column=0, padx=5, pady=5)
        entry = tk.Entry(self.container, textvariable=var, state=state)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry

    def atualizar_hora(self):
        agora = time.strftime("%H:%M:%S")
        self.horaAtual_var.set(agora)

        self.root.after(1000, self.atualizar_hora)

    def extrair_cte(self, *args):
        cte = str(self.codBarra_var.get()[24:34]).lstrip("0")
        self.numero_var.set(cte)

    def verificar_existente(self, *args):
        from service import verificar_existente
        if verificar_existente(self.numero_var.get()):
            self.obs_var.set("Usar o Botão consulta")

    def cadastrar(self):
        cadastrar_cte(self.remente_var, self.codBarra_var, self.numero_var,
                      self.placa_var, self.motorista_var, self.data_var)

    def consultar(self):
        consultar_cte(self)
        self.obs_var.set("")

    def atualizar(self):
        atualizar_cte(self.numero_var, self.placa_var, self.motorista_var)
