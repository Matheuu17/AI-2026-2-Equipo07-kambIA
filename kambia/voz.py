"""Jarvis: asistente por voz de KambIA (extra).

Reutiliza la idea del primer prototipo del equipo (extras/jarvis_voz.py): un agente reflejo que
reacciona a palabras clave. La diferencia es que ahora responde con lo que deciden los agentes
de KambIA sobre los datos reales. Funciona en el navegador: el audio llega desde st.audio_input.
"""
import io
import re
import statistics

from .agentes import COMPRAR, AgenteUtilidad
from .datos import historial_hasta
from .simulador import solo_tecnicas


def transcribir(wav_bytes):
    """Voz → texto con el reconocedor de Google (necesita internet)."""
    import speech_recognition as sr

    rec = sr.Recognizer()
    with sr.AudioFile(io.BytesIO(wav_bytes)) as fuente:
        audio = rec.record(fuente)
    try:
        return rec.recognize_google(audio, language="es-PE")
    except sr.UnknownValueError:
        return ""


def sintetizar(texto):
    """Texto → audio MP3 (Google TTS)."""
    from gtts import gTTS

    buf = io.BytesIO()
    gTTS(texto, lang="es", tld="com.mx").write_to_fp(buf)
    return buf.getvalue()


MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]


def _fecha_es(f):
    return f"{f.day} de {MESES[f.month - 1]}"


def _numero_antes_de(texto, palabras):
    m = re.search(r"(\d[\d.,]*)\s*(?:" + palabras + ")", texto)
    return int(re.sub(r"[.,]", "", m.group(1))) if m else None


def responder(texto, con, df, monto, plazo, aversion_riesgo, tabla=None):
    """Reglas condición-acción por palabra clave → respuesta en texto."""
    t = texto.lower()
    hoy = df["fecha"].iloc[-1].strftime("%Y-%m-%d")
    hist = historial_hasta(con, hoy)
    tc = hist[-1]

    if any(p in t for p in ("salir", "adiós", "adios", "gracias")):
        return "A sus órdenes. Aquí estaré cuando tenga que pagar otra factura."

    if any(p in t for p in ("compro", "comprar", "espero", "esperar", "conviene", "decisión", "decido")):
        dias = _numero_antes_de(t, "día|dia") or plazo
        monto_voz = _numero_antes_de(t, "dólar|dolar|\\$|usd") or monto
        p = {"tc_hoy": tc, "historial": hist, "dias_restantes": max(dias - 1, 0), "monto": monto_voz}
        accion, motivo = AgenteUtilidad(aversion_riesgo).actuar(p)
        costo = monto_voz * tc
        if accion == COMPRAR:
            return (f"Le recomiendo comprar hoy. El dólar está en {tc:.3f} soles y los {monto_voz:,} dólares "
                    f"le costarían {costo:,.0f} soles. Esperar {dias} días no compensa el riesgo.")
        ahorro = monto_voz * (tc - statistics.mean(hist))
        return (f"Le recomiendo esperar. El dólar está en {tc:.3f}, por encima de su promedio de veinte días, "
                f"si vuelve a ese promedio ahorraría unos {ahorro:,.0f} soles. Tiene {dias} días; si llega al último, compre igual.")

    if any(p in t for p in ("mejor", "gana", "ganador", "estrategia", "agente")) and tabla is not None:
        agentes = solo_tecnicas(tabla)  # igual que el 🏆 de la app: sin modos base ni Óptimo
        top = agentes.loc[agentes["Ahorro promedio vs base (S/)"].idxmax()]
        seguro = agentes.loc[agentes["Pierde vs base (%)"].idxmin()]
        return (f"En la simulación, {top['Estrategia']} ahorra más en promedio: {top['Ahorro promedio vs base (S/)']:,.0f} "
                f"soles por factura. El más seguro es {seguro['Estrategia']}: solo pierde contra la base en el "
                f"{seguro['Pierde vs base (%)']:.0f} por ciento de los casos.")

    if any(p in t for p in ("dólar", "dolar", "precio", "cambio", "cotiza", "cuánto", "cuanto")):
        prom7 = statistics.mean(hist[-7:])
        tendencia = "subiendo" if tc > prom7 else "bajando"
        return (f"El dólar está en {tc:.3f} soles, al {_fecha_es(df['fecha'].iloc[-1])}. Su promedio de siete días es "
                f"{prom7:.3f}, así que viene {tendencia}.")

    if any(p in t for p in ("hola", "jarvis", "ayuda", "buenas")):
        return ("Hola, soy Jarvis de KambIA. Pregúnteme: a cuánto está el dólar, si compro o espero, "
                "por ejemplo 'tengo cinco días, compro o espero', o cuál es la mejor estrategia.")

    return "No le entendí. Puede preguntarme a cuánto está el dólar, si compro o espero, o cuál estrategia gana."
