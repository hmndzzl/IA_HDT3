# Agente de Preguntas Frecuentes (RAG) - Parachute S.A.

**Autor:** Hugo Méndez Lee - 241265

**Enlace al video de demostración:** [INSERTA EL LINK DEL VIDEO AQUÍ]

---

## 📖 Descripción del Proyecto
Este proyecto es una demostración de un agente inteligente de preguntas frecuentes desarrollado para la empresa ficticia **Parachute S.A**. Utiliza una arquitectura RAG (Retrieval-Augmented Generation) simple en la terminal. El agente carga información desde un archivo de texto plano con los detalles de un próximo evento de paracaidismo y utiliza un modelo de lenguaje grande (LLM) para responder a las preguntas del usuario **basándose estrictamente** en el contenido de dicho archivo.

Si el usuario hace una pregunta cuya respuesta no se encuentra en la base de conocimientos, el agente admitirá educadamente que no puede responderla, evitando alucinaciones y asegurando la veracidad de la información.

## 🚀 Tecnologías y Herramientas

*   **Python 3:** Lenguaje principal de desarrollo.
*   **OpenAI SDK:** Utilizado como cliente estándar (OpenAPI) para comunicarse con la API de generación de texto.
*   **NVIDIA Build (NIM):** Proveedor de la API y modelos de lenguaje.

### ¿Qué es NVIDIA Build y cómo fue utilizado?
NVIDIA Build (NIM - NVIDIA Inference Microservices) es una plataforma que ofrece acceso mediante API a una amplia variedad de modelos fundacionales (como los de la familia Llama, Mistral, Gemma, entre otros) alojados en la infraestructura acelerada por GPUs de NVIDIA. 

En este proyecto, se utilizó NVIDIA Build como proveedor del LLM. Aprovechando que su API es compatible con el estándar de OpenAI, simplemente redirigimos el SDK oficial de Python `openai` hacia el endpoint de NVIDIA (`https://integrate.api.nvidia.com/v1`). Esto permite usar modelos Open Source de alto rendimiento de manera sencilla y segura, protegiendo las credenciales mediante variables de entorno.

## 📂 Estructura del Proyecto

```text
IA_HDT3/
├── .env                  # Variables de entorno (API Key, Modelo) - No se sube al repositorio
├── .example_env          # Plantilla de variables de entorno requeridas
├── .gitignore            # Archivos excluidos del control de versiones
├── agent.py              # Script principal que ejecuta el Agente Conversacional y el ciclo RAG
├── FAQs_Parachute_SA_Guatemala_2026.txt # Base de conocimiento (Contexto para el modelo)
└── requirements.txt      # Dependencias del proyecto (openai, python-dotenv, httpx)
```

## ⚙️ Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de contar con lo siguiente:
1. **Python 3.8+** instalado en tu sistema. (Puedes verificarlo ejecutando `python --version` o `python3 --version` en tu terminal).
2. **Git** instalado para poder clonar el repositorio.
3. Una **cuenta activa en NVIDIA Build** ([build.nvidia.com](https://build.nvidia.com/)).
4. Una **API Key de NVIDIA** generada desde tu cuenta (no requiere tarjeta de crédito).

## 💻 Instrucciones de Instalación y Ejecución Local

Sigue estos pasos para clonar el proyecto y ejecutar el agente en tu propia terminal:

### 1. Clonar el repositorio y entrar al directorio
```bash
git clone https://github.com/hmndzzl/IA_HDT3.git
cd IA_HDT3
```

### 2. Crear y activar el entorno virtual
Es una buena práctica usar un entorno virtual para aislar las dependencias:
```bash
# Crear entorno virtual
python3 -m venv .venv

# Activar en Mac/Linux:
source .venv/bin/activate
# (Si usas Windows, ejecuta: .venv\Scripts\activate)
```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno
Crea un archivo llamado `.env` en la raíz del proyecto. Puedes basarte en el archivo `.example_env`. El archivo debe verse así:
```env
NVIDIA_API_KEY="tu_api_key_de_nvidia_aqui"
NVIDIA_MODEL="nombre_del_modelo_a_usar"
```
*(Nota: El nombre del modelo debe ser uno al que tengas acceso en tu cuenta de NVIDIA Build, por ejemplo: `meta/llama-3.1-8b-instruct`)*

### 5. Ejecutar el Agente
```bash
python agent.py
```
¡Listo! Ahora puedes empezar a chatear con el agente en tu terminal. Escribe tus preguntas o escribe `Bye` (o presiona `Ctrl-C`) para salir de la sesión.