# KambIA — Equipo ## 

**Problema y quién lo sufre.** Importadores, pymes y profesionales peruanos que reciben facturas en dólares y tienen unos días para pagarlas. Compran los dólares "cuando se acuerdan" y no saben si conviene comprar hoy o esperar. KambIA decide, día a día, **COMPRAR o ESPERAR** con el histórico real USD/PEN.

**Modo base.** (1) Lo que hace hoy el importador: comprar el mismo día que llega la factura. (2) Comprar un día al azar dentro del plazo, para saber si una técnica aporta algo más que la suerte.

**Técnicas comparadas.** Parte 1 (bloque 1): agentes **reflejo simple**, **basado en modelo**, **basado en objetivos** y **basado en utilidad**, todos sobre datos que perciben con **SQL (SQLite)** y analizan con **pandas**. Parte 2: pendiente (regresión del tipo de cambio que alimente al agente de utilidad).

**Métrica.** Soles gastados por factura y ahorro frente al modo base, sobre las mismas facturas para todos.

| Técnica | Costo prom. (S/) | Ahorro vs base (S/) | Gana / pierde vs base | Peor caso (S/) | Tiempo | Corridas |
|---|---|---|---|---|---|---|
| Base (compra el día 1) | 35,737.00 | +0.00 | — | — | 0.3 ms | 632 |
| Aleatorio (modo base 2) | 35,697.05 | +39.95 | 52% / 36% | −894 | 1.4 ms | 632 |
| Reflejo simple | 35,735.24 | +1.76 | 31% / 12% | −958 | 11.5 ms | 632 |
| Basado en modelo | 35,731.51 | +5.49 | 18% / 36% | −605 | 4.3 ms | 632 |
| Basado en objetivos | 35,715.33 | +21.67 | 38% / 20% | −980 | 7.5 ms | 632 |
| **Basado en utilidad** | 35,715.79 | +21.21 | 15% / **4%** | −627 | 44.9 ms | 632 |
| Óptimo (ve el futuro, solo referencia) | 35,505.43 | +231.57 | 85% / 0% | 0 | — | 632 |

*Factura de US$ 10,000 con 10 días hábiles de plazo; una corrida por cada día de inicio entre abril de 2024 y octubre de 2026.*

**Lectura.** El de utilidad ahorra casi lo mismo que el de objetivos, pero pierde contra la base solo en el 4 % de las facturas, porque pesa el riesgo de esperar. El aleatorio parece ganar solo porque el dólar bajó de S/ 3.75 a S/ 3.43 en el periodo. Por semestre (ahorro promedio por factura, S/):

| Semestre | Dólar | Aleatorio | Reflejo | Modelo | Objetivos | Utilidad |
|---|---|---|---|---|---|---|
| 2024-S1 | sube | −48.7 | +26.7 | −48.5 | −101.3 | −4.2 |
| 2025-S1 | baja | +96.1 | −34.2 | +33.9 | +45.6 | +24.7 |
| 2026-S1 | sube | −34.7 | −21.7 | +10.3 | +39.6 | +38.5 |
| 2026-S2 | sube | +2.8 | −20.0 | −17.6 | −4.1 | +6.4 |

Cuando el dólar sube, el aleatorio pierde y el de utilidad se mantiene: es la estrategia más robusta.

**Cómo decide cada agente** (`kambia/agentes.py`, método `actuar`; el ciclo percibir → actuar está en `correr_agente` de `kambia/simulador.py`):
- **Reflejo:** si el TC de hoy ≤ promedio de 7 días, COMPRAR; si no, ESPERAR.
- **Modelo:** guarda un estado interno (tendencia suavizada con α); si la tendencia sube, compra.
- **Objetivos:** el día 1 fija una meta (promedio de 20 días − margen) y compra al alcanzarla.
- **Utilidad:** U(comprar) = −monto·TC contra U(esperar) = −monto·promedio20 − λ·monto·TC·σ·√días; elige la mayor.
- **Entorno:** si llega el último día sin comprar, obliga a comprar.

**Cómo ejecutarlo.** Enlace público: `https://<pendiente>.streamlit.app`. En local:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

En la app se cambian en vivo el monto, el plazo, el periodo, λ, α, el margen y los días del promedio. Extras: pestaña **Jarvis (voz)**, que responde por voz con la decisión del agente de utilidad, y una consola SQL de solo lectura.

**Datos.** `data/usdpen.csv`: USD/PEN diario de días hábiles (marzo de 2024 a octubre de 2026), de [fawazahmed0/currency-api](https://github.com/fawazahmed0/exchange-api). Se corrigieron 3 picos aislados de más de 1 % que se revertían al día siguiente.

**Uso de IA.** Se usó Claude (Anthropic) para generar la estructura inicial de `kambia/` y `app.py`. El equipo revisó y ajustó: *(completar qué cambió cada uno)*. El prototipo de voz `extras/jarvis_voz.py` (agente reflejo por palabras clave) fue la primera versión del equipo y dio origen a `kambia/voz.py`.

**Roles.**
- Integrante 1 (líder): … ([commits](#))
- Integrante 2: …
- Integrante 3: …
- Integrante 4: …
