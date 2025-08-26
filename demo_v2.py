"""Demo que cria um CSV de exemplo, atualiza montantes e gera relatórios prontos para BI."""
from pathlib import Path
import pandas as pd
from datetime import date, timedelta
from storage import save_csv, load_csv, save_json, save_excel
from finance import inserir_transacao, atualizar_montantes, criar_relatorio_para_bi





DATA_FILE = "data/transacoes_v2.csv"


# start a fresh df
try:
    df = load_csv(DATA_FILE)
except Exception:
    df = pd.DataFrame(columns=["id","data","tipo","valor","juros_dia","montante","descricao"])


# se vazio, popula exemplo
if df.empty:
    exemplos = [
        {"id":1, "data": pd.to_datetime(date.today()-timedelta(days=60)), "tipo":"receita", "valor":5000.0, "juros_dia":pd.NA, "montante":pd.NA, "descricao":"Salário"},
        {"id":2, "data": pd.to_datetime(date.today()-timedelta(days=45)), "tipo":"despesa", "valor":1500.0, "juros_dia":pd.NA, "montante":pd.NA, "descricao":"Aluguel"},
        {"id":3, "data": pd.to_datetime(date.today()-timedelta(days=30)), "tipo":"investimento", "valor":1000.0, "juros_dia":0.001, "montante":pd.NA, "descricao":"Tesouro"},
    ]
    df = pd.concat([df, pd.DataFrame(exemplos)], ignore_index=True)


# atualiza montantes até hoje
from finance import atualizar_montantes


df = atualizar_montantes(df)


# salva em formatos
Path("data").mkdir(exist_ok=True)
save_csv(df, DATA_FILE)
save_json(df, "data/transacoes_v2.json")
save_excel(df, "data/transacoes_v2.xlsx")


# gera relatório pronto para BI
from finance import criar_relatorio_para_bi
rel = criar_relatorio_para_bi(df)
rel.to_csv("data/relatorio_mensal.csv", index=False)


print("Demo executada. Arquivos em ./data/")