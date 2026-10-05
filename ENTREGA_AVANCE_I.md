# Avance I (semana 8): qué pide la guía, cómo estamos y qué falta

Revisión de KambIA contra la *Guía de Trabajo Final* (secciones 5 a 9, Anexo 01 y Anexo 03).

## 1. Qué debe funcionar en la Parte 1

| Requisito | Estado | Dónde |
|---|---|---|
| Problema real y quién lo sufre | ✅ | README, primer párrafo |
| Modo base | ✅ | `AgenteBase` (compra el día 1) y `AgenteAleatorio` (modo base 2) |
| Al menos dos técnicas del bloque 1 | ✅ (4) | Reflejo, modelo, objetivos y utilidad, más SQL + pandas |
| Misma métrica para todas | ✅ | Soles gastados y ahorro vs base, sobre las mismas 632 facturas |
| Tabla comparativa dentro del prototipo | ✅ | Pestaña **Comparación** |
| En línea | ❌ | Falta publicar (ver sección 4) |

La guía pide **al menos** dos técnicas. Tener cuatro suma, siempre que **cada integrante pueda explicar las cuatro**.

## 2. Entregables (sección 7)

| Entregable | Estado | Qué falta |
|---|---|---|
| a) Enlace público | ❌ | Publicar en Streamlit Community Cloud |
| b) Repo `AI-2026-2-Equipo##-nombre-corto` | ❌ | Renombrar `jarvis-financiero` (por ejemplo `AI-2026-2-Equipo07-kambia`) |
| b) Commits de **todos** los integrantes | ❌ | "Sin commits, sin proyecto": cada uno debe tener commits propios |
| c) README de una página | 🟡 | Completar número de equipo, enlace, uso de IA por integrante y roles |
| d) Demo de 5 minutos | 🟡 | Guion listo en `GUION_DEMO.md`; falta ensayarlo |

## 3. Rúbrica (20 puntos): dónde estamos

| Criterio | Hoy | Para el 5 |
|---|---|---|
| Funciona en línea (5) | 1 (solo local) | El enlace abre en el navegador del docente y la comparación corre completa |
| Preguntas del docente (5, individual) | depende de cada uno | Ubicar en el código, explicar con números por qué ganó una técnica y predecir el efecto de un parámetro (ver `GUION_DEMO.md`) |
| Creatividad (2) + puntualidad (1) + voluntariado (2) | 2 + ? + ? | Creatividad asegurada (problema propio, datos reales, Óptimo como techo, voz, consola SQL). Entregar el enlace a tiempo y **ofrecerse como voluntarios** |
| Coevaluación (5) | votos de la clase | App clara, demo sin fallas |

Ojo: quien no pueda explicar código que presentó como propio saca 0 en Preguntas. Por eso hay que declarar el uso de IA y repasar el código.

## 4. Pendientes en orden de impacto

1. [ ] **Publicar en Streamlit Community Cloud** (vale de 1 a 5 puntos). Lo hace quien tenga acceso al repo:
   share.streamlit.io → *Create app* → repo y rama → archivo `app.py` → *Advanced settings* → Python **3.12** → *Deploy*. Copiar el enlace al README.
2. [ ] **Renombrar el repo** a `AI-2026-2-Equipo##-kambia` (GitHub → Settings → Repository name). Lo hace el dueño.
3. [ ] **Commits de cada integrante** con su propia cuenta y trabajo real: uno completa los roles del README, otro el uso de IA, otro ensaya y ajusta el guion, otro revisa un agente y comenta su código.
4. [ ] **Completar el README**: número de equipo, enlace público, qué cambió cada uno respecto a lo generado con IA, y roles con enlaces a sus commits.
5. [ ] **Ensayar la demo** (`GUION_DEMO.md`) desde el enlace público, con el cronómetro.
6. [ ] **Cada integrante practica las preguntas del Anexo 03** con las respuestas de `GUION_DEMO.md`. El docente elige al azar quién responde.
7. [ ] **Ofrecerse como voluntarios** para exponer: son 2 puntos.

## 5. Cambios hechos en esta rama

- El 🏆 de la app y la respuesta de Jarvis se eligen solo entre **técnicas**. El aleatorio se presenta como **segundo modo base**, como lo permite la guía ("manual, aleatorio o una regla de una línea"). Antes la app mostraba "Aleatorio" como ganador, que es lo primero que cuestionaría el docente.
- README: tabla por semestre que explica por qué el aleatorio parece ganar (el dólar bajó en el periodo) y por qué el de utilidad es el más robusto.
- `requirements.txt`: `streamlit>=1.50`, porque la app usa `width="stretch"`, que no existe en versiones anteriores.

## 6. Extras que se quedan (suman en creatividad y en la defensa)

- **Óptimo (ve el futuro)**: techo de ahorro posible; da contexto a la tabla.
- **Una factura paso a paso**: muestra qué percibe y qué decide cada agente cada día. Responde directo la pregunta 1 del Anexo 03.
- **Consola SQL** de solo lectura: demuestra el tema "agentes sobre datos con SQL".
- **Parámetros en vivo** (λ, α, margen, plazo, periodo): el docente puede pedir cambios en vivo.
- **Jarvis (voz)**: evolución del primer prototipo del equipo, ahora conectado a los agentes.
