document.addEventListener('DOMContentLoaded', function() {
    const storyForm = document.getElementById('storyForm');
    const resultContainer = document.getElementById('resultContainer');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const alertsContainer = document.getElementById('alertsContainer');
    const resetBtn = document.getElementById('resetBtn');
    const copyBtn = document.getElementById('copyBtn');
    const regenerateBtn = document.getElementById('regenerateBtn');

    // Variables para almacenar el último resultado
    let lastStoryData = null;
    let lastFormData = null;
    let isFirstGeneration = true; // Variable para trackear si es la primera generación

    // Manejar envío del formulario
    storyForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Obtener datos del formulario
        const formData = new FormData(storyForm);
        const data = Object.fromEntries(formData.entries());
        
        // Validar que al menos hay algún dato
        const hasStructuredData = data.genero || data.personajes || data.escenario || data.tono || data.extension || data.conflicto || data.publico_objetivo;
        const hasNaturalData = data.descripcion && data.descripcion.trim().length >= 20;
        const hasInteractiveData = data.historia_interactiva && data.historia_interactiva.trim().length >= 20;
        
        if (!hasStructuredData && !hasNaturalData && !hasInteractiveData) {
            showAlert('Por favor, completa al menos algunos campos del formulario o escribe una descripción libre/interactiva (mínimo 20 caracteres).', 'warning');
            return;
        }

        // Guardar datos para regeneración
        lastFormData = data;
        
        // Mostrar loading
        showLoading(true);
        hideResult();
        clearAlerts();

        try {
            const response = await fetch('/ia', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                displayStory(result);
                showAlert('¡Historia generada exitosamente!', 'success');
            } else {
                showAlert(`Error: ${result.detail || 'Error desconocido'}`, 'danger');
            }
        } catch (error) {
            console.error('Error:', error);
            showAlert('Error de conexión. Verifica que el servidor esté ejecutándose.', 'danger');
        } finally {
            showLoading(false);
        }
    });

    // Función para mostrar la historia
    function displayStory(result) {
        try {
            // Intentar parsear la respuesta como JSON
            let storyData;
            try {
                // Limpiar la respuesta de la IA
                const cleanResponse = result.response.replace(/```json\n?|\n?```/g, '').trim();
                storyData = JSON.parse(cleanResponse);
            } catch (e) {
                // Si no es JSON válido, mostrar como texto plano
                storyData = {
                    titulo: 'Historia Generada',
                    historia: result.response,
                    moraleja: null,
                    conclusion: null
                };
            }

            // Guardar datos para regeneración
            lastStoryData = storyData;

            // Mostrar título
            const titleElement = document.getElementById('storyTitle');
            titleElement.textContent = storyData.titulo || 'Historia Generada';
            titleElement.style.fontSize = '1.3rem';
            titleElement.style.fontWeight = '700';
            titleElement.style.color = '#fff';

            // Mostrar contenido
            const contentElement = document.getElementById('storyContent');
            contentElement.innerHTML = storyData.historia || result.response;
            contentElement.style.textAlign = 'left';
            contentElement.style.whiteSpace = 'pre-line';

            // Mostrar moraleja si existe
            const moralejaElement = document.getElementById('storyMoraleja');
            if (storyData.moraleja) {
                moralejaElement.innerHTML = `<strong>Moraleja:</strong> ${storyData.moraleja}`;
                moralejaElement.style.display = 'block';
            } else {
                moralejaElement.style.display = 'none';
            }

            // Mostrar advertencias si existen
            if (result.warnings && result.warnings.length > 0) {
                result.warnings.forEach(warning => {
                    showAlert(warning, 'info');
                });
            }

            // Mostrar resultado
            resultContainer.style.display = 'block';
            resultContainer.scrollIntoView({ behavior: 'smooth' });

            // *** AGREGAR ESTA LÍNEA ***
            // Actualizar placeholders después de la primera generación exitosa
            updatePlaceholdersAfterGeneration();

        } catch (error) {
            console.error('Error al procesar la historia:', error);
            showAlert('Error al procesar la respuesta de la IA.', 'danger');
        }
    }

    // Función para regenerar historia
    regenerateBtn.addEventListener('click', async function() {
        if (!lastFormData) {
            showAlert('No hay datos previos para regenerar. Completa el formulario primero.', 'warning');
            return;
        }

        showLoading(true);
        hideResult();
        clearAlerts();

        try {
            const response = await fetch('/ia', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(lastFormData)
            });

            const result = await response.json();

            if (response.ok) {
                displayStory(result);
                showAlert('¡Historia regenerada exitosamente!', 'success');
                updatePlaceholdersAfterGeneration();
            } else {
                showAlert(`Error: ${result.detail || 'Error desconocido'}`, 'danger');
            }
        } catch (error) {
            console.error('Error:', error);
            showAlert('Error de conexión al regenerar la historia.', 'danger');
        } finally {
            showLoading(false);
        }
    });

    // Función para copiar historia
    copyBtn.addEventListener('click', function() {
        if (!lastStoryData) {
            showAlert('No hay historia para copiar.', 'warning');
            return;
        }

        const textToCopy = `${lastStoryData.titulo}\n\n${lastStoryData.historia}${lastStoryData.moraleja ? '\n\nMoraleja: ' + lastStoryData.moraleja : ''}`;
        
        navigator.clipboard.writeText(textToCopy).then(function() {
            showAlert('Historia copiada al portapapeles.', 'success');
        }).catch(function() {
            showAlert('Error al copiar la historia.', 'danger');
        });
    });

    // Función para reiniciar formulario
    resetBtn.addEventListener('click', function() {
        storyForm.reset();
        hideResult();
        clearAlerts();
        lastStoryData = null;
        lastFormData = null;
        
        // Restaurar placeholders originales
        const descripcionField = document.getElementById('descripcion');
        if (descripcionField) {
            descripcionField.placeholder = "Describe libremente la historia que quieres que genere la IA. Incluye detalles sobre personajes, escenario, género, tono, conflicto, etc. Mínimo 20 caracteres.";
        }
        
        const historiaInteractivaField = document.getElementById('historia_interactiva');
        if (historiaInteractivaField) {
            historiaInteractivaField.placeholder = "Describe la historia interactiva que quieres que genere la IA. La IA creará una historia con puntos de decisión donde tú puedes elegir el rumbo. Incluye detalles sobre personajes, escenario, género, tono, conflicto, etc. Mínimo 20 caracteres.";
        }
        
        // Resetear bandera
        isFirstGeneration = true;
        
        showAlert('<i class="bi bi-info-circle me-2"></i>Formulario reiniciado', 'info');
    });

    // Funciones auxiliares
    function showLoading(show) {
        loadingSpinner.style.display = show ? 'block' : 'none';
        document.getElementById('generateBtn').disabled = show;
        document.getElementById('regenerateBtn').disabled = show;
    }

    function hideResult() {
        resultContainer.style.display = 'none';
    }

    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        alertsContainer.appendChild(alertDiv);

        // Auto-remover después de 8 segundos para la alerta de memoria
        const duration = message.includes('Memoria del LLM') ? 8000 : 5000;
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, duration);
    }

    function clearAlerts() {
        alertsContainer.innerHTML = '';
    }

    // Validación en tiempo real para descripción libre
    const descripcionField = document.getElementById('descripcion');
    if (descripcionField) {
        descripcionField.addEventListener('input', function() {
            const length = this.value.trim().length;
            const minLength = 20;
            
            if (length > 0 && length < minLength) {
                this.setCustomValidity(`Mínimo ${minLength} caracteres (actual: ${length})`);
            } else {
                this.setCustomValidity('');
            }
        });
    }

    // Validación en tiempo real para historia interactiva
    const historiaInteractivaField = document.getElementById('historia_interactiva');
    if (historiaInteractivaField) {
        historiaInteractivaField.addEventListener('input', function() {
            const length = this.value.trim().length;
            const minLength = 20;
            
            if (length > 0 && length < minLength) {
                this.setCustomValidity(`Mínimo ${minLength} caracteres (actual: ${length})`);
            } else {
                this.setCustomValidity('');
            }
        });
    }

    // Cambio de pestañas
    const tabButtons = document.querySelectorAll('[data-bs-toggle="tab"]');
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Limpiar validaciones al cambiar de pestaña
            clearAlerts();
        });
    });

    // Tooltips para campos
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Función para resetear la memoria del LLM
    async function resetMemory() {
        try {
            const resetMemoryBtn = document.getElementById('resetMemoryBtn');
            resetMemoryBtn.disabled = true;
            resetMemoryBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Limpiando...';
            
            const response = await fetch('/ia', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    reset_memory: true
                })
            });

            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }

            const data = await response.json();
            
            // Verificar si la operación fue exitosa
            if (data.success || data.message) {
                showAlert('✅ Memoria del LLM limpiada exitosamente. Las siguientes historias no tendrán contexto previo.', 'success');
                
                // Restaurar placeholders originales al limpiar memoria
                const descripcionField = document.getElementById('descripcion');
                if (descripcionField) {
                    descripcionField.placeholder = "Describe libremente la historia que quieres que genere la IA. Incluye detalles sobre personajes, escenario, género, tono, conflicto, etc. Mínimo 20 caracteres.";
                }
                
                const historiaInteractivaField = document.getElementById('historia_interactiva');
                if (historiaInteractivaField) {
                    historiaInteractivaField.placeholder = "Describe la historia interactiva que quieres que genere la IA. La IA creará una historia con puntos de decisión donde tú puedes elegir el rumbo. Incluye detalles sobre personajes, escenario, género, tono, conflicto, etc. Mínimo 20 caracteres.";
                }
                
                // Resetear bandera
                isFirstGeneration = true;
                
            } else {
                throw new Error('Respuesta inesperada del servidor');
            }
            
        } catch (error) {
            console.error('Error al resetear memoria:', error);
            showAlert('❌ Error al limpiar la memoria. Intenta nuevamente.', 'danger');
        } finally {
            const resetMemoryBtn = document.getElementById('resetMemoryBtn');
            resetMemoryBtn.disabled = false;
            resetMemoryBtn.innerHTML = '<i class="bi bi-trash me-2"></i>Limpiar Memoria';
        }
    }

    // Agregar event listener para el botón de limpiar memoria
    const resetMemoryBtn = document.getElementById('resetMemoryBtn');
    if (resetMemoryBtn) {
        resetMemoryBtn.addEventListener('click', resetMemory);
    }

    // Función para actualizar placeholders después de generar una historia
    function updatePlaceholdersAfterGeneration() {
        if (isFirstGeneration) {
            // Cambiar placeholder para descripción libre
            const descripcionField = document.getElementById('descripcion');
            if (descripcionField) {
                descripcionField.placeholder = "Puedes continuar agregando personajes, ideas, conflictos, o modificar completamente cualquier aspecto de la historia.";
            }
            
            // Cambiar placeholder para historia interactiva
            const historiaInteractivaField = document.getElementById('historia_interactiva');
            if (historiaInteractivaField) {
                historiaInteractivaField.placeholder = "Debes elegir cual decisión quieres tomar para darle rumbo a tu historia";
            }
            
            isFirstGeneration = false;
        }
    }

    // Función para generar imagen a partir de la historia
    const generateImageBtn = document.getElementById('generateImageBtn');
    if (generateImageBtn) {
        generateImageBtn.addEventListener('click', async function() {
            if (!lastStoryData || !lastStoryData.historia) {
                showAlert('Primero genera una historia antes de crear la imagen.', 'warning');
                return;
            }

            // Usar el título y la historia como prompt
            const prompt = `${lastStoryData.titulo || ''}. ${lastStoryData.historia}`;

            generateImageBtn.disabled = true;
            generateImageBtn.innerHTML = '<i class="bi bi-hourglass-split me-1"></i>Generando...';

            showAlert('Generando imagen, esto puede tardar unos segundos...', 'info');

            try {
                const response = await fetch('/generate-image', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt })
                });
                const data = await response.json();

                if (data.success) {
                    // Mostrar la imagen
                    const imageContainer = document.getElementById('imageContainer');
                    const generatedImage = document.getElementById('generatedImage');
                    generatedImage.src = `data:image/png;base64,${data.image_base64}`;
                    imageContainer.style.display = 'block';
                    showAlert('¡Imagen generada exitosamente!', 'success');
                    imageContainer.scrollIntoView({ behavior: 'smooth' });
                } else {
                    showAlert('No se pudo generar la imagen.', 'danger');
                }
            } catch (error) {
                showAlert('Error al generar la imagen.', 'danger');
            } finally {
                generateImageBtn.disabled = false;
                generateImageBtn.innerHTML = '<i class="bi bi-image me-1"></i>Generar Imagen';
            }
        });
    }
});