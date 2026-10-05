# Guion de la demo (5 minutos) y preguntas del examen oral

Todo se muestra desde el **enlace público**. Parámetros por defecto: US$ 10,000, plazo de 10 días hábiles, λ = 0.5.

## Minuto 0:00 – 1:00 · El problema

- "Un importador peruano recibe una factura de US$ 10,000 y tiene 10 días hábiles para pagarla. Hoy compra los dólares el mismo día que llega la factura. ¿Le conviene comprar hoy o esperar?"
- "Usamos el tipo de cambio real USD/PEN de marzo de 2024 a octubre de 2026: 660 días hábiles en SQLite."
- "Comparamos dos modos base (comprar el día 1 y comprar al azar) contra cuatro técnicas del bloque 1: reflejo, basado en modelo, basado en objetivos y basado en utilidad. La métrica es la misma para todos: **soles gastados y ahorro frente al modo base**."

## 1:00 – 2:30 · Pestaña Comparación

- "Simulamos **632 facturas**, una por cada día de inicio posible, y todas las estrategias resuelven las mismas facturas."
- Señalar la tabla:
  - "El de **objetivos** ahorra más en promedio: **S/ 21.67 por factura**."
  - "El de **utilidad** ahorra casi lo mismo, **S/ 21.21**, pero **solo pierde contra la base en el 4 % de las facturas**. El de objetivos pierde en el 20 %."
  - "El **Óptimo** ve el futuro: es el techo, **S/ 231.57**. Ningún agente real puede llegar ahí."
- "El aleatorio muestra +S/ 39.95, pero es un modo base: gana solo porque el dólar bajó de 3.75 a 3.43 en el periodo. En los semestres en que el dólar subió pierde: −48.7 en 2024-S1 y −34.7 en 2026-S1. El de utilidad se mantiene: +38.5 en 2026-S1."

## 2:30 – 4:00 · Una factura paso a paso

- Pestaña **Una factura paso a paso**: elegir la fecha más reciente.
- "La zona azul es el plazo; cada marca es el día en que compró cada estrategia."
- En "Ver qué percibió y decidió cada día", elegir **Basado en utilidad**:
  - "Cada día **percibe** el tipo de cambio de hoy y los últimos 20 días con esta consulta SQL (pestaña Datos), que nunca devuelve el futuro."
  - "Calcula U(comprar) y U(esperar), y **actúa** según cuál es mayor. Aquí se ve el número de cada día y el motivo."
- Mostrar en el código: `kambia/simulador.py` línea 36 (`agente.actuar(p)`, donde actúa) y `kambia/datos.py` línea 26 (la consulta SQL, donde percibe).

## 4:00 – 5:00 · Cambio en vivo con predicción

- **Decir la predicción ANTES de mover el control:** "Si subo la aversión al riesgo λ de 0.5 a 2, el agente de utilidad castiga tanto el riesgo de esperar que va a comprar siempre el día 1: se vuelve igual al modo base. Su ahorro caerá a casi cero y dejará de perder."
- Mover λ a 2.0. Resultado: **ahorro S/ 0.24, pierde 0 %, día promedio 1.0**.
- Bajar λ a 0: "Ahora no le importa el riesgo: ahorra un poco más (**S/ 24.27**), pero pierde el doble de veces (**8.9 %**) y su peor caso empeora a **−904**."
- Cierre: "λ es el control entre ahorrar y no arriesgar. Por eso el de utilidad es nuestra técnica más robusta."

## Preguntas probables (Anexo 03) con nuestros números

1. **¿Dónde percibe y dónde actúa?** Percibe en `kambia/simulador.py` → `percepciones()` (línea 20), que llama a `historial_hasta()` de `kambia/datos.py` (consulta SQL, línea 26). Actúa en `correr_agente()` (línea 36: `agente.actuar(p)`); cada agente decide en su método `actuar()` de `kambia/agentes.py`.
2. **¿Qué generó la IA y qué cambiaron?** La estructura inicial de `kambia/` y `app.py` se generó con Claude. *(Cada integrante dice qué revisó o cambió: por ejemplo, el umbral del reflejo, la fórmula de riesgo, la tabla por semestre.)*
3. **Cambie un parámetro y prediga.** λ = 2 → compra el día 1 y ahorro ≈ 0 (S/ 0.24, pierde 0 %). λ = 0 → más ahorro (S/ 24.27) pero más pérdidas (8.9 %). Plazo 20 → el de objetivos sube a S/ 69.4 porque tiene más días para que llegue su meta; plazo 5 → todos ahorran menos (objetivos S/ 7.5, utilidad S/ 3.6).
4. **¿Por qué el reflejo pierde contra el de utilidad? ¿Qué percibe uno que el otro ignora?** El reflejo solo compara hoy contra el promedio de 7 días. El de utilidad además percibe **cuántos días quedan** y **qué tan volátil está el dólar**, y pesa el riesgo de esperar. Resultado: el reflejo ahorra S/ 1.76 y pierde el 12 % de las veces; el de utilidad ahorra S/ 21.21 y pierde el 4 %.
5. **¿Por qué esa métrica?** Al importador le importa cuántos soles paga. El ahorro frente a la base dice directamente si la técnica le sirve. El % de facturas en que pierde y el peor caso miden el riesgo.
6. **¿Con cuántos datos lo midieron? ¿Es suficiente?** 632 facturas sobre 660 días hábiles reales. Las facturas se solapan (días seguidos), así que no son 632 casos independientes. Por eso además lo mostramos por semestre: el de utilidad es positivo o casi cero en todos los semestres; el aleatorio no.
7. **Si los datos fueran 10 veces más grandes, ¿qué se cae primero?** El de utilidad es el más lento (44.9 ms en 632 facturas, porque calcula la volatilidad cada día), pero sigue siendo instantáneo. La consulta SQL tiene índice por fecha, así que escala bien.
8. **¿Cuándo el modo base sería mejor que su técnica?** Cuando el dólar sube sin pausa todo el plazo: esperar siempre sale caro. Por ejemplo en 2024-S1 (3.75 → 3.83), donde el de utilidad perdió S/ 4.2 por factura y el de objetivos S/ 101.3.
9. **¿Quién lo sufre y qué faltó para hacerlo real?** Importadores y pymes que pagan en dólares. Faltan el tipo de cambio de compra y venta de cada banco o casa de cambio (no solo el de mercado) y las comisiones. Riesgo ético: es una recomendación, no asesoría financiera; la decisión final es del usuario.
