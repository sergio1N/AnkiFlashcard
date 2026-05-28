import os
import re
from datetime import datetime
from ia import generar_tarjeta
from Anki import añadir_a_anki

print("Iniciando extracción de datos...")
#ruta de notas
ruta_base = r"C:\Github\obsidiana-notes\Personal\daily notes"

fecha_hoy = datetime.now().strftime("%Y-%m-%d")
archivo_hoy = os.path.join(ruta_base, f"{fecha_hoy}.md") #Nombre del archivo a extraer datos.

def extraer_datos():
    if not os.path.exists(archivo_hoy):
        print("No se encontró la nota de hoy.")
        return None

    with open(archivo_hoy, "r", encoding="utf-8") as f:
        contenido = f.read()

    # Captura: número. [palabra] (salto de línea) context: texto
    pattern = r"\d+\.\s*\[([^\]]+)\]\s*\n\s*context:\s*(.+)"
    matches = re.findall(pattern, contenido, re.IGNORECASE)
    
    return matches

# Ejemplo de uso
datos = extraer_datos()
print("Datos extraídos:", datos)

# Procesar en IA
for palabra, contexto in datos:
    tarjeta = generar_tarjeta(palabra, contexto)
    print(f"Tarjeta generada:\n{tarjeta}")
    partes = tarjeta.strip().split('|')
    frente_anki = f"{partes[0]}<br><small>{partes[1]}</small>"
    reverso_anki = f"{partes[2]}<br><br><b>Ejemplo:</b> {partes[3]}<br><i>{partes[4]}</i>"

    #inyectar a Anki
    resultado = añadir_a_anki(frente_anki, reverso_anki)
    print(f"Resultado de inyección: {resultado}")