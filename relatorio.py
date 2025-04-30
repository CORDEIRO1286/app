import tkinter as tk
from tkinter import messagebox
from data import carregar_json

class Relatorio:
    def __init__(self, transport_form_app):
        self.transport_form_app = transport_form_app

    def exibir_resultado(self, resultado=[]):
        if not hasattr(self, 'janela'):
            self.janela = tk.Toplevel()
            self.janela.title("Relatório")
            self.janela.geometry("1800x800")
            self.resultado_texto = tk.Text(self.janela, height=15, width=132, state=tk.DISABLED)
            self.resultado_texto.pack(pady=10)

        self.resultado_texto.config(state=tk.NORMAL)
        self.resultado_texto.delete("1.0", tk.END)

        for item in resultado:
            texto_formatado = (
                f"Remetente: {item['remetente']} | "
                f"CTe: {item['numero_cte']} | "
                f"Placa: {item['placa']} | "
                f"Motorista: {item['nome']} | "
                f"Data de Entrega: {item['data_entrega']}\n"
            )
            self.resultado_texto.insert(tk.END, texto_formatado)

        self.resultado_texto.config(state=tk.DISABLED)

    def buscar_cliente(self, remetente):
        dados = carregar_json('dados_cte.json')
        cliente = [item for item in dados if item.get('remetente') == remetente]
        if not cliente:
            messagebox.showerror("Erro", "Cliente não encontrado!")
        else:
            self.exibir_resultado(cliente)

    def buscar_cte(self, numero):
        dados = carregar_json('dados_cte.json')
        for item in dados:
            if item.get('numero_cte') == numero:
                app = self.transport_form_app
                app.remente_var.set(item.get('remetente', ''))
                app.codBarra_var.set(item.get('codigo_barras', ''))
                app.placa_var.set(item.get('placa', ''))
                app.motorista_var.set(item.get('nome', ''))
                app.data_var.set(item.get('data_entrega', ''))
                app.data_entry.config(state='normal')
                app.data_entry.config(state='readonly')
                messagebox.showinfo("Sucesso", "CTe Encontrado")
                app.remente_var.set('')
                app.codBarra_var.set('')
                app.placa_var.set('')
                app.motorista_var.set('')
                app.data_var.set('')
                return
        messagebox.showerror("Erro", "CTe não encontrado!")

    def buscar_placa(self, placa):
        dados = carregar_json('dados_cte.json')
        resultado = [item for item in dados if item.get('placa') == placa]
        if not resultado:
            messagebox.showerror("Erro", "Placa não encontrada!")
        else:
            self.exibir_resultado(resultado)
