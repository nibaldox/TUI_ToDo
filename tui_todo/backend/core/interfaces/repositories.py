#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo que define las interfaces para los repositorios.

Este módulo contiene las clases abstractas que definen los contratos
que deben implementar los repositorios concretos para cada entidad.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Generic, TypeVar

from ..entities.task import Task
from ..entities.project import Project
from ..entities.tag import Tag

# Definición de tipos genéricos para las entidades
T = TypeVar('T')


class Repository(Generic[T], ABC):
    """
    Interfaz base para todos los repositorios.
    
    Define los métodos comunes que deben implementar todos los repositorios
    independientemente de la entidad que manejen.
    """
    
    @abstractmethod
    def save(self, entity: T) -> T:
        """
        Guarda una entidad en el repositorio.
        
        Args:
            entity: La entidad a guardar
            
        Returns:
            La entidad guardada, posiblemente con campos actualizados
        """
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """
        Obtiene una entidad por su ID.
        
        Args:
            entity_id: El ID de la entidad a buscar
            
        Returns:
            La entidad si se encuentra, None en caso contrario
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """
        Obtiene todas las entidades del repositorio.
        
        Returns:
            Lista de todas las entidades
        """
        pass
    
    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """
        Elimina una entidad del repositorio.
        
        Args:
            entity_id: El ID de la entidad a eliminar
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        pass
    
    @abstractmethod
    def update(self, entity: T) -> Optional[T]:
        """
        Actualiza una entidad existente.
        
        Args:
            entity: La entidad con los datos actualizados
            
        Returns:
            La entidad actualizada si se encuentra, None en caso contrario
        """
        pass


class TaskRepository(Repository[Task], ABC):
    """
    Interfaz para el repositorio de tareas.
    
    Extiende la interfaz base de repositorio y añade métodos específicos
    para las tareas.
    """
    
    @abstractmethod
    def get_by_status(self, status: str) -> List[Task]:
        """
        Obtiene tareas por su estado.
        
        Args:
            status: El estado de las tareas a buscar
            
        Returns:
            Lista de tareas con el estado especificado
        """
        pass
    
    @abstractmethod
    def get_by_project(self, project_id: str) -> List[Task]:
        """
        Obtiene tareas por su proyecto.
        
        Args:
            project_id: El ID del proyecto
            
        Returns:
            Lista de tareas asociadas al proyecto
        """
        pass
    
    @abstractmethod
    def get_by_tag(self, tag: str) -> List[Task]:
        """
        Obtiene tareas por una etiqueta.
        
        Args:
            tag: La etiqueta a buscar
            
        Returns:
            Lista de tareas con la etiqueta especificada
        """
        pass
    
    @abstractmethod
    def get_overdue(self) -> List[Task]:
        """
        Obtiene tareas vencidas.
        
        Returns:
            Lista de tareas vencidas
        """
        pass
    
    @abstractmethod
    def search(self, query: str) -> List[Task]:
        """
        Busca tareas por texto.
        
        Args:
            query: El texto a buscar en título y descripción
            
        Returns:
            Lista de tareas que coinciden con la búsqueda
        """
        pass


class ProjectRepository(Repository[Project], ABC):
    """
    Interfaz para el repositorio de proyectos.
    
    Extiende la interfaz base de repositorio y añade métodos específicos
    para los proyectos.
    """
    
    @abstractmethod
    def get_root_projects(self) -> List[Project]:
        """
        Obtiene proyectos raíz (sin padre).
        
        Returns:
            Lista de proyectos raíz
        """
        pass
    
    @abstractmethod
    def get_subprojects(self, parent_id: str) -> List[Project]:
        """
        Obtiene subproyectos de un proyecto.
        
        Args:
            parent_id: El ID del proyecto padre
            
        Returns:
            Lista de subproyectos
        """
        pass
    
    @abstractmethod
    def search(self, query: str) -> List[Project]:
        """
        Busca proyectos por texto.
        
        Args:
            query: El texto a buscar en nombre y descripción
            
        Returns:
            Lista de proyectos que coinciden con la búsqueda
        """
        pass


class TagRepository(Repository[Tag], ABC):
    """
    Interfaz para el repositorio de etiquetas.
    
    Extiende la interfaz base de repositorio y añade métodos específicos
    para las etiquetas.
    """
    
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Tag]:
        """
        Obtiene una etiqueta por su nombre.
        
        Args:
            name: El nombre de la etiqueta
            
        Returns:
            La etiqueta si se encuentra, None en caso contrario
        """
        pass
    
    @abstractmethod
    def get_all_with_count(self) -> Dict[Tag, int]:
        """
        Obtiene todas las etiquetas con el número de tareas asociadas.
        
        Returns:
            Diccionario con etiquetas como claves y conteo como valores
        """
        pass
