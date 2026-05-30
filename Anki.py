import requests
import base64
import os
import tempfile
from gtts import gTTS
from ia import buscar_y_subir_imagen

ANKI_URL= 'http://localhost:8765'
MODELO= "Ingles_Boost"
MAZO= "Ingles"


# ─── Generar audio y subirlo a Anki ───────────────────────────────────────────
 
def generar_y_subir_audio(texto, nombre_archivo):
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        ruta_tmp = tmp.name
 
    tts = gTTS(text=texto, lang='en', slow=False)
    tts.save(ruta_tmp)
 
    with open(ruta_tmp, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode("utf-8")
 
    os.remove(ruta_tmp)
 
    resultado = requests.post(ANKI_URL, json={
        "action": "storeMediaFile",
        "version": 6,
        "params": {"filename": nombre_archivo, "data": audio_b64}
    }).json()
 
    if resultado.get("error"):
        print(f"  Error subiendo audio '{nombre_archivo}': {resultado['error']}")
        return ""
 
    return f"[sound:{nombre_archivo}]"
 

 
# ─── Plantilla HTML ────────────────────────────────────────────────────────────
 
FRENTE_HTML = """
<style>
  .card-wrap {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    max-width: 420px;
    margin: 20px auto;
    padding: 1.5rem;
    border-radius: 14px;
    border: 1px solid #3a3a3a;
    background: transparent;
  }
  .label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #666;
    margin-bottom: 1rem;
  }
  .word {
    font-size: 38px;
    font-weight: 500;
    color: #7F77DD;
    margin: 0 0 6px;
  }
  .pronun {
    font-size: 15px;
    color: #999;
    margin: 0 0 4px;
  }
  .prompt {
    font-size: 12px;
    color: #555;
    margin-top: 1.5rem;
    font-style: italic;
  }
</style>
 
<div class="card-wrap">
  <p class="label">¿Sabes qué significa?</p>
  <p class="word">{{Palabra}}</p>
  <p class="pronun">/ {{Pronunciacion}} /</p>
  {{Audio}}
  <p class="prompt">Piensa en la traducción antes de voltear.</p>
</div>
"""
 
REVERSO_HTML = """
<style>
  .card-wrap {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    max-width: 420px;
    margin: 20px auto;
    padding: 1.5rem;
    border-radius: 14px;
    border: 1px solid #3a3a3a;
    background: transparent;
  }
  .label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #666;
    margin-bottom: 1rem;
  }
  .word {
    font-size: 38px;
    font-weight: 500;
    color: #7F77DD;
    margin: 0 0 4px;
  }
  .pronun {
    font-size: 14px;
    color: #999;
    margin: 0 0 14px;
  }
  .divider {
    border: none;
    border-top: 1px solid #3a3a3a;
    margin: 14px 0;
  }
  .transl {
    font-size: 24px;
    font-weight: 500;
    color: #1D9E75;
    margin: 0 0 16px;
  }
  .example {
    font-size: 14px;
    color: #aaaaaa;
    font-style: italic;
    line-height: 1.7;
    margin: 0;
  }
  .example b {
    color: #7F77DD;
    font-style: normal;
    font-weight: 500;
    text-decoration: underline;
    text-underline-offset: 3px;
  }
  .reveal-btn {
    margin-top: 12px;
    font-size: 12px;
    padding: 5px 14px;
    border-radius: 8px;
    background: #2a2a2a;
    border: 1px solid #3a3a3a;
    color: #888;
    cursor: pointer;
    display: inline-block;
  }
  .transl-example {
    font-size: 13px;
    color: #aaaaaa;
    font-style: italic;
    line-height: 1.7;
    margin-top: 8px;
    display: none;
  }
  .card-img {
    width: 100%;
    border-radius: 10px;
    margin-top: 1.2rem;
    opacity: 0.9;
    height: 90%;
  }
</style>
 
<div class="card-wrap">
 {{#Imagen}}<img class="card-img" src="{{Imagen}}">{{/Imagen}}
  <p class="label">Resultado</p>
  <p class="word">{{Palabra}}</p>
  <p class="pronun">/ {{Pronunciacion}} /</p>
  <hr class="divider">
  <p class="transl">{{Traduccion}}</p>
  <p class="example">{{Ejemplo}}</p>
  {{AudioEjemplo}}
  <p class="transl-example" id="te">{{EjemploTrad}}</p>
  <button class="reveal-btn" id="btn"
    onclick="document.getElementById('te').style.display='block';
             document.getElementById('btn').style.display='none';">
    ver traducción del ejemplo
  </button>

</div>
"""
 
# ─── Crear modelo si no existe ─────────────────────────────────────────────────
 
def crear_modelo_si_no_existe():
    r = requests.post(ANKI_URL, json={
        "action": "modelNames",
        "version": 6
    }).json()
 
    if MODELO in r.get("result", []):
        print(f"Modelo '{MODELO}' ya existe, omitiendo creación.")
        return
 
    payload = {
        "action": "createModel",
        "version": 6,
        "params": {
            "modelName": MODELO,
            "inOrderFields": [
                "Palabra", "Pronunciacion", "Traduccion",
                "Ejemplo", "EjemploTrad", "Audio", "AudioEjemplo", "Imagen"
            ],
            "css": "",
            "cardTemplates": [{
                "Name": "Ingles_Boost_Card",
                "Front": FRENTE_HTML,
                "Back": REVERSO_HTML
            }]
        }
    }
 
    resultado = requests.post(ANKI_URL, json=payload).json()
 
    if resultado.get("error"):
        print(f"Error creando modelo: {resultado['error']}")
    else:
        print(f"Modelo '{MODELO}' creado correctamente.")
 
# ─── Añadir nota ───────────────────────────────────────────────────────────────
 
def añadir_a_anki(palabra, pronunciacion, traduccion, ejemplo, ejemplo_trad, usar_imagen):
    import re
 
    ejemplo_html = re.sub(
        rf'\b({re.escape(palabra)})\b',
        r'<b>\1</b>',
        ejemplo,
        flags=re.IGNORECASE
    )
 
    ejemplo_limpio = re.sub(r'<[^>]+>', '', ejemplo)
    print(f"  Generando audio: palabra...")
    tag_audio_palabra = generar_y_subir_audio(palabra, f"ib_{palabra.lower()}_word.mp3")
    print(f"  Generando audio: ejemplo...")
    tag_audio_ejemplo = generar_y_subir_audio(ejemplo_limpio, f"ib_{palabra.lower()}_example.mp3")
 
    nombre_imagen = ""
    if usar_imagen:
        print(f"  Buscando imagen para '{palabra}'...")
        nombre_imagen = buscar_y_subir_imagen(palabra)
 
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": MAZO,
                "modelName": MODELO,
                "fields": {
                    "Palabra":       palabra,
                    "Pronunciacion": pronunciacion,
                    "Traduccion":    traduccion,
                    "Ejemplo":       ejemplo_html,
                    "EjemploTrad":   ejemplo_trad,
                    "Audio":         tag_audio_palabra,
                    "AudioEjemplo":  tag_audio_ejemplo,
                    "Imagen":        nombre_imagen
                },
                "options": {"allowDuplicate": False}
            }
        }
    }
 
    response = requests.post(ANKI_URL, json=payload).json()
 
    if response.get("error"):
        print(f"  Error al añadir '{palabra}': {response['error']}")
    else:
        print(f"  Tarjeta '{palabra}' añadida con ID: {response['result']}")
 
    return response