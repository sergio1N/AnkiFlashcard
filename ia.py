import os
from dotenv import load_dotenv
from groq import Groq
import requests
import base64

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
UNSPLASH_KEY   = os.getenv("UNSPLASH_API_KEY")
ANKI_URL       = 'http://localhost:8765'



client = Groq(api_key=api_key)

def generar_tarjeta(palabra, contexto):
    prompt = f"""
        Actúa como un profesor de inglés experto. Crea una tarjeta de Anki para la palabra: '{palabra}'.
        El usuario la encontró en este contexto: '{contexto}'.
        
        Tu respuesta debe ser una sola línea de texto con este formato exacto, usando '|' como separador:
        [PALABRA]|[PRONUNCIACIÓN RESPEL]|[TRADUCCIÓN]|[ORACIÓN EJEMPLO]|[TRADUCCIÓN EJEMPLO]|[IMAGEN]
        
        Reglas estrictas:
        1. No escribas nada más, ni introducciones, ni comentarios.
        2. Significado (TRADUCCIÓN): Da 1-2 sinónimos en español separados por " / " 
        y añade entre paréntesis una micro-definición de máximo 6 palabras que 
        capture el matiz clave. Ejemplo: "evitar / eludir (alejarse algo deliberadamente)".
        Si es verbo irregular añade al final: (inf:base, part:participio).
        3. Contexto: úsalo para determinar el significado correcto pero NO lo repliques en la tarjeta.
        4. Oración de ejemplo: nivel B1/B2, natural y simple.
        5. Traducción de la oración: al español de forma natural.
        6. IMAGEN: responde únicamente SI o NO.
           - SI: si la palabra puede representarse fácilmente con una foto real
             (objetos, acciones físicas, animales, lugares, personas haciendo algo concreto).
             Ejemplos: deliver, run, bridge, dog, forest.
           - NO: si la palabra es abstracta, gramatical o difícil de ilustrar con una foto.
             Ejemplos: although, therefore, despite, able, whether.
        
        Respuesta:
    """
 
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
 
    return chat_completion.choices[0].message.content
 

# ─── Buscar imagen en Unsplash y subirla a Anki ───────────────────────────────
 
def buscar_y_subir_imagen(palabra):
    try:
        r = requests.get(
            "https://api.unsplash.com/search/photos",
            params={"query": palabra, "per_page": 1, "orientation": "landscape"},
            headers={"Authorization": f"Client-ID {UNSPLASH_KEY}"}
        )
        datos = r.json()
 
        if not datos.get("results"):
            print(f"  Sin imagen para '{palabra}' en Unsplash.")
            return ""
 
        url_imagen = datos["results"][0]["urls"]["small"]
        img_data   = requests.get(url_imagen).content
        img_b64    = base64.b64encode(img_data).decode("utf-8")
        nombre     = f"ib_{palabra.lower()}_img.jpg"
 
        resultado = requests.post(ANKI_URL, json={
            "action": "storeMediaFile",
            "version": 6,
            "params": {"filename": nombre, "data": img_b64}
        }).json()
 
        if resultado.get("error"):
            print(f"  Error subiendo imagen: {resultado['error']}")
            return ""
 
        print(f"  Imagen subida: {nombre}")
        return nombre
 
    except Exception as e:
        print(f"  Error buscando imagen: {e}")
        return ""