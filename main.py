from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from history_ai import history_ai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IARequest(BaseModel):
    message: Optional[str] = None
    reset_memory: Optional[bool] = False

@app.post("/ia")
async def ia_endpoint(request: IARequest):
    """
    Endpoint para el AI experto en historia.
    Recibe un mensaje del usuario y devuelve la respuesta de la IA.
    
    Parámetros esperados en el request:
    - message: El mensaje del usuario
    - reset_memory (opcional): Si es True, reinicia la memoria de la conversación
    
    Retorna:
    - response: La respuesta de la IA
    """
    
    if request.reset_memory:
        history_ai.reset_memory()
        return {"message": "Memoria de conversación reiniciada"}
    
    if not request.message:
        raise HTTPException(
            status_code=400,
            detail="Se requiere un mensaje para la IA"
        )
    
    try:
        response = history_ai.process_message(request.message)
        print(f"Mensaje procesado: {response}")
        return {"response": response}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el mensaje: {str(e)}"
        )

