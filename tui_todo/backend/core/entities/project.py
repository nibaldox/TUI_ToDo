#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo que define la entidad Project (Proyecto).

Este módulo contiene la definición de la clase Project, que representa
un proyecto o categoría en el sistema TUI ToDo.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import uuid4


@dataclass
class Project:
    """
    Clase que representa un proyecto o categoría en el sistema.
    
    Un proyecto puede contener tareas y también puede tener subproyectos,
    formando una estructura jerárquica.
    
    Attributes:
        name: Nombre del proyecto
        id: Identificador único del proyecto
        description: Descripción detallada (opcional)
        color: Color asociado al proyecto para visualización
        created_at: Fecha y hora de creación
        parent_id: ID del proyecto padre (opcional)
        metadata: Metadatos adicionales
    """
    
    name: str
    id: str = field(default_factory=lambda: str(uuid4()))
    description: Optional[str] = None
    color: str = "blue"  # Color por defecto
    created_at: datetime = field(default_factory=datetime.now)
    parent_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_root(self) -> bool:
        """Verifica si el proyecto es un proyecto raíz (sin padre)."""
        return self.parent_id is None
    
    def update_metadata(self, key: str, value: Any) -> None:
        """Actualiza un valor en los metadatos del proyecto."""
        self.metadata[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el proyecto a un diccionario."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "color": self.color,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "parent_id": self.parent_id,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        """Crea una instancia de Project a partir de un diccionario."""
        # Convertir strings de fecha a objetos datetime
        created_at = datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None
        
        return cls(
            id=data.get("id"),
            name=data["name"],
            description=data.get("description"),
            color=data.get("color", "blue"),
            created_at=created_at,
            parent_id=data.get("parent_id"),
            metadata=data.get("metadata", {})
        )
