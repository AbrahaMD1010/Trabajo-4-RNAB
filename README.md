# Generador de Historias con IA

Un generador de historias inteligente que utiliza Google Gemini para crear historias únicas y cautivadoras basadas en las preferencias del usuario.

##  Características

###  Funcionalidades Principales
- **Generación de Historias**: Crea historias de 300-800 palabras con IA
- **Entrada Flexible**: Formulario estructurado o descripción libre
- **Múltiples Géneros**: Fantasía, misterio, romance, terror, ciencia ficción, comedia, aventura, drama
- **Control de Tono**: Humorístico, oscuro, caprichoso, dramático, satírico, serio
- **Interfaz Web Moderna**: Diseño responsive y fácil de usar
- **Memoria de Conversación**: Mantiene contexto entre generaciones

###  Elementos de la Historia
- **Personajes**: Nombres, roles, rasgos de personalidad, relaciones
- **Escenario**: Período de tiempo, ubicación, atmósfera
- **Género**: 8 géneros literarios disponibles
- **Elementos de Trama**: Tipo de conflicto, obstáculos, estilo de resolución
- **Tono**: 6 tonos narrativos diferentes
- **Extensión**: Corta (300-400), mediana (400-600), larga (600-800 palabras)

##  Instalación

### Prerrequisitos
- Python 3.8 o superior
- API Key de Google Gemini

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd Trabajo-4-RNAB-main
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar API Key**
   - Ve a [Google AI Studio](https://aistudio.google.com/)
   - Crea una nueva API key
   - Crea un archivo `.env` en la raíz del proyecto:
   ```
   GOOGLE_API_KEY=tu_api_key_aqui
   ```

4. **Ejecutar la aplicación**
   ```bash
   python main.py
   ```

5. **Abrir en el navegador**
   - Ve a `http://localhost:8000`
   - ¡Disfruta generando historias!

##  Uso

### Interfaz Web

1. **Formulario Estructurado**
   - Selecciona género y tono
   - Describe personajes, escenario y conflicto
   - Elige la extensión deseada

2. **Descripción Libre**
   - Escribe una descripción natural de la historia
   - Mínimo 20 caracteres
   - Incluye palabras clave narrativas

3. **Generar Historia**
   - Haz clic en "Generar Historia"
   - Espera a que la IA procese tu solicitud
   - Lee tu historia única

4. **Funciones Adicionales**
   - **Regenerar**: Crea una nueva versión con los mismos parámetros
   - **Copiar**: Copia la historia al portapapeles
   - **Reiniciar**: Limpia el formulario

### API REST

También puedes usar la API directamente:

```bash
curl -X POST "http://localhost:8000/ia" \
  -H "Content-Type: application/json" \
  -d '{
    "genero": "fantasía",
    "personajes": "Un mago joven y su aprendiz",
    "escenario": "Una torre mágica en las montañas",
    "tono": "dramático",
    "extension": "mediana (400-600 palabras)",
    "conflicto": "El aprendiz debe salvar al mago de una maldición"
  }'
```

##  Arquitectura

### Módulos Principales

1. **`main.py`**: Servidor FastAPI y endpoints
2. **`history_ai.py`**: Clase principal de IA con LangChain
3. **`entrada_processor.py`**: Procesamiento y validación de entradas
4. **`templates/index.html`**: Interfaz web principal
5. **`static/style.css`**: Estilos CSS
6. **`static/script.js`**: Funcionalidad JavaScript

### Flujo de Datos

1. **Entrada del Usuario** → `entrada_processor.py`
2. **Validación y Procesamiento** → Prompt estructurado
3. **Generación con IA** → `history_ai.py` (Google Gemini)
4. **Respuesta JSON** → Interfaz web
5. **Visualización** → HTML/CSS/JavaScript

##  Características de la Interfaz

- **Diseño Responsive**: Funciona en móviles y escritorio
- **Animaciones Suaves**: Transiciones y efectos visuales
- **Validación en Tiempo Real**: Feedback inmediato al usuario
- **Alertas Inteligentes**: Mensajes informativos y de error
- **Tema Oscuro**: Interfaz moderna con gradientes azules

##  Configuración Avanzada

### Variables de Entorno
```bash
GOOGLE_API_KEY=tu_api_key_aqui
```

### Personalización del Modelo
En `history_ai.py` puedes modificar:
- **Modelo**: `gemini-1.5-pro` o `gemini-2.0-flash`
- **Temperatura**: Controla la creatividad (0.0-1.0)
- **Prompt**: Instrucciones para la generación

### Estilos Personalizados
Modifica `static/style.css` para cambiar:
- Colores y gradientes
- Tipografías
- Animaciones
- Layout responsive

##  Solución de Problemas

### Error de API Key
```
Error: Invalid API key
```
- Verifica que el archivo `.env` existe
- Confirma que la API key es válida
- Revisa que no hay espacios extra

### Error de Conexión
```
Error de conexión. Verifica que el servidor esté ejecutándose.
```
- Asegúrate de que `python main.py` esté ejecutándose
- Verifica que el puerto 8000 esté disponible
- Revisa el firewall

### Error de Validación
```
La descripción no contiene palabras clave narrativas
```
- Incluye palabras como: historia, personaje, escenario, conflicto
- Asegúrate de tener al menos 20 caracteres
- Usa el formulario estructurado como alternativa

##  Ejemplos de Uso

### Historia de Fantasía
```
Género: Fantasía
Personajes: Un dragón anciano y un niño huérfano
Escenario: Una cueva mágica en las montañas nevadas
Tono: Dramático
Conflicto: El niño debe convencer al dragón de ayudarle a salvar su aldea
```

### Historia de Misterio
```
Género: Misterio
Personajes: Una detective privada y su asistente
Escenario: Una mansión victoriana en la noche
Tono: Oscuro
Conflicto: Investigar la desaparición de un valioso diamante
```

##  Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

##  Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

##  Agradecimientos

- **Google Gemini**: Modelo de IA para generación de historias
- **LangChain**: Framework para aplicaciones de IA
- **FastAPI**: Framework web moderno
- **Bootstrap**: Framework CSS para la interfaz
- **Bootstrap Icons**: Iconografía moderna

---

**¡Disfruta creando historias únicas con IA!**  