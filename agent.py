import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la API Key y el modelo de Nvidia
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
MODEL = os.getenv("NVIDIA_MODEL")

if not NVIDIA_API_KEY or NVIDIA_API_KEY == "TU_API_KEY_AQUI":
    print("Error: Por favor, configura tu NVIDIA_API_KEY en el archivo .env")
    sys.exit(1)

# Inicializar el cliente de OpenAI apuntando al endpoint de Nvidia Build
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)

# Nombre del archivo de FAQs
FAQ_FILE = "FAQs_Parachute_SA_Guatemala_2026.txt"

def read_faq_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{filepath}'.")
        sys.exit(1)

def get_system_prompt(faq_content):
    return f"""Eres un agente de preguntas frecuentes para la empresa Parachute S.A.
Tu objetivo es responder a las preguntas de los usuarios sobre un próximo evento.

REGLAS ESTRICTAS:
1. DEBES responder ÚNICAMENTE basándote en la información proporcionada en el siguiente documento de preguntas frecuentes.
2. Si la pregunta del usuario NO puede ser respondida con la información del documento, DEBES responder exactamente o algo muy similar a: "Lo siento, no tengo información sobre eso." o "No puedo responder a esa pregunta basándome en la información disponible." No inventes información.
3. Sé educado y profesional.

DOCUMENTO DE PREGUNTAS FRECUENTES:
{faq_content}
"""

def main():
    print("Cargando base de conocimiento...")
    faq_content = read_faq_file(FAQ_FILE)
    system_prompt = get_system_prompt(faq_content)
    
    print("Iniciando Agente de Preguntas Frecuentes de Parachute S.A...")
    print("Escribe 'Bye' para salir, o presiona Ctrl-C.")
    print("-" * 50)

    # Variable de control para el ciclo
    is_running = True
    
    # Historial de la conversación, iniciando con el prompt del sistema
    messages = [
        {"role": "system", "content": system_prompt}
    ]

    while is_running:
        try:
            # Obtener el input del usuario
            user_input = input("\nTú: ").strip()
            
            # Verificar si el usuario quiere salir
            if user_input.lower() == 'bye':
                print("Agente: ¡Hasta luego! Gracias por contactar a Parachute S.A.")
                is_running = False
                continue
                
            if not user_input:
                continue

            # Agregar la pregunta del usuario al historial
            messages.append({"role": "user", "content": user_input})

            # Realizar la llamada a la API
            # Se utiliza stream=True para mostrar la respuesta como si estuviera "escribiendo"
            response_stream = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.2, # Temperatura baja para que sea más determinista y siga el contexto
                top_p=0.7,
                max_tokens=1024,
                stream=True
            )

            print("Agente: ", end="", flush=True)
            full_response = ""
            
            # Iterar sobre el stream y mostrar los fragmentos
            for chunk in response_stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content
                    
            print() # Nueva línea al final de la respuesta
            
            # Agregar la respuesta del agente al historial para mantener el contexto en la sesión
            messages.append({"role": "assistant", "content": full_response})

        except KeyboardInterrupt:
            # Manejar la interrupción con Ctrl+C elegantemente
            print("\nAgente: Sesión terminada por el usuario (Ctrl-C). ¡Hasta luego!")
            is_running = False
            
        except EOFError:
            # Manejar Ctrl+D o fin de archivo
            print("\nAgente: Fin de entrada detectado. ¡Hasta luego!")
            is_running = False
            
        except Exception as e:
            # Manejar errores de API o de conexión sin botar el programa completo
            print(f"\n[Error de comunicación con la API]: {e}")
            print("Por favor, intenta tu pregunta nuevamente.")

if __name__ == "__main__":
    main()
