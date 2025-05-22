# TUI ToDo - Sistema Avanzado de Gestión de Tareas en Terminal

TUI ToDo es un sistema avanzado de gestión de tareas y organización personal que funciona completamente en la terminal. Basado en la biblioteca Textual para Python, proporciona una experiencia de usuario rica y potente sin necesidad de una interfaz gráfica tradicional.

## Características

### Gestión de Tareas Avanzada
- **Estados múltiples de tareas**: Soporte para diversos estados como pendiente, completado, diferido, importante, cancelado y parcial.
- **Organización jerárquica**: Sistema de navegación en árbol para organizar tareas por proyectos, áreas de vida y categorías.
- **Calendario integrado**: Visualización de tareas en un calendario para planificación temporal.

### Interfaz Optimizada
- **Diseño TUI moderno**: Interfaz de terminal limpia y atractiva con paneles, encabezados y pies de página.
- **Navegación eficiente**: Sistema completo de atajos de teclado para una gestión rápida sin necesidad de ratón.
- **Estilos personalizables**: Apariencia totalmente personalizable mediante CSS de Textual (TCSS).

### Productividad
- **Contenido dinámico**: Visualización adaptada al contexto según la selección en el árbol de navegación.
- **Sistema de notas integrado**: Capacidad para adjuntar notas detalladas a las tareas y proyectos.
- **Visualización de alertas**: Destacado visual de tareas importantes o próximas a vencer.

## Requisitos

- Python 3.7+
- Textual
- Rich

## Instalación

1. Clona este repositorio o descarga los archivos.
2. Crea un entorno virtual (recomendado):
   ```bash
   python -m venv env
   ```
3. Activa el entorno virtual:
   - En Windows:
     ```bash
     env\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source env/bin/activate
     ```
4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Para ejecutar la aplicación, utiliza uno de los siguientes comandos:

```bash
python terminal_app_textual.py
```

o

```bash
python TUI.py
```

### Atajos de teclado

- `q`: Salir de la aplicación
- `Ctrl+t`: Alternar el estado del checkbox "Theme Test"

### Navegación

- Utiliza las teclas de flecha para navegar por el árbol
- Presiona `Enter` para seleccionar un elemento del árbol
- El contenido principal se actualizará según la selección

## Estructura del proyecto

### Archivos actuales
- `terminal_app_textual.py`: Archivo principal de la aplicación
- `TUI.py`: Versión alternativa de la aplicación
- `textual_terminal_tui.tcss`: Archivo de estilos CSS para Textual
- `requirements.txt`: Lista de dependencias del proyecto

### Estructura planificada (con backend)
- `models/`: Módulos para la gestión de datos
  - `task.py`: Modelo de tareas
  - `project.py`: Modelo de proyectos/categorías
  - `tag.py`: Sistema de etiquetas
- `storage/`: Módulos para persistencia de datos
  - `database.py`: Gestión de base de datos SQLite
  - `file_storage.py`: Almacenamiento basado en archivos
  - `sync.py`: Sincronización con servicios externos
- `views/`: Componentes de la interfaz de usuario
  - `task_list.py`: Vista de lista de tareas
  - `task_detail.py`: Vista detallada de tareas
  - `calendar_view.py`: Vista de calendario mejorada
- `controllers/`: Lógica de negocio
  - `task_controller.py`: Gestión de tareas
  - `filter_controller.py`: Filtrado y búsqueda
  - `reminder_controller.py`: Sistema de recordatorios

## Personalización

### Modificar el estilo

Para modificar el estilo de la aplicación, edita el archivo `textual_terminal_tui.tcss`. Este archivo utiliza la sintaxis de CSS de Textual, que es similar al CSS estándar pero con algunas características específicas para interfaces de terminal.

### Agregar nuevas funcionalidades

Para agregar nuevas funcionalidades, puedes:

1. Crear nuevos widgets heredando de las clases base de Textual
2. Modificar los widgets existentes
3. Agregar nuevos atajos de teclado en la lista `BINDINGS`

### Personalizar estados de tareas

El sistema soporta los siguientes estados de tareas que puedes personalizar o extender:

- `[ ]` Pendiente
- `[x]` Completado
- `[>]` Diferido
- `[!]` Importante
- `[?]` Pregunta/Duda
- `[i]` Información
- `[-]` Cancelado
- `[p]` Parcialmente completado

## Solución de problemas

### La aplicación no inicia

- Verifica que todas las dependencias estén instaladas correctamente
- Asegúrate de que el archivo CSS tenga la extensión `.tcss`
- Comprueba que no haya errores de sintaxis en el código

### Problemas de visualización

- Asegúrate de que tu terminal soporte colores y caracteres Unicode
- Ajusta el tamaño de la ventana de la terminal si los elementos se ven desplazados

## Contribución

Las contribuciones son bienvenidas. Por favor, siente libre de:

1. Reportar errores
2. Sugerir mejoras
3. Enviar pull requests

## Licencia

Este proyecto está licenciado bajo la licencia MIT.
