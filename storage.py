from pathlib import Path
import pandas as pd
from typing import Iterable
from datetime import datetime


CSV_COLUMNS = ["id", "data", "tipo", "valor", "juros_dia", "montante", "descricao"]




def _ensure_dir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)




def load_csv(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        return pd.DataFrame(columns=CSV_COLUMNS)
    df = pd.read_csv(p, parse_dates=["data"]) # data -> datetime64
    # normalize columns
    for c in CSV_COLUMNS:
        if c not in df.columns:
            df[c] = pd.NA
        df = df[CSV_COLUMNS]
    return df




def save_csv(df: pd.DataFrame, path: str) -> None:
    _ensure_dir(Path(path))
    df_copy = df.copy()
    # ensure date -> ISO
    if pd.api.types.is_datetime64_any_dtype(df_copy["data"]):
        df_copy["data"] = df_copy["data"].dt.strftime("%Y-%m-%d")
        df_copy.to_csv(path, index=False)




def save_excel(df: pd.DataFrame, path: str) -> None:
    _ensure_dir(Path(path))
    df.to_excel(path, index=False)




def save_json(df: pd.DataFrame, path: str) -> None:
    _ensure_dir(Path(path))
    df.to_json(path, orient="records", date_format="iso", force_ascii=False)




def next_id(df: pd.DataFrame) -> int:
    if df.empty:
        return 1
    return int(df["id"].max()) + 1