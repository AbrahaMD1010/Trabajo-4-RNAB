import re
from fastapi import HTTPException
from typing import Tuple, List, Dict, Any

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
    "tono", "extension", "conflicto", "publico_objetivo"
}

def process_user_input(data: Dict[str, Any]) -> Tuple[str, List[str]]:
    """
    Valida y transforma la entrada del usuario en un texto plano para el modelo generador.

    Retorna:
    - user_input: Prompt limpio y unificado.
    - warnings: Lista de sugerencias o advertencias.
    """
    warnings = []
    
    # Obtener datos
    genero = data.get('genero', '')
    personajes = data.get('personajes', '')
    escenario = data.get('escenario', '')
    tono = data.get('tono', '')
    extension = data.get('extension', '')
    conflicto = data.get('conflicto', '')
    descripcion = data.get('descripcion', '')
    historia_interactiva = data.get('historia_interactiva', '')
    publico_objetivo = data.get('publico_objetivo', '')
    
    # Verificar si hay datos de historia interactiva
    if historia_interactiva:
        # Usar prompt específico para historia interactiva
        prompt = f"""
        Dado que eres un experto en literatura y creación de historias, quiero que crees una historia interactiva en la que debes abrir decisiones para el usuario como por ejemplo, llegas a una bosque con dos caminos, uno esta lleno de ruidos de bestias y en el otro se dice que hay bandidos, estas opciones debes ser puestas al final de la historia separadas por literales alfabeticos como A), B), debes dejar la historia a ese punto y permitir que el usuario tome la decisión, la cual debe ser relevante para la historia, algo muy importante a tener en cuenta es que no debes alargar ls historia de manera innecesaria, y cuando la historia ya llegue a su fin entregame toda la historia completa desde el inicio de la generación. Para crear la historia debes  tener en cuenta las siguientes reglas para crear una buena historia:
                1. Usa el genero que se te indique en los requerimientos, debes ceñirte muy bien a las características de dicho genero para crear la historia, es decir, los cuentos se caracterizan por tener introducción, nudo y desenlace, por lo que debes estructurar la historia de la manera correcta, si el género no es especificado, debes tener en cuenta los demás requerimientos para escoger un género con el fin de crear una historia interesante, puedes tener en cuenta aspectos como ambientación, personajes, sentimiento deseado a transmitir, etc.
                2. Ten presente la extensión que se pide para crear la historia, si esta no es especificada, crea la historia con un rango de 300 a 800 palabras.
                3. Asegúrate de mantener coherencia narrativa y estructural entre los hechos de la historia, conversaciones, personajes y demás.
                4. Debes tener en cuenta los personajes que se piden en la historia, recuerda crearlos con respecto a su personalidad, cualidadades y caracteristicas establecidas desde el inicio, estas no deben cambiar a no ser de que la historia lo requiera, por ejemplo, en caso de que un personaje requiera un desarrollo o un cambio debido a los hechos ocurridos. si  no se especifican los personajes o parte de sus caracteristicas, crea personajes coherentes con los demás aspectos de la historia, adicionalmente asegúrate de crear conversaciones coherentes con la historia, características y personalidades de los personajes.
                5. Con respecto al escenario, comienza a generar la historia a partir del escenario pedido, en caso de no ser pedido usa el escenario que mejor se acomode a la historia.
                6. Ten en cuenta los elementos de la trama pedidos como: Tipo de conflicto, obstáculos, estilo de resolución, ya que esto es importante para que estructures la historia, especialmente con la extensión de esta para que se puedan incluir y desarrollarse todos los elementos de la manera correcta.
                7. Toma en cuenta el tono y el sentimiento que se quiere conseguir con la historia, es decir, si  se pide que la historia tenga tono humorístico, dramático o satírico, debes incluirlo en la historia al igual que el sentimiento que se quiere expresar.
                8. Ten cuenta el publico o audiencia objetivo, ya que esto te ayudara a crear una historia acorde a las expectativas de la audiencia, por ejemplo, si se pide una historia para niños, debes tener en cuenta el lenguaje y los temas que se pueden tratar.
                Solo responde con el título y la historia creada, en caso de que se pida una conclusión o moraleja también puedes darla, solo danos el texto plano sin caracteres extraños como para especificar negritas tipo (** **), dado esto genera un JSON siguiendo la forma descrita abajo. No agregue ningún atributo que no aparezca en el esquema que se muestra a continuación.
                ```python
                {{
                    titulo: string  # Título de la historia
                    historia: string  # Texto de la historia
                }}.
                ```
        
        Descripción de la historia interactiva: {historia_interactiva}
        """
        
        warnings.append("Historia interactiva detectada - se incluirán puntos de decisión")
        return prompt, warnings
    
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
        if data.get("publico_objetivo"):
            parts.append(f"La historia está dirigida a un público {data['publico_objetivo']}.")
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
