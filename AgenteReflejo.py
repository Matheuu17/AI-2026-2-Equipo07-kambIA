import speech_recognition as sr
import pyttsx3

class JarvisFinancieroReflejo:
    def __init__(self):
        # Coonfiguracion del TTS
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 160) 
        
        # Configuracion del STT
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Reglas
        self.reglas = {
            "dólar": self.consultar_dolar,
            "dolar": self.consultar_dolar,
            "euro": self.consultar_euro,
            "hola": self.saludar,
            "saludo": self.saludar
        }

    def hablar(self, texto):
        """Convierte texto en audio reproducible."""
        print(f"Jarvis: {texto}")
        self.engine.say(texto)
        self.engine.runAndWait()

    def escuchar(self):
        """Captura audio del micrófono y lo traduce a texto."""
        with self.microphone as source:
            print("\nEscuchando...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
            audio = self.recognizer.listen(source)

        try:
            texto = self.recognizer.recognize_google(audio, language="es-ES")
            print(f"Tú (Voz detectada): {texto}")
            return texto
        except sr.UnknownValueError:
            return "" # Si no entendió
        except sr.RequestError:
            self.hablar("Error de conexión al procesar el audio.")
            return ""

    def actuar(self, estimulo):
        """Evalúa la regla de condición-acción."""
        estimulo_limpio = estimulo.lower()

        for palabra_clave, accion in self.reglas.items():
            if palabra_clave in estimulo_limpio:
                return accion()

        return "Lo siento, señor. Mi protocolo actual solo reconoce consultas sobre el dólar o el euro."

    # --- Métodos de acción ---
    def consultar_dolar(self):
        return "El tipo de cambio del dólar hoy es compra tres punto setenta y cinco, venta tres punto setenta y ocho."

    def consultar_euro(self):
        return "El euro se cotiza actualmente en cuatro punto doce."

    def saludar(self):
        return "A sus servicios, señor. ¿Qué indicador financiero requiere hoy?"


# --- Ejecución interactiva por voz ---
if __name__ == "__main__":
    jarvis = JarvisFinancieroReflejo()
    jarvis.hablar("Sistemas en línea. Jarvis escuchando.")

    while True:
        orden_voz = jarvis.escuchar()

        if not orden_voz:
            continue

        if any(palabra in orden_voz.lower() for palabra in ["salir", "apagar", "adiós", "terminar"]):
            jarvis.hablar("Desconectando sistemas. Hasta luego, señor.")
            break

        respuesta = jarvis.actuar(orden_voz)
        jarvis.hablar(respuesta)