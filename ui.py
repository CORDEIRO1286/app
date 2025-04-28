import tkinter as tk
from components import TransportFormApp

def iniciar_app():
    root = tk.Tk()
    app = TransportFormApp(root)
    root.mainloop()
