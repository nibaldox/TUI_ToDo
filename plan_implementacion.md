# Plan de Implementación: Backend para TUI ToDo

## Resumen del Proyecto

TUI ToDo es un sistema avanzado de gestión de tareas en terminal que combina la eficiencia de las interfaces TUI con funcionalidades avanzadas de organización personal. Este documento detalla el plan para implementar el backend que dará soporte a todas las funcionalidades planificadas.

## Objetivos

1. Crear un sistema de almacenamiento persistente para tareas y proyectos
2. Implementar un modelo de datos flexible que soporte estados múltiples de tareas
3. Desarrollar un sistema de filtrado y búsqueda eficiente
4. Permitir la sincronización con servicios externos (opcional)
5. Mantener la eficiencia y velocidad característica de las aplicaciones de terminal

## Fases de Implementación

### Fase 0: Configuración del Proyecto y Estructura (Semana 0)

#### Tareas

- [x] Diseñar la arquitectura del proyecto (Clean Architecture)
- [x] Crear documento de estructura del proyecto (`estructura.md`)
- [x] Crear la estructura de directorios base
  - [x] Crear estructura para el backend (core, adapters, frameworks)
  - [x] Crear estructura para el frontend (widgets, views, controllers)
  - [x] Crear estructura para pruebas (tests/backend, tests/frontend)
  - [x] Crear estructura para documentación (docs)
  - [x] Crear estructura para scripts (scripts)
- [x] Inicializar paquetes Python con archivos `__init__.py`
- [x] Crear archivos principales
  - [x] Crear `main.py` en la raíz del proyecto
  - [x] Crear `app.py` en el frontend
- [x] Configurar entorno de desarrollo
  - [x] Actualizar `requirements.txt` con dependencias
  - [x] Crear script de configuración inicial (`scripts/setup_dev.py`)

### Fase 1: Estructura Base y Modelos de Datos (Semana 1)

#### Tareas

- [x] Definir modelo de datos para tareas (`Task`) # COMPLETADO
  - Atributos: id, título, descripción, estado, fecha_creación, fecha_vencimiento, prioridad, etiquetas, proyecto_id
- [x] Definir modelo de datos para proyectos/categorías (`Project`) # COMPLETADO
  - Atributos: id, nombre, descripción, color, padre_id (para jerarquía)
- [x] Definir modelo para etiquetas (`Tag`) # COMPLETADO
  - Atributos: id, nombre, color
- [x] Implementar relaciones entre modelos # COMPLETADO
- [x] Crear tests unitarios para los modelos # COMPLETADO

#### Entregables

- Módulos Python con clases de modelos
- Documentación de la estructura de datos
- Tests unitarios

### Fase 2: Sistema de Almacenamiento (Semana 2)

#### Tareas

- [x] Implementar capa de abstracción para almacenamiento (`StorageInterface`) # COMPLETADO
- [x] Desarrollar almacenamiento basado en SQLite # COMPLETADO
  - [x] Crear esquema de base de datos # COMPLETADO
  - [ ] Implementar almacenamiento alternativo basado en archivos JSON
    - Serialización/deserialización de modelos
    - Gestión de archivos
- [ ] Crear sistema de migración para actualizaciones futuras # PENDIENTE
- [x] Implementar mecanismo de respaldo automático (`DatabaseService.backup`) # COMPLETADO

#### Entregables

- Módulo de base de datos SQLite funcional
- Módulo de almacenamiento basado en archivos JSON (parcial)
- Herramientas de migración y respaldo
- Tests de integración de la capa de almacenamiento

### Fase 3: Lógica de Negocio y Controladores (Semana 3)

#### Estado actual

- Casos de uso (use cases) implementados para tareas, proyectos y etiquetas.
- Repositorios y entidades conectados y funcionales.
- Script de inicialización y datos de ejemplo funcionando.
- [x] Pruebas unitarias e integración de repositorios y casos de uso completadas.

#### Próximos pasos inmediatos

- [x] Iniciar el desarrollo de la interfaz TUI con Textual
  - [x] Vista de lista de tareas con filtros
  - [x] Integración con TaskController para listado de tareas
  - [ ] Vista de lista de proyectos
- [ ] Comenzar pruebas manuales de la UI
- [ ] Documentar componentes y flujos de la interfaz

#### Tareas

- [x] Desarrollar controlador de tareas (`TaskController`)
  - [x] Métodos para crear, actualizar, eliminar y consultar tareas
  - [x] Lógica para gestionar estados y transiciones
- [x] Implementar controlador de proyectos (`ProjectController`)
  - [x] Gestión de la jerarquía de proyectos
  - [x] Operaciones de reorganización
- [x] Crear sistema de filtros y búsqueda (`FilterController`)
  - [x] Búsqueda por texto
  - [x] Filtrado por estado, fecha, etiquetas, etc.
- [x] Desarrollar sistema de recordatorios (`ReminderController`)
  - [x] Lógica para detectar tareas próximas a vencer
  - [x] Mecanismo de notificación en terminal

#### Entregables

- [x] Controladores implementados y documentados
- [x] Sistema de filtros y búsqueda
- [x] Mecanismo de recordatorios
- [x] Tests de funcionalidad

### Fase 4: Integración con la Interfaz de Usuario (Semana 4)

#### Tareas

- [x] Refactorizar la UI actual para usar nuevos modelos y controladores
- [x] Implementar vistas para gestión de tareas
  - [x] Vista de lista de tareas con filtros
  - [x] Vista detallada de tareas
  - [x] Formularios para crear/editar tareas
- [x] Mejorar widget calendario (resaltar días, navegación meses)
- [x] Crear sistema de comandos rápidos (atajos CRUD)
- [x] Añadir validación de campos en formularios
- [x] Diseñar mensaje de confirmación al eliminar tarea

#### Próximos Pasos de UI

- [x] Validar título obligatorio en formularios
- [x] Implementar ConfirmDialog para eliminación
- [x] Añadir validación de fecha y notificaciones de error
- [ ] Documentar flujos de UI en README y manual de usuario

#### Entregables

- [x] UI integrada con backend
- [x] Nuevas vistas y widgets
- [x] Sistema de comandos y atajos
- [x] Validaciones y confirmaciones
- [ ] Manual de usuario actualizado

### Fase 5: Funcionalidades Avanzadas (Semana 5)

#### Tareas

- [x] Sincronización con servicios externos (CalDAV)
  - [x] Autenticación y manejo de credenciales
  - [x] Sincronización unidireccional básica
  - [x] Sincronización bidireccional  
    - [x] Diseño del modelo de sincronización (UID, etag, metadata)  
    - [x] Extender `CalDAVSyncService` con métodos `fetch_remote_changes`, `push_local_changes`, manejo de deletes  
    - [x] Estrategia de resolución de conflictos (“última modificación gana”)  
    - [ ] Pruebas unitarias e integración con servidor CalDAV simulado  
    - [x] UI/UX: atajo `sync_bidirectional` y mensajes de estado  
    - [x] Documentación: actualizar plan y README  
- [x] Exportación/Importación (iCal, CSV)
- [ ] Sistema de estadísticas y reportes
  - [ ] API de estadísticas (backend)
  - [ ] UI de reportes
- [ ] Plantillas para tareas recurrentes
  - [ ] Definir formato de plantilla y frecuencia
  - [ ] Scheduler para ejecución automática
- [ ] Framework de plugins
  - [ ] Diseñar interfaz de extensibilidad
  - [ ] Cargador dinámico de plugins
  - [ ] Ejemplo de plugin simple

#### Próximos Pasos Avanzados

- Implementar fetch_events en CalDAVSyncService
- Crear módulo de export/import (iCal, CSV)
- Desarrollar StatsService para métricas de tareas
- [x] Implementar sincronización bidireccional con CalDAV

#### Entregables

- [x] Módulo de sincronización completo
- [x] Funcionalidad de exportación/importación integrada
- [ ] API y UI de estadísticas funcionando
- [ ] Plantillas recurrentes operativas
- [ ] Framework de plugins con documentación y ejemplo

### Fase 6: Empaquetado y Despliegue (Semana 6)

#### Tareas

- [ ] Crear `setup.py` o `pyproject.toml` para distribuir CLI como paquete instalable
- [ ] Configurar `Dockerfile` e imagen Docker para la aplicación
- [ ] Configurar pipeline de CI/CD (GitHub Actions) que ejecute tests y despliegue
- [ ] Publicar paquete en PyPI (opcional)

#### Entregables

- Paquete instalable de la aplicación (CLI)
- Imagen Docker optimizada
- Pipeline de CI/CD documentado y funcionando
- Guía de instalación y despliegue

## Tecnologías a Utilizar

- **Base**: Python 3.7+
- **UI**: Textual, Rich
- **Almacenamiento**: SQLite, JSON
- **Testing**: Pytest
- **Documentación**: Markdown, Sphinx

## Consideraciones Técnicas

### Rendimiento

- Optimizar consultas a la base de datos para mantener la respuesta inmediata
- Implementar caché para datos frecuentemente accedidos
- Usar lazy loading para componentes pesados

### Seguridad

- Cifrar datos sensibles en almacenamiento
- Validar todas las entradas de usuario
- Implementar control de acceso si se añade soporte multiusuario

### Extensibilidad

- Diseñar con patrones que faciliten la extensión (Strategy, Observer, etc.)
- Documentar APIs internas para facilitar el desarrollo de plugins
- Mantener separación clara entre lógica de negocio e interfaz

## Métricas de Éxito

- Tiempo de respuesta < 100ms para operaciones comunes
- Capacidad para manejar > 10,000 tareas sin degradación de rendimiento
- Cobertura de tests > 80%
- Documentación completa y actualizada

## Riesgos y Mitigación

| Riesgo | Impacto | Probabilidad | Mitigación |
|--------|---------|--------------|------------|
| Complejidad excesiva en el modelo de datos | Alto | Media | Iteraciones frecuentes con prototipos simples |
| Problemas de rendimiento con muchas tareas | Alto | Baja | Pruebas de carga temprana, optimización proactiva |
| Dificultad en la integración UI/backend | Medio | Media | Desarrollo incremental, tests de integración |
| Compatibilidad con diferentes terminales | Bajo | Alta | Pruebas en múltiples entornos, uso de abstracciones |

## Próximos Pasos Inmediatos

1. Crear estructura de directorios y esqueleto de módulos
2. Implementar modelos básicos de datos
3. Configurar entorno de desarrollo y testing
4. Desarrollar prototipo inicial del sistema de almacenamiento

---

Este plan será revisado y actualizado regularmente a medida que avance el desarrollo.
