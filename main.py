import os
import re
from datetime import datetime
from ia import generar_tarjeta
from anki import crear_modelo_si_no_existe, añadir_a_anki

print("Iniciando extracción de datos...")

# ─── Ruta de notas ─────────────────────────────────────────────────────────────
ruta_base   = r"C:\Github\obsidiana-notes\Personal\daily notes"
fecha_hoy   = datetime.now().strftime("%Y-%m-%d")
archivo_hoy = os.path.join(ruta_base, f"{fecha_hoy}.md")

# ─── Extractor ────────────────────────────────────────────────────────────────
def extraer_datos():
    if not os.path.exists(archivo_hoy):
        print("No se encontró la nota de hoy.")
        return []

    with open(archivo_hoy, "r", encoding="utf-8") as f:
        contenido = f.read()

    pattern = r"\d+\.\s*\[([^\]]+)\]\s*\n\s*context:\s*(.+)"
    matches = re.findall(pattern, contenido, re.IGNORECASE)

    if not matches:
        print("No se encontraron palabras en la nota de hoy.")
    else:
        print(f"Palabras encontradas: {[m[0] for m in matches]}")

    return matches

# ─── Main ──────────────────────────────────────────────────────────────────────
datos = extraer_datos()

if datos:
    crear_modelo_si_no_existe()

    for palabra, contexto in datos:
        print(f"\nProcesando: {palabra}")

        tarjeta = generar_tarjeta(palabra, contexto)
        print(f"  Respuesta IA: {tarjeta}")

        partes = [p.strip() for p in tarjeta.strip().split('|')]

        if len(partes) < 6:
            print(f"  Formato inesperado ({len(partes)} campos), saltando '{palabra}'.")
            continue

        palabra_raw   = partes[0]
        pronunciacion = partes[1]
        traduccion    = partes[2]
        ejemplo       = partes[3]
        ejemplo_trad  = partes[4]
        usar_imagen   = partes[5].strip().upper() == "SI"

        print(f"  Imagen: {'sí' if usar_imagen else 'no'}")

        añadir_a_anki(palabra_raw, pronunciacion, traduccion, ejemplo, ejemplo_trad, usar_imagen="SI")