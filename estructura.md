# Estructura del Proyecto TUI ToDo

Este documento describe la estructura propuesta para el proyecto TUI ToDo, aplicando principios de Clean Code y separando claramente el frontend del backend.

## Estructura de Directorios

```
tui_todo/
│
├── backend/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   ├── task.py
│   │   │   ├── project.py
│   │   │   └── tag.py
│   │   ├── use_cases/
│   │   │   ├── __init__.py
│   │   │   ├── task_use_cases.py
│   │   │   ├── project_use_cases.py
│   │   │   └── tag_use_cases.py
│   │   └── interfaces/
│   │       ├── __init__.py
│   │       ├── repositories.py
│   │       └── presenters.py
│   │
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── sqlite_repository.py
│   │   │   └── json_repository.py
│   │   └── presenters/
│   │       ├── __init__.py
│   │       └── textual_presenter.py
│   │
│   └── frameworks/
│       ├── __init__.py
│       ├── db/
│       │   ├── __init__.py
│       │   ├── sqlite_db.py
│       │   └── migrations/
│       └── external/
│           ├── __init__.py
│           └── sync_services.py
│
├── frontend/
│   ├── __init__.py
│   ├── app.py                      # Punto de entrada principal
│   ├── styles/
│   │   └── textual_terminal_tui.tcss
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── calendar_widget.py
│   │   ├── task_list_widget.py
│   │   └── sidebar_widget.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── main_view.py
│   │   ├── task_detail_view.py
│   │   └── project_view.py
│   └── controllers/
│       ├── __init__.py
│       ├── task_controller.py
│       └── navigation_controller.py
│
├── tests/
│   ├── backend/
│   │   ├── test_entities.py
│   │   ├── test_use_cases.py
│   │   └── test_repositories.py
│   └── frontend/
│       ├── test_widgets.py
│       └── test_controllers.py
│
├── docs/
│   ├── architecture.md
│   ├── backend.md
│   ├── frontend.md
│   └── user_guide.md
│
├── scripts/
│   ├── setup_db.py
│   └── generate_sample_data.py
│
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py
└── main.py                        # Punto de entrada general
```

## Principios de Clean Code Aplicados

### 1. Arquitectura Limpia (Clean Architecture)

La estructura sigue los principios de la Arquitectura Limpia con capas bien definidas:

- **Core (Núcleo)**: Contiene las entidades de negocio, casos de uso e interfaces independientes de frameworks.
- **Adapters (Adaptadores)**: Implementa las interfaces definidas en el núcleo.
- **Frameworks**: Contiene código específico de frameworks y herramientas externas.

### 2. Separación de Responsabilidades

- **Backend**: Toda la lógica de negocio y persistencia de datos.
- **Frontend**: Interfaz de usuario y presentación.
- **Tests**: Pruebas separadas por componente.

### 3. Principio SOLID

- **S (Responsabilidad Única)**: Cada clase tiene una única responsabilidad.
- **O (Abierto/Cerrado)**: Las entidades están abiertas para extensión pero cerradas para modificación.
- **L (Sustitución de Liskov)**: Las implementaciones de repositorio son intercambiables.
- **I (Segregación de Interfaces)**: Interfaces específicas para cada necesidad.
- **D (Inversión de Dependencias)**: Las dependencias apuntan hacia adentro, hacia el núcleo.

## Plan de Implementación con Metodología Lean

### Fase 1: Estructura Básica y MVP (Mínimo Producto Viable)

1. **Semana 1: Configuración y Entidades Básicas**
   - Crear la estructura de directorios
   - Implementar entidades básicas (Task, Project)
   - Configurar entorno de pruebas
   - Crear repositorio simple basado en JSON

2. **Semana 2: Frontend Mínimo Funcional**
   - Migrar widgets actuales a la nueva estructura
   - Implementar controladores básicos
   - Conectar frontend con repositorio simple
   - Crear primera versión funcional con almacenamiento

### Fase 2: Iteraciones Incrementales

3. **Semana 3: Mejora de Persistencia**
   - Implementar repositorio SQLite
   - Añadir migraciones
   - Implementar caché para mejorar rendimiento
   - Pruebas de integración

4. **Semana 4: Funcionalidades Avanzadas de Tareas**
   - Implementar sistema de etiquetas
   - Añadir filtros y búsqueda
   - Mejorar la vista de calendario
   - Implementar recordatorios

5. **Semana 5: Refinamiento y Optimización**
   - Mejorar la experiencia de usuario
   - Optimizar rendimiento
   - Añadir estadísticas básicas
   - Documentación completa

### Principios Lean Aplicados

1. **Entrega Incremental**:
   - Cada iteración produce una versión funcional
   - Priorización de características por valor

2. **Eliminación de Desperdicios**:
   - Código conciso y enfocado
   - Pruebas automatizadas para detectar problemas temprano
   - Refactorización continua

3. **Calidad Integrada**:
   - Pruebas unitarias desde el inicio
   - Revisiones de código
   - Documentación actualizada con el código

4. **Aprendizaje Continuo**:
   - Retrospectivas al final de cada iteración
   - Ajuste del plan según lo aprendido

## Beneficios de esta Estructura

1. **Mantenibilidad**: Código organizado y fácil de entender
2. **Testabilidad**: Componentes aislados fáciles de probar
3. **Extensibilidad**: Fácil añadir nuevas características
4. **Independencia Tecnológica**: El núcleo no depende de frameworks específicos
5. **Desarrollo Paralelo**: Equipos pueden trabajar en frontend y backend simultáneamente
