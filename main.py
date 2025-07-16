from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
from history_ai import history_ai
from entrada_processor import process_user_input
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar archivos estáticos y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class IARequest(BaseModel):
    message: Optional[str] = None
    reset_memory: Optional[bool] = False
    # Campos estructurados para el procesador de entrada
    genero: Optional[str] = None
    personajes: Optional[str] = None
    escenario: Optional[str] = None
    tono: Optional[str] = None
    extension: Optional[str] = None
    conflicto: Optional[str] = None
    descripcion: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal con la interfaz de usuario"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ia")
async def ia_endpoint(request: IARequest):
    """
    Endpoint para el AI experto en historia.
    Recibe un mensaje del usuario y devuelve la respuesta de la IA.
    
    Parámetros esperados en el request:
    - message: El mensaje del usuario (texto libre)
    - reset_memory (opcional): Si es True, reinicia la memoria de la conversación
    - Campos estructurados: genero, personajes, escenario, tono, extension, conflicto, descripcion
    
    Retorna:
    - response: La respuesta de la IA
    - warnings: Lista de advertencias del procesador
    """
    
    if request.reset_memory:
        history_ai.reset_memory()
        return {"message": "Memoria de conversación reiniciada"}
    
    # Preparar datos para el procesador de entrada
    input_data = {
        "genero": request.genero,
        "personajes": request.personajes,
        "escenario": request.escenario,
        "tono": request.tono,
        "extension": request.extension,
        "conflicto": request.conflicto,
        "descripcion": request.descripcion or request.message
    }
    
    # Procesar entrada usando el módulo de procesamiento
    try:
        processed_input, warnings = process_user_input(input_data)
        
        # Generar historia con la IA
        response = history_ai.process_message(processed_input)
        
        return {
            "response": response,
            "warnings": warnings,
            "processed_input": processed_input
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el mensaje: {str(e)}"
        )

