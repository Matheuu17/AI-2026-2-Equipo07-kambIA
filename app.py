"""KambIA — ¿cuándo conviene comprar los dólares para pagar al proveedor?"""
import altair as alt
import pandas as pd
import streamlit as st

from kambia.agentes import crear_agentes
from kambia.datos import crear_base, leer_todo
from kambia.voz import responder, sintetizar, transcribir
from kambia.simulador import correr_agente, percepciones, simular_lote, solo_tecnicas, tabla_comparativa

st.set_page_config(page_title="KambIA", page_icon="💱", layout="wide")

# Etiquetas de presentación: se conservan los nombres y columnas internos.
ETIQUETAS_ESTRATEGIAS = {
    "Aleatorio (modo base 2)": "Aleatorio (referencia adicional)",
}
ETIQUETAS_COLUMNAS = {
    "Gana a la base (%)": "Facturas en que gana a la base (%)",
    "Pierde vs base (%)": "Facturas en que pierde frente a la base (%)",
    "Peor caso vs base (S/)": "Mayor pérdida frente a la base (S/)",
}


def para_mostrar(tabla):
    """Copia con etiquetas legibles, sin alterar los datos usados en los cálculos."""
    vista = tabla.rename(columns=ETIQUETAS_COLUMNAS).copy()
    vista["Estrategia"] = vista["Estrategia"].replace(ETIQUETAS_ESTRATEGIAS)
    return vista


@st.cache_resource
def conexion():
    return crear_base()


con = conexion()
df = leer_todo(con)

st.title("💱 KambIA")
st.markdown(
    "Un importador peruano recibe una factura en dólares y tiene unos días para pagarla. "
    "**¿Qué día le conviene comprar los dólares?** Comparamos cuatro técnicas del bloque 1 "
    "con **Base (compra el día 1)**, el modo base principal, sobre el histórico real USD/PEN. "
    "**Aleatorio** es una referencia adicional para comparar con la suerte; no es una técnica inteligente."
)

# ---------- parámetros ----------
with st.sidebar:
    st.header("Parámetros")
    monto = st.number_input("Monto de la factura (US$)", 1000, 1_000_000, 10_000, step=1000)
    plazo = st.slider("Plazo para pagar (días hábiles)", 2, 20, 10)
    fmin, fmax = df["fecha"].min().date(), df["fecha"].max().date()
    periodo = st.date_input("Periodo de facturas a evaluar", (fmin, fmax), min_value=fmin, max_value=fmax)
    st.subheader("Agentes")
    dias_promedio = st.slider("Reflejo: días del promedio", 3, 20, 7)
    alfa = st.slider("Modelo: suavizado de la tendencia (α)", 0.1, 1.0, 0.5, 0.1)
    margen = st.slider("Objetivos: margen bajo el promedio (%)", 0.0, 2.0, 0.3, 0.1) / 100
    aversion = st.slider("Utilidad: aversión al riesgo (λ)", 0.0, 3.0, 0.5, 0.1)
    semilla = st.number_input("Aleatorio: semilla", 0, 9999, 7)

agentes = crear_agentes(dias_promedio, alfa, margen, aversion, semilla)
desde, hasta = (periodo[0].isoformat(), periodo[1].isoformat()) if len(periodo) == 2 else (None, None)

tab_cmp, tab_caso, tab_agentes, tab_datos, tab_voz = st.tabs(
    ["📊 Comparación", "🔍 Una factura paso a paso", "🤖 Cómo decide cada agente", "🗄️ Datos (SQL)", "🎙️ Jarvis (voz)"]
)

# ---------- comparación ----------
with tab_cmp:
    st.markdown(
        "**Métrica principal:** ahorro promedio por factura frente a comprar el día 1.\n\n"
        "**Métricas secundarias:** porcentaje de facturas en que gana o pierde frente a la base y peor caso."
    )
    corridas, tiempos = simular_lote(con, df, agentes, monto, plazo, desde, hasta)
    if corridas.empty:
        st.warning("El periodo elegido es muy corto para ese plazo. Amplía el periodo.")
        st.stop()
    tabla = tabla_comparativa(corridas, tiempos, agentes)
    solo_agentes = solo_tecnicas(tabla)  # el 🏆 se elige solo entre técnicas, no entre modos base
    ganador = solo_agentes.loc[solo_agentes["Ahorro promedio vs base (S/)"].idxmax()]
    seguro = solo_agentes.loc[solo_agentes["Peor caso vs base (S/)"].idxmax()]

    c1, c2, c3 = st.columns(3)
    c1.metric("Facturas simuladas", f"{len(corridas)}", f"US$ {monto:,} a {plazo} días", delta_color="off")
    c2.metric("🏆 Técnica con mayor ahorro promedio", ganador["Estrategia"], f"S/ {ganador['Ahorro promedio vs base (S/)']:,.2f} por factura")
    c3.metric("🛡️ Técnica con menor pérdida en el peor caso", seguro["Estrategia"], f"S/ {seguro['Peor caso vs base (S/)']:,.2f}")

    st.caption(
        "Las técnicas destacadas pueden ser agentes distintos porque optimizan criterios diferentes: "
        "ahorro promedio y menor pérdida en el peor caso."
    )
    st.info(
        "**Óptimo (referencia, ve el futuro) NO es un agente.** Representa el mejor resultado posible "
        "con conocimiento del futuro y se usa solo como techo de referencia; no es implementable en la realidad."
    )
    tabla_vista = para_mostrar(tabla)
    # El Óptimo no se cronometra: ocultar solo su tiempo en la presentación.
    tabla_vista.loc[
        tabla_vista["Estrategia"] == "Óptimo (referencia, ve el futuro)", "Tiempo total (ms)"
    ] = float("nan")
    st.dataframe(
        tabla_vista.style.format({
            "Costo promedio (S/)": "{:,.2f}", "Ahorro promedio vs base (S/)": "{:+,.2f}",
            "Ahorro total (S/)": "{:+,.0f}", "Facturas en que gana a la base (%)": "{:.1f}", "Facturas en que pierde frente a la base (%)": "{:.1f}",
            "Mayor pérdida frente a la base (S/)": "{:+,.2f}", "Día promedio de compra": "{:.2f}", "Tiempo total (ms)": "{:.1f}",
        }, na_rep="—"),
        hide_index=True, width="stretch",
    )
    st.caption(
        "Cada corrida es una factura que empieza en un día hábil distinto del periodo. "
        "En «Mayor pérdida», un valor negativo indica pérdida; cero o positivo indica que no hubo pérdidas. "
        "«Tiempo total (ms)» mide el tiempo acumulado de las corridas, en milisegundos. "
        "El tiempo del Óptimo se muestra como «—» porque no se cronometra."
    )

    barras = alt.Chart(tabla_vista).mark_bar().encode(
        x=alt.X("Ahorro promedio vs base (S/):Q"),
        y=alt.Y("Estrategia:N", sort="-x", title=None),
        color=alt.condition(alt.datum["Ahorro promedio vs base (S/)"] >= 0, alt.value("#2e7d32"), alt.value("#c62828")),
        tooltip=list(tabla_vista.columns),
    ).properties(height=260, title="Ahorro promedio por factura frente a comprar el día 1")
    st.altair_chart(barras, width="stretch")

# ---------- caso ----------
with tab_caso:
    fechas_validas = corridas["inicio"].tolist()
    inicio = st.selectbox("Fecha en que llega la factura", fechas_validas, index=len(fechas_validas) - 1)
    i = df.index[df["fecha"] == pd.Timestamp(inicio)][0]
    ventana = df["fecha"].iloc[i:i + plazo].dt.strftime("%Y-%m-%d").tolist()
    perc = percepciones(con, ventana, monto)

    compras, trazas = [], {}
    for a in agentes:
        dia, traza = correr_agente(a, perc)
        trazas[a.nombre] = traza
        compras.append({"Estrategia": a.nombre, "fecha": pd.Timestamp(perc[dia]["fecha"]),
                        "Día": dia + 1, "TC": perc[dia]["tc_hoy"], "Costo (S/)": monto * perc[dia]["tc_hoy"]})
    compras = pd.DataFrame(compras)
    compras["Ahorro vs base (S/)"] = compras["Costo (S/)"].iloc[0] - compras["Costo (S/)"]

    serie = df.iloc[max(0, i - 15):i + plazo]
    linea = alt.Chart(serie).mark_line(color="#888").encode(
        x=alt.X("fecha:T", title=None), y=alt.Y("tc:Q", scale=alt.Scale(zero=False), title="S/ por US$"))
    plazo_area = alt.Chart(pd.DataFrame({"a": [pd.Timestamp(ventana[0])], "b": [pd.Timestamp(ventana[-1])]})) \
        .mark_rect(opacity=0.12, color="#1565c0").encode(x="a:T", x2="b:T")
    compras_vista = para_mostrar(compras)
    puntos = alt.Chart(compras_vista).mark_point(size=160, filled=True).encode(
        x="fecha:T", y="TC:Q", color="Estrategia:N", shape="Estrategia:N", tooltip=list(compras_vista.columns))
    st.altair_chart((plazo_area + linea + puntos).properties(height=320), width="stretch")
    st.caption("Zona azul = plazo para pagar. Cada marca es el día en que compró cada estrategia.")

    st.dataframe(compras_vista.drop(columns="fecha").style.format(
        {"TC": "{:.4f}", "Costo (S/)": "{:,.2f}", "Ahorro vs base (S/)": "{:+,.2f}"}),
        hide_index=True, width="stretch")

    elegido = st.selectbox("Ver qué percibió y decidió cada día", [a.nombre for a in agentes], index=5,
                           format_func=lambda nombre: ETIQUETAS_ESTRATEGIAS.get(nombre, nombre))
    st.dataframe(pd.DataFrame(trazas[elegido]), hide_index=True, width="stretch")

# ---------- voz ----------
with tab_voz:
    st.markdown(
        "Pregúntale en voz alta: *«¿a cuánto está el dólar?»*, *«tengo 5 días, ¿compro o espero?»* "
        "o *«¿cuál es la mejor estrategia?»*. Jarvis responde con la decisión del **agente de utilidad** "
        "sobre la última cotización y con la tabla de esta página."
    )
    audio = st.audio_input("Hablar con Jarvis")
    escrito = st.text_input("…o escríbele", placeholder="¿Compro o espero si me quedan 3 días?")
    pregunta = ""
    if audio is not None:
        try:
            pregunta = transcribir(audio.getvalue())
        except Exception as e:
            st.error(f"No pude procesar el audio ({e}). Prueba escribiendo la pregunta.")
        if audio is not None and not pregunta:
            st.warning("No te entendí. Habla más cerca del micrófono o escribe la pregunta.")
    pregunta = escrito.strip() or pregunta
    if pregunta:
        respuesta = responder(pregunta, con, df, monto, plazo, aversion, tabla)
        # Alinear la explicación visible con la tarjeta, reutilizando su resultado.
        if "El más seguro es " in respuesta:
            respuesta = respuesta.split("El más seguro es ", 1)[0] + (
                f"La técnica con menor pérdida en el peor caso es {seguro['Estrategia']}: "
                f"su resultado en el peor caso frente a comprar el día 1 es "
                f"S/ {seguro['Peor caso vs base (S/)']:,.2f}."
            )
        with st.chat_message("user"):
            st.write(pregunta)
        with st.chat_message("assistant", avatar="🤖"):
            st.write(respuesta)
            try:
                st.audio(sintetizar(respuesta), format="audio/mp3", autoplay=True)
            except Exception:
                st.caption("(Sin audio: no hay conexión con el servicio de voz.)")

# ---------- datos ----------
with tab_datos:
    st.markdown(
        f"Histórico USD/PEN, **{len(df)} días hábiles** ({fmin} a {fmax}), guardado en SQLite "
        "(tabla `tipo_cambio`). Cada día los agentes perciben con esta consulta, que nunca devuelve el futuro:"
    )
    st.code("SELECT tc FROM tipo_cambio\nWHERE fecha <= :hoy\nORDER BY fecha DESC\nLIMIT 20;", language="sql")
    st.altair_chart(alt.Chart(df).mark_line().encode(
        x=alt.X("fecha:T", title=None), y=alt.Y("tc:Q", scale=alt.Scale(zero=False), title="S/ por US$")
    ).properties(height=260), width="stretch")
    consulta = st.text_area("Prueba tu propia consulta SQL (solo lectura)",
                            "SELECT strftime('%Y', fecha) AS anio, ROUND(AVG(tc),4) AS promedio,\n"
                            "       MIN(tc) AS minimo, MAX(tc) AS maximo\nFROM tipo_cambio GROUP BY anio;")
    if consulta.strip().lower().startswith("select"):
        try:
            st.dataframe(pd.read_sql(consulta, con), hide_index=True)
        except Exception as e:
            st.error(f"Error en la consulta: {e}")
    else:
        st.info("Solo se permiten consultas SELECT.")

# ---------- agentes ----------
with tab_agentes:
    for a in agentes:
        nombre = ETIQUETAS_ESTRATEGIAS.get(a.nombre, a.nombre)
        if a is agentes[0]:
            st.markdown(f"**Base principal — {nombre}.** {a.descripcion}")
        elif a is agentes[1]:
            st.markdown(
                f"**Referencia aleatoria — {nombre}.** Elige un día al azar dentro del plazo. "
                "Sirve para saber si una técnica aporta algo más que la suerte; no es una técnica inteligente."
            )
        else:
            descripcion = a.descripcion
            if a is agentes[2]:
                descripcion = descripcion.replace("7 días", f"{dias_promedio} días")
            st.markdown(f"**{nombre}.** {descripcion}")
    st.info(
        "**Óptimo (referencia, ve el futuro):** no es un agente ni una estrategia implementable en la realidad. "
        "Elige el mejor día conociendo todas las cotizaciones futuras del plazo; es el techo de referencia."
    )
    st.markdown(
        "**Regla del entorno:** si llega el último día del plazo sin haber comprado, el agente está obligado a comprar.\n\n"
        f"**¿Qué percibe cada uno?** El reflejo solo mira hoy contra el promedio de {dias_promedio} días. El basado en modelo "
        "recuerda lo que vio ayer y arma una tendencia interna. El de objetivos se fija una meta de precio. "
        "El de utilidad además pesa **cuántos días quedan** y **qué tan volátil** está el dólar: mientras más días "
        "y más volatilidad, más riesgoso es esperar."
    )
