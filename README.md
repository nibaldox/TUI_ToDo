# TUI ToDo - Sistema Avanzado de Gestión de Tareas en Terminal

TUI ToDo es un sistema avanzado de gestión de tareas y organización personal que funciona completamente en la terminal. Basado en la biblioteca Textual para Python, proporciona una experiencia de usuario rica y potente sin necesidad de una interfaz gráfica tradicional.

## Características

### Gestión de Tareas Avanzada

- **Estados múltiples de tareas**: Soporte para diversos estados como pendiente, completado, diferido, importante, cancelado y parcial.
- **Organización jerárquica**: Sistema de navegación en árbol para organizar tareas por proyectos, áreas de vida y categorías.
- **Calendario integrado**: Visualización de tareas en un calendario para planificación temporal.
- **Resaltado de feriados**: Los días feriados nacionales de Chile se muestran en rojo.

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
- caldav>=1.0.0
- holidays>=0.25.0
- icalendar>=4.0.0

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

5. Configura las variables de entorno para CalDAV:

   ```bash
   export CALDAV_URL=<url>
   export CALDAV_USER=<user>
   export CALDAV_PASS=<pass>
   ```

## Uso

Para ejecutar la aplicación, utiliza:

```bash
python TUI.py
```

- Presiona `s` para sincronizar eventos CalDAV (unidireccional).
- Presiona `b` para sincronización bidireccional CalDAV.

### Inicialización de la base de datos

Antes de usar la aplicación, ejecuta:

```bash
python initialize_db.py
```

### Ejecutar pruebas

```bash
python -m unittest discover -s tui_todo/tests/backend
```

### Atajos de teclado

- `q`: Salir de la aplicación
- `Ctrl+t`: Alternar el checkbox "Theme Test"
- `n`: Nueva tarea (abre formulario)
- `e`: Editar tarea seleccionada
- `d`: Eliminar tarea seleccionada (abre confirmación)
- `s`: Sincronizar eventos CalDAV
- `b`: Sincronización bidireccional CalDAV
- `Flechas ← →`: Navegar meses en calendario
- `Enter`: Seleccionar elemento en la navegación

## Estructura del proyecto

```bash
├── .gitignore
├── README.md
├── initialize_db.py      # Script de inicialización de base de datos
├── plan_implementacion.md
├── requirements.txt
├── TUI.py                # Ejecutable principal de la aplicación TUI
├── tui_todo
│   ├── backend
│   │   ├── adapters
│   │   │   ├── database
│   │   │   │   └── database_service.py
│   │   │   └── repositories
│   │   │       ├── sqlite_task_repository.py
│   │   │       ├── sqlite_project_repository.py
│   │   │       └── sqlite_tag_repository.py
│   │   ├── core
│   │   │   ├── entities
│   │   │   ├── interfaces
│   │   │   └── use_cases
│   │   └── frameworks
│   └── tests
│       └── backend
│           ├── test_entities.py
│           └── test_repositories.py
└── tui_todo_data         # Ignorada por .gitignore, almacena la base de datos SQLite
```

## Clean Architecture

El proyecto sigue principios de Clean Architecture, separando:

- Entidades (`core/entities`)
- Casos de uso (`core/use_cases`)
- Adaptadores de persistencia (`adapters/repositories`)
- Lógica de presentación y scripts

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
