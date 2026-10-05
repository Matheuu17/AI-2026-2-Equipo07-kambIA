"""Entorno: una factura de US$ `monto` que vence en `plazo` días hábiles.
El agente decide cada día; si llega al último día sin comprar, el entorno lo obliga a comprar."""
import time

import pandas as pd

from .agentes import COMPRAR
from .datos import VENTANA_HISTORIAL, historial_hasta

NOMBRE_OPTIMO = "Óptimo (referencia, ve el futuro)"


def percepciones(con, fechas, monto):
    """Arma con SQL lo que el agente percibe cada día de la ventana."""
    plazo = len(fechas)
    salida = []
    for i, f in enumerate(fechas):
        hist = historial_hasta(con, f)
        salida.append({"fecha": f, "tc_hoy": hist[-1], "historial": hist,
                       "dias_restantes": plazo - 1 - i, "monto": monto})
    return salida


def correr_agente(agente, perc):
    """Ciclo percibir → decidir → actuar. Devuelve el día de compra y la traza."""
    agente.reiniciar()
    traza = []
    for dia, p in enumerate(perc):
        accion, motivo = agente.actuar(p)
        if accion != COMPRAR and p["dias_restantes"] == 0:
            accion, motivo = COMPRAR, "Vence el plazo: el entorno obliga a comprar."
        traza.append({"dia": dia + 1, "fecha": p["fecha"], "tc": p["tc_hoy"], "accion": accion, "motivo": motivo})
        if accion == COMPRAR:
            return dia, traza
    raise RuntimeError("el agente no compró")


def simular_lote(con, df, agentes, monto, plazo, desde=None, hasta=None):
    """Corre todos los agentes sobre cada factura posible (una por día de inicio) del periodo."""
    fechas = df["fecha"].dt.strftime("%Y-%m-%d").tolist()
    inicio_min = VENTANA_HISTORIAL - 1
    filas = []
    tiempos = {a.nombre: 0.0 for a in agentes}
    for i in range(inicio_min, len(fechas) - plazo + 1):
        if (desde and fechas[i] < desde) or (hasta and fechas[i] > hasta):
            continue
        ventana = fechas[i:i + plazo]
        perc = percepciones(con, ventana, monto)
        fila = {"inicio": fechas[i]}
        for a in agentes:
            t0 = time.perf_counter()
            dia, _ = correr_agente(a, perc)
            tiempos[a.nombre] += time.perf_counter() - t0
            fila[a.nombre] = monto * perc[dia]["tc_hoy"]
            fila[a.nombre + "|dia"] = dia + 1
        mejor = min(range(plazo), key=lambda d: perc[d]["tc_hoy"])
        fila[NOMBRE_OPTIMO] = monto * perc[mejor]["tc_hoy"]
        fila[NOMBRE_OPTIMO + "|dia"] = mejor + 1
        filas.append(fila)
    return pd.DataFrame(filas), tiempos


def tabla_comparativa(corridas, tiempos, agentes):
    """Misma métrica para todos: costo en soles y ahorro frente al modo base."""
    base = agentes[0].nombre
    nombres = [a.nombre for a in agentes] + [NOMBRE_OPTIMO]
    n = len(corridas)
    filas = []
    for nom in nombres:
        ahorro = corridas[base] - corridas[nom]
        filas.append({
            "Estrategia": nom,
            "Costo promedio (S/)": corridas[nom].mean(),
            "Ahorro promedio vs base (S/)": ahorro.mean(),
            "Ahorro total (S/)": ahorro.sum(),
            "Gana a la base (%)": (ahorro > 0.005).mean() * 100,
            "Pierde vs base (%)": (ahorro < -0.005).mean() * 100,
            "Peor caso vs base (S/)": ahorro.min(),
            "Día promedio de compra": corridas[nom + "|dia"].mean(),
            "Tiempo total (ms)": tiempos.get(nom, 0.0) * 1000,
            "Corridas": n,
        })
    return pd.DataFrame(filas)
