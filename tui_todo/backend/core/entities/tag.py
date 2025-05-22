#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo que define la entidad Tag (Etiqueta).

Este módulo contiene la definición de la clase Tag, que representa
una etiqueta que puede ser asociada a tareas en el sistema TUI ToDo.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import uuid4


@dataclass
class Tag:
    """
    Clase que representa una etiqueta en el sistema.
    
    Las etiquetas pueden ser asociadas a tareas para facilitar
    la organización y búsqueda.
    
    Attributes:
        name: Nombre de la etiqueta
        id: Identificador único de la etiqueta
        color: Color asociado a la etiqueta para visualización
        created_at: Fecha y hora de creación
        description: Descripción opcional de la etiqueta
        metadata: Metadatos adicionales
    """
    
    name: str
    id: str = field(default_factory=lambda: str(uuid4()))
    color: str = "gray"  # Color por defecto
    created_at: datetime = field(default_factory=datetime.now)
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la etiqueta a un diccionario."""
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "description": self.description,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Tag':
        """Crea una instancia de Tag a partir de un diccionario."""
        # Convertir strings de fecha a objetos datetime
        created_at = datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None
        
        return cls(
            id=data.get("id"),
            name=data["name"],
            color=data.get("color", "gray"),
            created_at=created_at,
            description=data.get("description"),
            metadata=data.get("metadata", {})
        )
