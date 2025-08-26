from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional


TIPOS = {"receita", "despesa", "investimento"}


@dataclass
class TransacaoRaw:
    # formato bruto usado ao criar entradas (strings permitidas para data)
    data: str
    tipo: str
    valor: float
    juros_dia: Optional[float] = None # ex.: 0.001 = 0.1% ao dia
    descricao: Optional[str] = None


def validar(self) -> None:
    if self.tipo not in TIPOS:
        raise ValueError(f"Tipo inválido: {self.tipo}. Deve ser um de {TIPOS}")
    if not isinstance(self.valor, (int, float)):
        raise ValueError("Valor deve ser número")