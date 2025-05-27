# Gallery-DL GUI

Una interfaz gráfica de usuario (GUI) para la herramienta de línea de comandos `gallery-dl`.

## Descripción

Esta GUI facilita el uso de `gallery-dl` proporcionando una interfaz visual intuitiva para:
- Ingresar URLs de galerías/imágenes
- Configurar opciones de descarga comunes
- Ver el progreso y logs en tiempo real
- Gestionar autenticación y opciones avanzadas

## Requisitos

- Python 3.6 o superior
- tkinter (incluido con Python en la mayoría de instalaciones)
- gallery-dl instalado y accesible

## Instalación de gallery-dl

Si aún no tienes `gallery-dl` instalado:

```bash
pip install gallery-dl
```

O desde el código fuente:
```bash
git clone https://github.com/mikf/gallery-dl.git
cd gallery-dl
python -m pip install .
```

## Uso

1. **Ejecutar la GUI:**
   ```bash
   python gallery_dl_gui.py
   ```

2. **Configurar la descarga:**
   - **URL(s):** Ingresa una o más URLs separadas por espacios
   - **Directorio de Salida:** Selecciona dónde guardar los archivos descargados

3. **Configurar opciones (pestañas):**

   ### Opciones Comunes
   - **Sobrescribir archivos existentes:** Fuerza la re-descarga de archivos ya existentes
   - **Modo Detallado:** Muestra información detallada durante la descarga
   - **Formato de Nombre:** Personaliza cómo se nombran los archivos descargados
   - **Rango de descarga:** Especifica qué elementos descargar (ej: "1-5, 8, 10-")
   - **Filtro de descarga:** Expresión Python para filtrar archivos (ej: "image_width >= 1000")

   ### Metadatos y Archivos
   - **Escribir metadatos:** Guarda información adicional en archivos .json
   - **Escribir info.json:** Crea un archivo de información de la galería/álbum
   - **Escribir tags:** Guarda etiquetas en archivos .txt
   - **Comprimir en ZIP:** Empaqueta las descargas en un archivo ZIP

   ### Avanzado / Autenticación
   - **Usuario/Contraseña:** Credenciales para sitios que requieren login
   - **Límite de velocidad:** Controla la velocidad de descarga (ej: "500k", "2.5M")
   - **Archivo de historial:** Evita re-descargar archivos ya procesados
   - **Opciones Adicionales:** Flags adicionales de gallery-dl no cubiertos por la GUI

4. **Iniciar descarga:**
   - Haz clic en "Descargar"
   - Observa el progreso en el área de log
   - El botón "Descargar" se deshabilitará y aparecerá el botón "Detener"

5. **Controlar la descarga:**
   - **Detener:** Haz clic en "Detener" para cancelar la descarga en progreso
   - La descarga se detendrá de forma segura y se mostrará un mensaje de cancelación
   - Los botones volverán a su estado inicial

## Detección Automática de gallery-dl

La GUI intenta encontrar `gallery-dl` automáticamente en este orden:

1. **Entorno empaquetado:** Busca `gallery-dl.exe` (Windows) o `gallery-dl` (Linux/macOS) junto al ejecutable de la GUI
2. **PATH del sistema:** Intenta ejecutar `gallery-dl --version`
3. **Módulo Python:** Intenta ejecutar `python -m gallery_dl --version`
4. **Script local:** Si la GUI está en la raíz del proyecto gallery-dl, usa el script local
5. **Fallback:** Asume que `gallery-dl` está disponible en el sistema

## Ejemplos de Uso

### Descarga básica
- URL: `https://example.com/gallery/123`
- Directorio: `C:\Downloads\Gallery`
- Opciones: Solo "Modo Detallado" marcado

### Descarga con filtros
- URL: `https://example.com/user/artist`
- Filtro: `image_width >= 1920 and image_height >= 1080`
- Rango: `1-20`

### Descarga con autenticación
- URL: `https://example.com/private/gallery`
- Usuario: `mi_usuario`
- Contraseña: `mi_contraseña`
- Escribir metadatos: ✓

## Características Técnicas

- **Threading:** Las descargas se ejecutan en hilos separados para mantener la GUI responsiva
- **Logs en tiempo real:** La salida de gallery-dl se muestra inmediatamente
- **Control de descarga:** Botón "Detener" para cancelar descargas en progreso de forma segura
- **Validación:** Verifica que se haya ingresado al menos una URL antes de iniciar
- **Manejo de errores:** Captura y muestra errores de ejecución
- **Cancelación segura:** Permite cerrar la aplicación durante una descarga activa

## Solución de Problemas

### "gallery-dl no encontrado"
- Asegúrate de que gallery-dl esté instalado: `pip install gallery-dl`
- Verifica que esté en el PATH: `gallery-dl --version`
- Si usas un entorno virtual, actívalo antes de ejecutar la GUI

### "Error al construir el comando"
- Revisa las opciones adicionales por sintaxis incorrecta
- Verifica que los filtros usen sintaxis Python válida

### La GUI no responde
- Las descargas largas pueden hacer que parezca que la GUI no responde
- El área de log debería mostrar progreso continuo
- Usa Ctrl+C en la terminal si necesitas forzar el cierre

## Limitaciones

- No todas las opciones de gallery-dl están disponibles en la GUI
- Las opciones muy específicas deben usarse en el campo "Opciones Adicionales"
- La GUI está optimizada para casos de uso comunes

## Contribuciones

Para reportar bugs o sugerir mejoras, por favor crea un issue en el repositorio del proyecto. 