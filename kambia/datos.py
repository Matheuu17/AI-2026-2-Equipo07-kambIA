"""Datos: el histórico USD/PEN vive en SQLite y los agentes lo consultan con SQL."""
import sqlite3
from pathlib import Path

import pandas as pd

CSV = Path(__file__).resolve().parent.parent / "data" / "usdpen.csv"
VENTANA_HISTORIAL = 20  # cuántas cotizaciones pasadas ve cada agente


def crear_base(csv=CSV):
    """Carga el CSV en una base SQLite en memoria (tabla tipo_cambio)."""
    con = sqlite3.connect(":memory:", check_same_thread=False)
    pd.read_csv(csv).to_sql("tipo_cambio", con, index=False)
    con.execute("CREATE INDEX idx_fecha ON tipo_cambio(fecha)")
    return con


def leer_todo(con):
    return pd.read_sql("SELECT fecha, tc FROM tipo_cambio ORDER BY fecha", con, parse_dates=["fecha"])


def historial_hasta(con, fecha, n=VENTANA_HISTORIAL):
    """Últimas n cotizaciones hasta `fecha` inclusive (el agente nunca ve el futuro)."""
    filas = con.execute(
        "SELECT tc FROM tipo_cambio WHERE fecha <= ? ORDER BY fecha DESC LIMIT ?", (fecha, n)
    ).fetchall()
    return [f[0] for f in reversed(filas)]
