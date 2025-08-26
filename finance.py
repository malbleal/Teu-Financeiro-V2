from datetime import datetime, date
from math import pow
import pandas as pd
from typing import Optional, Tuple


# espera-se que df contenha colunas: id, data (datetime), tipo, valor (float), juros_dia (float|NA), montante (float|NA), descricao




def normalize_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # despesa fica negativa
    df["valor"] = df.apply(lambda r: -abs(r["valor"]) if r["tipo"] == "despesa" else abs(r["valor"]), axis=1)
    return df




def dias_entre(d1: pd.Timestamp, d2: pd.Timestamp) -> int:
    return max(int((d2.normalize() - d1.normalize()).days), 0)




def calcular_montante(capital: float, juros_dia: float, dias: int) -> float:
    # juros_dia em decimal (ex.: 0.001)
    if juros_dia is None or pd.isna(juros_dia):
        return capital
    return float(capital * pow(1 + float(juros_dia), dias))




def atualizar_montantes(df: pd.DataFrame, referencia: Optional[date] = None) -> pd.DataFrame:
    """Atualiza a coluna 'montante' para linhas de tipo 'investimento' calculadas até a data 'referencia'.
    Se referencia for None, usa hoje().
    """
    df = df.copy()
    if referencia is None:
        referencia = pd.Timestamp(datetime.utcnow().date())
    else:
        referencia = pd.Timestamp(referencia)

    def _calc(row):
        if row["tipo"] != "investimento":
            return row.get("montante", pd.NA)
        dias = dias_entre(pd.Timestamp(row["data"]), referencia)
        return calcular_montante(row["valor"], row.get("juros_dia", None), dias)

    df["montante"] = df.apply(_calc, axis=1)
    return df




def agregar_por_mes(df: pd.DataFrame) -> pd.DataFrame:
    df2 = normalize_values(df)
    df2 = df2.copy()
    df2["ano_mes"] = df2["data"].dt.to_period("M").astype(str)
    res = df2.groupby(["ano_mes", "tipo"]) ["valor"].sum().reset_index()
    return res




def saldo_acumulado(df: pd.DataFrame) -> pd.DataFrame:
    df2 = normalize_values(df).sort_values(by="data")
    df2["saldo_acumulado"] = df2["valor"].cumsum()
    return df2[["data", "tipo", "valor", "saldo_acumulado"]]




def criar_relatorio_para_bi(df: pd.DataFrame) -> pd.DataFrame:
    # """Prepara um dataframe wide por mês com colunas: ano_mes, total_receita, total_despesa, total_investimento, saldo"""
    agg = agregar_por_mes(df)
    pivot = agg.pivot(index="ano_mes", columns="tipo", values="valor").fillna(0)
    pivot["saldo"] = pivot.get("receita", 0) + pivot.get("investimento", 0) + pivot.get("despesa", 0)
    pivot = pivot.reset_index()
    return pivot




def inserir_transacao(df: pd.DataFrame, data: date | str, tipo: str, valor: float, juros_dia: Optional[float] = None, descricao: Optional[str] = None) -> pd.DataFrame:
    df = df.copy()
    new_id = int(df["id"].max()) + 1 if not df.empty else 1
    data_ts = pd.to_datetime(data).normalize()
    df = pd.concat([df, pd.DataFrame([{"id": new_id, "data": data_ts, "tipo": tipo, "valor": float(valor), "juros_dia": juros_dia, "montante": pd.NA, "descricao": descricao}])], ignore_index=True)
    return df




def atualizar_transacao(df: pd.DataFrame, id_: int, **fields) -> pd.DataFrame:
    df = df.copy()
    mask = df["id"] == id_
    if not mask.any():
        raise KeyError(f"ID {id_} não encontrado")
    for k, v in fields.items():
        if k == "data":
            df.loc[mask, "data"] = pd.to_datetime(v).normalize()
        else:
            df.loc[mask, k] = v
    return df




def deletar_transacao(df: pd.DataFrame, id_: int) -> pd.DataFrame:
    if id_ not in df["id"].values:
        raise KeyError(f"ID {id_} não encontrado")
    return df[df["id"] != id_].reset_index(drop=True)