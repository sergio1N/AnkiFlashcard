### El Script Final (La "Inyección")
import requests

# Configuración
ANKI_URL = 'http://localhost:8765'

def añadir_a_anki(frente, reverso):
    # Esto asume que tienes un tipo de nota "Básico"
    # Campos: Frente (Palabra+Pronun), Reverso (Significado+Ejemplo+Trad)
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": "Ingles",# maso que exista
                "modelName": "Básico",
                "fields": {
                    "Anverso": frente,  
                    "Reverso": reverso
                },
                "options": {"allowDuplicate": False}
            }
        }
    }
    response = requests.post(ANKI_URL, json=payload)
    return response.json()

# 8. Unicamente y solo si la palabra es un verbo IRREGULAR ,incluye en la [TRADUCCION] su forma en pasado o presente perfecto segun corresponda, Ejemplo:si la palabra es saw entonces en el apartado de traduccion debes incluir: vio (past:see, part: seen)
