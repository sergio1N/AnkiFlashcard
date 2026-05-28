import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY no está definida en el entorno")


client = Groq(api_key=api_key)

def generar_tarjeta(palabra, contexto):
    prompt = f"""
        Actúa como un profesor de inglés experto. Crea una tarjeta de Anki para la palabra: '{palabra}'.
        El usuario la encontró en este contexto: '{contexto}'.
        
        Tu respuesta debe ser una sola línea de texto con este formato exacto, usando '|' como separador de campos:
        [PALABRA]|[PRONUNCIACIÓN RESPEL]|[TRADUCCIÓN]|[ORACIÓN EJEMPLO]|[TRADUCCIÓN EJEMPLO]
        
        Reglas estrictas de contenido:
        1. No escribas nada más, ni introducciones, ni comentarios.
        2. Significado (TRADUCCIÓN): 
           - Debe ser preciso, sencillo y al grano.
           - Si la palabra es un verbo irregular, añade obligatoriamente al final: (inf:base, part:participio). Ejemplo: "vio (inf:see, part:seen)".
           - Si no es verbo irregular, solo pon la traducción simple sin paréntesis.
        3. Contexto: Úsalo fundamentalmente para determinar el significado correcto, pero NO lo repliques dentro de la tarjeta.
        4. Oración de ejemplo: Nivel B1/B2, natural y simple.
        5. Traducción de la oración: Tradúcela al español de forma natural.
        6. Si no hay contexto útil, utiliza el significado más común de la palabra.
        
        Respuesta:
    """

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile", # modelo de ia (puede requerir updates según disponibilidad)
    )
    
    return chat_completion.choices[0].message.content

