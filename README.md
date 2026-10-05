# Jarvis Financiero - Fase 1: Agente de Reflejo Simple

## Descripción del Proyecto
Este proyecto es la primera iteración de un asistente virtual financiero (Jarvis) desarrollado para el curso de Agentes Inteligentes. En esta fase inicial, el sistema opera bajo la arquitectura de un **Agente de Reflejo Simple**.

El comportamiento del agente se basa estrictamente en reglas de condición-acción (if-then):
- **Percepción:** Captura el audio del entorno mediante el micrófono del usuario y lo convierte a texto en tiempo real (Speech-to-Text).
- **Procesamiento:** Evalúa el estímulo actual analizando la presencia de palabras clave específicas (ej. "dólar", "euro") dentro de su base de conocimiento estática (diccionario de reglas).
- **Acción:** Ejecuta el método correspondiente y responde inmediatamente a través de síntesis de voz (Text-to-Speech).

El agente no mantiene un historial de conversación ni evalúa el impacto a largo plazo de sus acciones; reacciona de forma autónoma y directa al estímulo presente.

## Tecnologías y Dependencias
El sistema está desarrollado en **Python** y requiere los siguientes módulos para la interacción por voz:

- `SpeechRecognition`: Para capturar y transcribir el audio a texto usando las APIs de Google.
- `pyttsx3`: Motor de síntesis de voz offline para generar las respuestas de audio sin latencia.
- `PyAudio`: Dependencia base multiplataforma que permite el acceso al hardware del micrófono.

## Instalación y Configuración

1. Clona el repositorio o descarga el archivo fuente `jarvis_reflejo.py`.
2. Abre una terminal en la carpeta del proyecto.
3. Instala las dependencias necesarias ejecutando el siguiente comando:

```bash
python -m pip install SpeechRecognition pyaudio pyttsx3
