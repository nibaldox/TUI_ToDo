#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Casos de uso para la gestión de etiquetas.

Este módulo contiene los casos de uso relacionados con la gestión de etiquetas,
que implementan la lógica de negocio de la aplicación.
"""

from typing import List, Optional, Dict, Any

from ..entities.tag import Tag
from ..interfaces.repositories import TagRepository, TaskRepository


class TagUseCases:
    """
    Casos de uso para la gestión de etiquetas.
    
    Esta clase implementa la lógica de negocio relacionada con las etiquetas,
    utilizando el repositorio de etiquetas para la persistencia.
    
    Attributes:
        tag_repository: Repositorio de etiquetas
        task_repository: Repositorio de tareas (opcional)
    """
    
    def __init__(self, tag_repository: TagRepository, task_repository: Optional[TaskRepository] = None):
        """
        Inicializa los casos de uso con los repositorios necesarios.
        
        Args:
            tag_repository: Repositorio de etiquetas a utilizar
            task_repository: Repositorio de tareas (opcional, para operaciones que involucren tareas)
        """
        self.tag_repository = tag_repository
        self.task_repository = task_repository
    
    def create_tag(self, name: str, description: Optional[str] = None,
                  color: str = "gray", metadata: Dict[str, Any] = None) -> Tag:
        """
        Crea una nueva etiqueta.
        
        Args:
            name: Nombre de la etiqueta
            description: Descripción de la etiqueta (opcional)
            color: Color asociado a la etiqueta
            metadata: Metadatos adicionales (opcional)
            
        Returns:
            La etiqueta creada
        """
        # Verificar si ya existe una etiqueta con el mismo nombre
        existing_tag = self.tag_repository.get_by_name(name)
        if existing_tag is not None:
            raise ValueError(f"Ya existe una etiqueta con el nombre '{name}'")
        
        # Crear la etiqueta con los parámetros proporcionados
        tag = Tag(
            name=name,
            description=description,
            color=color,
            metadata=metadata or {}
        )
        
        # Guardar la etiqueta en el repositorio
        return self.tag_repository.save(tag)
    
    def update_tag(self, tag_id: str, **kwargs) -> Optional[Tag]:
        """
        Actualiza una etiqueta existente.
        
        Args:
            tag_id: ID de la etiqueta a actualizar
            **kwargs: Atributos a actualizar
            
        Returns:
            La etiqueta actualizada si existe, None en caso contrario
        """
        # Obtener la etiqueta existente
        tag = self.tag_repository.get_by_id(tag_id)
        if tag is None:
            return None
        
        # Verificar si se está cambiando el nombre y si el nuevo nombre ya existe
        if 'name' in kwargs and kwargs['name'] != tag.name:
            existing_tag = self.tag_repository.get_by_name(kwargs['name'])
            if existing_tag is not None:
                raise ValueError(f"Ya existe una etiqueta con el nombre '{kwargs['name']}'")
        
        # Actualizar los atributos proporcionados
        for key, value in kwargs.items():
            if hasattr(tag, key):
                setattr(tag, key, value)
        
        # Guardar la etiqueta actualizada
        return self.tag_repository.update(tag)
    
    def delete_tag(self, tag_id: str, remove_from_tasks: bool = False) -> bool:
        """
        Elimina una etiqueta.
        
        Args:
            tag_id: ID de la etiqueta a eliminar
            remove_from_tasks: Si es True, también elimina la etiqueta de las tareas asociadas
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        # Verificar que la etiqueta existe
        tag = self.tag_repository.get_by_id(tag_id)
        if tag is None:
            return False
        
        # Eliminar la etiqueta de las tareas si se solicita y el repositorio de tareas está disponible
        if remove_from_tasks and self.task_repository is not None:
            tasks = self.task_repository.get_by_tag(tag.name)
            for task in tasks:
                task.remove_tag(tag.name)
                self.task_repository.update(task)
        
        # Eliminar la etiqueta
        return self.tag_repository.delete(tag_id)
    
    def get_tag(self, tag_id: str) -> Optional[Tag]:
        """
        Obtiene una etiqueta por su ID.
        
        Args:
            tag_id: ID de la etiqueta a buscar
            
        Returns:
            La etiqueta si existe, None en caso contrario
        """
        return self.tag_repository.get_by_id(tag_id)
    
    def get_tag_by_name(self, name: str) -> Optional[Tag]:
        """
        Obtiene una etiqueta por su nombre.
        
        Args:
            name: Nombre de la etiqueta
            
        Returns:
            La etiqueta si existe, None en caso contrario
        """
        return self.tag_repository.get_by_name(name)
    
    def get_all_tags(self) -> List[Tag]:
        """
        Obtiene todas las etiquetas.
        
        Returns:
            Lista de todas las etiquetas
        """
        return self.tag_repository.get_all()
    
    def get_tags_with_usage_count(self) -> Dict[Tag, int]:
        """
        Obtiene todas las etiquetas con su frecuencia de uso.
        
        Returns:
            Diccionario con etiquetas como claves y frecuencia como valores
        """
        return self.tag_repository.get_all_with_count()
    
    def get_or_create_tag(self, name: str, color: str = "gray") -> Tag:
        """
        Obtiene una etiqueta existente o crea una nueva si no existe.
        
        Args:
            name: Nombre de la etiqueta
            color: Color a usar si se crea una nueva etiqueta
            
        Returns:
            La etiqueta existente o la nueva etiqueta creada
        """
        tag = self.tag_repository.get_by_name(name)
        if tag is not None:
            return tag
        
        return self.create_tag(name=name, color=color)
