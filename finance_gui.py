import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd
from pathlib import Path
from finance import inserir_transacao, atualizar_transacao, deletar_transacao, atualizar_montantes
from storage import load_csv, save_csv

DATA_FILE = "data/transacoes_v2.csv"
Path("data").mkdir(exist_ok=True)

def carregar_dados():
    df = load_csv(DATA_FILE)
    return df

def salvar_dados(df):
    save_csv(df, DATA_FILE)
    atualizar_tabela(df)

def atualizar_tabela(df):
    for row in tree.get_children():
        tree.delete(row)
    for _, row in df.sort_values(by="data").iterrows():
        tree.insert("", "end", iid=row["id"], values=list(row))

def adicionar_transacao():
    df = carregar_dados()
    try:
        data = simpledialog.askstring("Data", "Data (YYYY-MM-DD):")
        if data is None:  # Usuário cancelou
            return
            
        tipo = simpledialog.askstring("Tipo", "Tipo (receita/despesa/investimento):")
        if tipo is None:  # Usuário cancelou
            return
            
        valor_str = simpledialog.askstring("Valor", "Valor:")
        if valor_str is None:  # Usuário cancelou
            return
        valor = float(valor_str)
        
        juros_dia_str = simpledialog.askstring("Juros/dia", "Juros/dia (opcional):")
        juros_dia = float(juros_dia_str) if juros_dia_str else None
        
        descricao = simpledialog.askstring("Descrição", "Descrição (opcional):")
        
        df = inserir_transacao(df, data, tipo, valor, juros_dia, descricao)
        salvar_dados(df)
        messagebox.showinfo("Sucesso", "Transação adicionada!")
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido! Digite um número.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def deletar_transacao_gui():
    df = carregar_dados()
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Aviso", "Selecione uma transação para deletar.")
        return
    
    if messagebox.askyesno("Confirmar", "Tem certeza que deseja deletar esta transação?"):
        df = deletar_transacao(df, int(selected[0]))
        salvar_dados(df)
        messagebox.showinfo("Sucesso", "Transação deletada!")

def atualizar_rendimentos_gui():
    df = carregar_dados()
    df = atualizar_montantes(df)
    salvar_dados(df)
    messagebox.showinfo("Sucesso", "Montantes atualizados!")

# --- Janela principal ---
root = tk.Tk()
root.title("Controle Financeiro V2")

# Botões
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Adicionar", command=adicionar_transacao).pack(side=tk.LEFT, padx=5)
tk.Button(frame_buttons, text="Deletar", command=deletar_transacao_gui).pack(side=tk.LEFT, padx=5)
tk.Button(frame_buttons, text="Atualizar Rendimentos", command=atualizar_rendimentos_gui).pack(side=tk.LEFT, padx=5)

# Tabela
tree = ttk.Treeview(root, columns=["id","data","tipo","valor","juros_dia","montante","descricao"], show="headings")
for col in ["id","data","tipo","valor","juros_dia","montante","descricao"]:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(fill=tk.BOTH, expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Carrega dados iniciais
df = carregar_dados()
atualizar_tabela(df)

root.mainloop()