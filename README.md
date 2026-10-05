# KambIA — Equipo 07

## Problema y quién lo sufre

Importadores, pymes y profesionales peruanos que reciben facturas en dólares deben decidir cuándo comprar USD para realizar sus pagos. Normalmente toman esta decisión sin analizar el comportamiento reciente del tipo de cambio.

**KambIA** compara distintas estrategias que deciden diariamente entre **COMPRAR** o **ESPERAR**, utilizando datos históricos reales del tipo de cambio USD/PEN.

## Modo base y técnicas comparadas

**Modo base principal:** comprar los dólares el mismo día en que se recibe la factura.

**Referencia adicional:** elegir aleatoriamente un día dentro del plazo de pago, para comparar si las técnicas inteligentes aportan más que una decisión al azar.

**Técnicas del bloque 1:**

- Agente reflejo simple.
- Agente basado en modelo.
- Agente basado en objetivos.
- Agente basado en utilidad.

Los agentes perciben datos almacenados en **SQLite** y los procesan mediante **pandas**.

> El modo **Óptimo** mostrado en la aplicación no es un agente real. Utiliza información futura únicamente como referencia del máximo ahorro posible.

## Métrica

La métrica principal es el **ahorro promedio por factura frente al modo base de comprar el día 1**.

Como métricas secundarias se utilizan:

- costo promedio en soles;
- porcentaje de facturas en que se gana o pierde frente a la base;
- mayor pérdida frente a la base;
- tiempo de ejecución.

## Resultados de referencia

Los siguientes resultados corresponden a una configuración de referencia de:

- **Factura:** US$ 10,000.
- **Plazo:** 10 días hábiles.
- **Periodo histórico:** abril de 2024 a octubre de 2026.
- **Corridas:** 632 simulaciones utilizando distintos días de inicio.

Los resultados pueden cambiar al modificar los parámetros desde la aplicación.

| Técnica | Costo prom. (S/) | Ahorro prom. vs base | Gana / pierde vs base | Mayor pérdida |
|---|---:|---:|---:|---:|
| Base (día 1) | 35,737.00 | S/ 0.00 | — | — |
| Aleatorio | 35,697.05 | S/ 39.95 | 52% / 36% | S/ -894 |
| Reflejo simple | 35,735.24 | S/ 1.76 | 31% / 12% | S/ -958 |
| Basado en modelo | 35,731.51 | S/ 5.49 | 18% / 36% | S/ -605 |
| Basado en objetivos | 35,715.33 | **S/ 21.67** | 38% / 20% | S/ -980 |
| Basado en utilidad | 35,715.79 | S/ 21.21 | 15% / **4%** | S/ -627 |

Con esta configuración, el **agente basado en objetivos obtiene el mayor ahorro promedio**, mientras que el **agente basado en utilidad pierde frente al modo base con menor frecuencia**, mostrando un comportamiento más conservador frente al riesgo.

## Prototipo

La aplicación permite modificar en tiempo real:

- monto de la factura;
- plazo de pago;
- periodo histórico;
- ventana del agente reflejo;
- parámetro α del agente basado en modelo;
- margen del agente basado en objetivos;
- aversión al riesgo λ del agente basado en utilidad.

También incluye:

- comparación general de estrategias;
- simulación de una factura paso a paso;
- explicación de cómo decide cada agente;
- visualización de datos mediante SQL;
- Jarvis como funcionalidad adicional por voz.

**Enlace público:**

https://ai-2026-2-equipo07-kambia-qt54q7quwsjfbk9zzyzoia.streamlit.app/

## Ejecución local

Crear el entorno virtual:

```bash
python -m venv .venv
```

### macOS / Linux

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Windows

```bash
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Datos

Se utiliza un histórico diario USD/PEN almacenado en `data/usdpen.csv`, que posteriormente se carga en SQLite para realizar las simulaciones.

Los datos utilizados corresponden al histórico USD/PEN empleado por el proyecto durante el periodo evaluado.

## Uso de IA

Se utilizó **Claude (Anthropic)** como apoyo para generar una primera estructura del proyecto, incluyendo una base inicial de `kambia/` y `app.py`.

A partir de esa base se utilizó **OpenAI Codex** para continuar el desarrollo y refinamiento del proyecto, incluyendo ajustes en la aplicación Streamlit, organización y presentación de las comparaciones entre agentes, mejoras de claridad en la interfaz, revisión del repositorio y apoyo en tareas de mantenimiento y documentación.

El equipo revisó, modificó y adaptó el código generado con IA. Todos los integrantes son responsables de comprender y explicar el funcionamiento de las partes presentadas.

## Roles

- **Alcalá Barzola, Matias Alejandro — Líder:** creación inicial del repositorio, coordinación del proyecto y organización de la entrega.
- **Morales Silva, Omar Jean Piere:** implementación principal de KambIA, incluyendo los modos base y agentes del bloque 1, integración con SQLite, simulador, aplicación Streamlit y asistente de voz.
- **Maquen Caisan, Fabian:** ajustes del proyecto según la rúbrica, incorporación y documentación de la referencia aleatoria, revisión de resultados, mejoras de presentación y claridad de la aplicación, documentación y limpieza del repositorio.