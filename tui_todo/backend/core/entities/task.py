#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo que define la entidad Task (Tarea).

Este módulo contiene la definición de la clase Task, que representa
una tarea en el sistema TUI ToDo.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from uuid import uuid4


class TaskStatus(str, Enum):
    """Enumeración de posibles estados de una tarea."""
    PENDING = "pending"         # Pendiente
    IN_PROGRESS = "in_progress" # En progreso
    COMPLETED = "completed"     # Completada
    DEFERRED = "deferred"       # Diferida
    CANCELED = "canceled"       # Cancelada
    IMPORTANT = "important"     # Importante
    QUESTION = "question"       # Pregunta/Duda
    INFO = "info"               # Información
    PARTIAL = "partial"         # Parcialmente completada


class TaskPriority(str, Enum):
    """Enumeración de posibles prioridades de una tarea."""
    LOW = "low"         # Baja
    MEDIUM = "medium"   # Media
    HIGH = "high"       # Alta
    URGENT = "urgent"   # Urgente


@dataclass
class Task:
    """
    Clase que representa una tarea en el sistema.
    
    Attributes:
        title: Título de la tarea
        status: Estado actual de la tarea
        created_at: Fecha y hora de creación
        id: Identificador único de la tarea
        description: Descripción detallada (opcional)
        due_date: Fecha de vencimiento (opcional)
        completed_at: Fecha de completado (opcional)
        priority: Prioridad de la tarea
        tags: Etiquetas asociadas a la tarea
        project_id: ID del proyecto al que pertenece (opcional)
        parent_id: ID de la tarea padre si es una subtarea (opcional)
        etag: ETag para sincronización CalDAV (opcional)
        last_modified: Timestamp última modificación (opcional)
        metadata: Metadatos adicionales
    """
    
    title: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    id: str = field(default_factory=lambda: str(uuid4()))
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    tags: List[str] = field(default_factory=list)
    project_id: Optional[str] = None
    parent_id: Optional[str] = None
    etag: Optional[str] = None  # ETag para sincronización CalDAV
    last_modified: Optional[datetime] = None  # Timestamp última modificación
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def complete(self) -> None:
        """Marca la tarea como completada."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
    
    def reopen(self) -> None:
        """Reabre una tarea completada o cancelada."""
        self.status = TaskStatus.PENDING
        self.completed_at = None
    
    def defer(self) -> None:
        """Marca la tarea como diferida."""
        self.status = TaskStatus.DEFERRED
    
    def cancel(self) -> None:
        """Marca la tarea como cancelada."""
        self.status = TaskStatus.CANCELED
        
    def mark_important(self) -> None:
        """Marca la tarea como importante."""
        self.status = TaskStatus.IMPORTANT
        
    def mark_in_progress(self) -> None:
        """Marca la tarea como en progreso."""
        self.status = TaskStatus.IN_PROGRESS
    
    def is_overdue(self) -> bool:
        """Verifica si la tarea está vencida."""
        if not self.due_date:
            return False
        
        if self.status in [TaskStatus.COMPLETED, TaskStatus.CANCELED]:
            return False
            
        return datetime.now() > self.due_date
    
    def add_tag(self, tag: str) -> None:
        """Añade una etiqueta a la tarea."""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Elimina una etiqueta de la tarea."""
        if tag in self.tags:
            self.tags.remove(tag)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la tarea a un diccionario."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "priority": self.priority.value,
            "tags": self.tags,
            "project_id": self.project_id,
            "parent_id": self.parent_id,
            "etag": self.etag,
            "last_modified": self.last_modified.isoformat() if self.last_modified else None,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Crea una instancia de Task a partir de un diccionario."""
        # Convertir strings de fecha a objetos datetime
        created_at = datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None
        due_date = datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None
        completed_at = datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None
        last_modified = datetime.fromisoformat(data["last_modified"]) if data.get("last_modified") else None
        
        # Convertir strings de enumeraciones a objetos Enum
        status = TaskStatus(data.get("status", "pending"))
        priority = TaskPriority(data.get("priority", "medium"))
        
        return cls(
            id=data.get("id"),
            title=data["title"],
            description=data.get("description"),
            status=status,
            created_at=created_at,
            due_date=due_date,
            completed_at=completed_at,
            priority=priority,
            tags=data.get("tags", []),
            project_id=data.get("project_id"),
            parent_id=data.get("parent_id"),
            etag=data.get("etag"),
            last_modified=last_modified,
            metadata=data.get("metadata", {})
        )
