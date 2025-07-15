import re
from fastapi import HTTPException
from typing import Tuple, List, Dict

# Módulo de Procesamiento de Entradas
# Maneja entradas estructuradas, libre y mixtas para generar un prompt coherente

# Conjunto de palabras clave narrativas para validar texto libre
NARRATIVE_KEYWORDS = {
    "historia", "personaje", "escenario", "conflicto",
    "aventura", "drama", "cuento", "relato"
}

# Campos estructurados permitidos
STRUCTURED_FIELDS = {
    "genero", "personajes", "escenario",
    "tono", "extension", "conflicto"
}

def process_user_input(data: Dict[str, any]) -> Tuple[str, List[str]]:
    """
    Valida y transforma la entrada del usuario en un texto plano para el modelo generador.

    Retorna:
    - user_input: Prompt limpio y unificado.
    - warnings: Lista de sugerencias o advertencias.
    """
    has_structured = any(
        field in data and data.get(field)
        for field in STRUCTURED_FIELDS
    )
    free_text = (data.get("descripcion") or data.get("texto") or "").strip()
    has_free_text = bool(free_text)

    if has_structured and not has_free_text:
        input_type = "estructurada"
    elif has_free_text and not has_structured:
        input_type = "natural"
    elif has_structured and has_free_text:
        input_type = "mixta"
    else:
        raise HTTPException(
            status_code=400,
            detail="Falta información para generar la historia."
        )

    warnings: List[str] = []

    if input_type in ("estructurada", "mixta"):
        if not (data.get("genero") or data.get("tono")):
            warnings.append("Especifique un género o un tono para orientar la historia.")
        if not (
            data.get("personajes") or data.get("escenario") or data.get("conflicto")
        ):
            warnings.append("Incluya al menos personajes, escenario o conflicto.")

        parts: List[str] = []
        if data.get("genero"):
            parts.append(f"La historia debe pertenecer al género {data['genero']}.")
        if data.get("tono"):
            parts.append(f"Debe tener un tono {data['tono']}.")
        if data.get("personajes"):
            parts.append(f"Incluye los siguientes personajes: {data['personajes']}.")
        if data.get("escenario"):
            parts.append(f"El escenario principal es: {data['escenario']}.")
        if data.get("conflicto"):
            parts.append(f"El conflicto central es: {data['conflicto']}.")
        if data.get("extension"):
            parts.append(f"La historia debe tener una extensión aproximada de {data['extension']}.")
        if has_free_text:
            parts.append(f"Descripción adicional: {free_text}")

        user_input = " ".join(parts)

    else:
        text = free_text
        if len(text) < 20:
            raise HTTPException(
                status_code=400,
                detail="La descripción libre debe tener al menos 20 caracteres."
            )
        if not any(
            re.search(r"\b" + kw + r"\b", text, re.IGNORECASE)
            for kw in NARRATIVE_KEYWORDS
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    "La descripción no contiene palabras clave narrativas "
                    "(e.g., personajes, escenario, conflicto)."
                )
            )
        user_input = text

    return user_input, warnings
