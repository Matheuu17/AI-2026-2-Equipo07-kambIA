# KambIA — Equipo ## 

**Problema y quién lo sufre.** Importadores, pymes y profesionales peruanos que reciben facturas en dólares y tienen unos días para pagarlas. Compran los dólares "cuando se acuerdan" y no saben si conviene comprar hoy o esperar. KambIA decide, día a día, **COMPRAR o ESPERAR** usando el histórico real USD/PEN.

**Modo base.** Lo que hace hoy el importador: compra los dólares el mismo día que llega la factura.

**Técnicas comparadas.**
- Parte 1 (bloque 1): agente aleatorio, reflejo simple, basado en modelo, basado en objetivos y basado en utilidad. Todos son agentes sobre datos que perciben con **SQL (SQLite)** y analizan con **pandas**.
- Parte 2: pendiente (regresión del tipo de cambio que alimente al agente de utilidad).

**Métrica.** Soles gastados por factura y ahorro frente al modo base. Todas las estrategias se miden sobre las mismas facturas.

| Técnica | Costo promedio (S/) | Ahorro vs base (S/) | Gana / pierde vs base | Peor caso (S/) | Tiempo | Corridas |
|---|---|---|---|---|---|---|
| Base (compra el día 1) | 35,737.00 | +0.00 | — | — | 0.3 ms | 632 |
| Aleatorio | 35,697.05 | +39.95 | 52% / 36% | −894 | 1.4 ms | 632 |
| Reflejo simple | 35,735.24 | +1.76 | 31% / 12% | −958 | 11.5 ms | 632 |
| Basado en modelo | 35,731.51 | +5.49 | 18% / 36% | −605 | 4.3 ms | 632 |
| Basado en objetivos | 35,715.33 | +21.67 | 38% / 20% | −980 | 7.5 ms | 632 |
| **Basado en utilidad** | 35,715.79 | +21.21 | 15% / **4%** | −627 | 44.9 ms | 632 |
| Óptimo (ve el futuro, solo referencia) | 35,505.43 | +231.57 | 85% / 0% | 0 | — | 632 |

*Condiciones: factura de US$ 10,000 con 10 días hábiles de plazo; una corrida por cada día de inicio entre abril de 2024 y octubre de 2026.* Lectura: el agente de utilidad ahorra tanto como el de objetivos, pero pierde contra la base solo en el 4 % de las facturas, porque considera el riesgo de esperar. El aleatorio sale bien únicamente porque el dólar bajó de S/ 3.75 a S/ 3.43 en ese periodo, y eso premia esperar. Si se filtra el periodo a meses en que el dólar subió, el resultado cambia.

**Cómo decide cada agente** (`kambia/agentes.py`):
- **Reflejo:** si el tipo de cambio de hoy es menor o igual al promedio de 7 días, COMPRAR; si no, ESPERAR.
- **Modelo:** guarda un estado interno, una tendencia suavizada con α. Si la tendencia sube, compra.
- **Objetivos:** el día 1 fija una meta (promedio de 20 días − 0.3 %) y compra cuando el precio la alcanza.
- **Utilidad:** compara U(comprar) = −monto·TC contra U(esperar) = −monto·promedio20 − λ·monto·TC·σ·√días. Elige la acción de mayor utilidad.
- **Entorno** (`kambia/simulador.py`): si llega el último día sin comprar, obliga a comprar.

**Extra: Jarvis por voz** (`kambia/voz.py`, pestaña 🎙️). Se le habla desde el navegador (por ejemplo, «tengo 5 días, ¿compro o espero?») y responde en voz alta con la decisión del agente de utilidad sobre la última cotización. Es la evolución del primer prototipo del equipo (`extras/jarvis_voz.py`): sigue siendo un agente reflejo por palabras clave, pero ahora conectado a los datos reales. Usa el reconocimiento de voz y la voz de Google, así que necesita internet.

**Cómo ejecutarlo.** Enlace público: `https://<pendiente>.streamlit.app`

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

En la app se pueden cambiar en vivo el monto, el plazo, el periodo, λ, α, el margen y los días del promedio.

**Datos.** `data/usdpen.csv`: tipo de cambio USD/PEN diario de días hábiles (marzo de 2024 a octubre de 2026), tomado de [fawazahmed0/currency-api](https://github.com/fawazahmed0/exchange-api). Se corrigieron 3 picos aislados de más de 1 % que se revertían al día siguiente.

**Uso de IA.** Se usó Claude (Anthropic) para generar la estructura inicial de `kambia/` y `app.py`. El equipo revisó y ajustó: *(completar qué cambió cada uno)*. El prototipo de voz `extras/jarvis_voz.py` (agente reflejo por palabras clave) fue la primera versión del equipo.

**Roles.**
- Integrante 1 (líder): … ([commits](#))
- Integrante 2: …
- Integrante 3: …
- Integrante 4: …
