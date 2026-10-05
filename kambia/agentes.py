"""Agentes de KambIA. Cada día el agente recibe una percepción y responde COMPRAR o ESPERAR.

Percepción (la arma el simulador con SQL):
    tc_hoy           tipo de cambio de hoy
    historial        últimas 20 cotizaciones (la última es hoy)
    dias_restantes   días hábiles que quedan DESPUÉS de hoy antes de pagar
    monto            dólares que hay que pagar
"""
import random
import statistics

COMPRAR, ESPERAR = "COMPRAR", "ESPERAR"


class Agente:
    nombre = "Agente"
    descripcion = ""
    es_modo_base = False  # True en las estrategias que sirven de referencia (no son técnicas del curso)

    def reiniciar(self):
        """Se llama al empezar cada factura nueva (limpia el estado interno)."""

    def actuar(self, p):
        raise NotImplementedError


class AgenteBase(Agente):
    nombre = "Base (compra el día 1)"
    descripcion = "Lo que hace hoy el importador: compra los dólares apenas recibe la factura."
    es_modo_base = True

    def actuar(self, p):
        return COMPRAR, "Siempre compra apenas llega la factura."


class AgenteAleatorio(Agente):
    nombre = "Aleatorio (modo base 2)"
    descripcion = ("Segundo modo base, como permite la guía (manual, aleatorio o una regla de una línea): "
                   "elige un día al azar dentro del plazo. Sirve para saber si una técnica aporta algo más que la suerte.")
    es_modo_base = True

    def __init__(self, semilla=7):
        self.rng = random.Random(semilla)

    def actuar(self, p):
        # probabilidad 1/(días que quedan contando hoy) => día uniforme en el plazo
        prob = 1 / (p["dias_restantes"] + 1)
        if self.rng.random() < prob:
            return COMPRAR, f"Sorteo con probabilidad {prob:.0%}: salió comprar."
        return ESPERAR, f"Sorteo con probabilidad {prob:.0%}: salió esperar."


class AgenteReflejo(Agente):
    nombre = "Reflejo simple"
    descripcion = "Regla condición-acción: si el dólar está por debajo de su promedio de 7 días, compra."

    def __init__(self, dias_promedio=7):
        self.dias_promedio = dias_promedio

    def actuar(self, p):
        promedio = statistics.mean(p["historial"][-self.dias_promedio:])
        if p["tc_hoy"] <= promedio:
            return COMPRAR, f"S/{p['tc_hoy']:.4f} ≤ promedio {self.dias_promedio} días S/{promedio:.4f}."
        return ESPERAR, f"S/{p['tc_hoy']:.4f} > promedio {self.dias_promedio} días S/{promedio:.4f}."


class AgenteModelo(Agente):
    nombre = "Basado en modelo"
    descripcion = "Guarda un estado interno (tendencia suavizada del dólar) y compra cuando el dólar empieza a subir."

    def __init__(self, alfa=0.5):
        self.alfa = alfa
        self.reiniciar()

    def reiniciar(self):
        self.ultimo_tc = None
        self.tendencia = 0.0

    def actuar(self, p):
        if self.ultimo_tc is None:  # primer día: arranca el modelo con el historial
            self.ultimo_tc = p["historial"][-2]
            cambios = [b - a for a, b in zip(p["historial"][-6:-1], p["historial"][-5:])]
            self.tendencia = statistics.mean(cambios[:-1]) if len(cambios) > 1 else 0.0
        # actualiza el estado interno con lo que percibió hoy
        self.tendencia = self.alfa * (p["tc_hoy"] - self.ultimo_tc) + (1 - self.alfa) * self.tendencia
        self.ultimo_tc = p["tc_hoy"]
        if self.tendencia > 0:
            return COMPRAR, f"Tendencia interna {self.tendencia:+.4f}: el dólar sube, mejor comprar ya."
        return ESPERAR, f"Tendencia interna {self.tendencia:+.4f}: el dólar baja, conviene esperar."


class AgenteObjetivos(Agente):
    nombre = "Basado en objetivos"
    descripcion = "Fija una meta de precio el día 1 (promedio de 20 días menos un margen) y compra al alcanzarla."

    def __init__(self, margen=0.003):
        self.margen = margen
        self.reiniciar()

    def reiniciar(self):
        self.meta = None

    def actuar(self, p):
        if self.meta is None:
            self.meta = statistics.mean(p["historial"]) * (1 - self.margen)
        if p["tc_hoy"] <= self.meta:
            return COMPRAR, f"Meta cumplida: S/{p['tc_hoy']:.4f} ≤ meta S/{self.meta:.4f}."
        return ESPERAR, f"Aún no llega a la meta S/{self.meta:.4f} (hoy S/{p['tc_hoy']:.4f})."


class AgenteUtilidad(Agente):
    nombre = "Basado en utilidad"
    descripcion = ("Compara la utilidad de comprar hoy contra la de esperar: ahorro esperado "
                   "menos el riesgo de que el dólar se dispare, según volatilidad y días que quedan.")

    def __init__(self, aversion_riesgo=0.5):
        self.aversion_riesgo = aversion_riesgo  # λ: cuánto castiga el riesgo

    def actuar(self, p):
        hist, tc, d, monto = p["historial"], p["tc_hoy"], p["dias_restantes"], p["monto"]
        precio_esperado = statistics.mean(hist)  # supone que el dólar vuelve a su promedio de 20 días
        cambios = [b / a - 1 for a, b in zip(hist[:-1], hist[1:])]
        volatilidad = statistics.pstdev(cambios) if len(cambios) > 1 else 0.0

        u_comprar = -monto * tc
        riesgo = self.aversion_riesgo * monto * tc * volatilidad * d ** 0.5
        u_esperar = -monto * precio_esperado - riesgo

        detalle = f"U(comprar)=S/{u_comprar:,.0f} · U(esperar)=S/{u_esperar:,.0f} (riesgo S/{riesgo:,.0f})"
        return (ESPERAR if u_esperar > u_comprar else COMPRAR), detalle


def crear_agentes(dias_promedio=7, alfa=0.5, margen=0.003, aversion_riesgo=0.5, semilla=7):
    return [
        AgenteBase(),
        AgenteAleatorio(semilla),
        AgenteReflejo(dias_promedio),
        AgenteModelo(alfa),
        AgenteObjetivos(margen),
        AgenteUtilidad(aversion_riesgo),
    ]
