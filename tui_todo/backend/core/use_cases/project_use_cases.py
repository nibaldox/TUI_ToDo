#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Casos de uso para la gestión de proyectos.

Este módulo contiene los casos de uso relacionados con la gestión de proyectos,
que implementan la lógica de negocio de la aplicación.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any

from ..entities.project import Project
from ..entities.relationships import ProjectHierarchy
from ..interfaces.repositories import ProjectRepository, TaskRepository


class ProjectUseCases:
    """
    Casos de uso para la gestión de proyectos.
    
    Esta clase implementa la lógica de negocio relacionada con los proyectos,
    utilizando el repositorio de proyectos para la persistencia.
    
    Attributes:
        project_repository: Repositorio de proyectos
        task_repository: Repositorio de tareas (opcional)
    """
    
    def __init__(self, project_repository: ProjectRepository, task_repository: Optional[TaskRepository] = None):
        """
        Inicializa los casos de uso con los repositorios necesarios.
        
        Args:
            project_repository: Repositorio de proyectos a utilizar
            task_repository: Repositorio de tareas (opcional, para operaciones que involucren tareas)
        """
        self.project_repository = project_repository
        self.task_repository = task_repository
    
    def create_project(self, name: str, description: Optional[str] = None,
                      color: str = "blue", parent_id: Optional[str] = None,
                      metadata: Dict[str, Any] = None) -> Project:
        """
        Crea un nuevo proyecto.
        
        Args:
            name: Nombre del proyecto
            description: Descripción del proyecto (opcional)
            color: Color asociado al proyecto
            parent_id: ID del proyecto padre (opcional)
            metadata: Metadatos adicionales (opcional)
            
        Returns:
            El proyecto creado
        """
        # Verificar que el proyecto padre existe si se proporciona
        if parent_id is not None:
            parent = self.project_repository.get_by_id(parent_id)
            if parent is None:
                raise ValueError(f"El proyecto padre con ID {parent_id} no existe")
        
        # Crear el proyecto con los parámetros proporcionados
        project = Project(
            name=name,
            description=description,
            color=color,
            parent_id=parent_id,
            metadata=metadata or {}
        )
        
        # Guardar el proyecto en el repositorio
        return self.project_repository.save(project)
    
    def update_project(self, project_id: str, **kwargs) -> Optional[Project]:
        """
        Actualiza un proyecto existente.
        
        Args:
            project_id: ID del proyecto a actualizar
            **kwargs: Atributos a actualizar
            
        Returns:
            El proyecto actualizado si existe, None en caso contrario
        """
        # Obtener el proyecto existente
        project = self.project_repository.get_by_id(project_id)
        if project is None:
            return None
        
        # Verificar que el proyecto padre existe si se proporciona
        if 'parent_id' in kwargs and kwargs['parent_id'] is not None:
            parent_id = kwargs['parent_id']
            
            # Evitar ciclos en la jerarquía
            if parent_id == project_id:
                raise ValueError("Un proyecto no puede ser su propio padre")
            
            # Verificar que el padre existe
            parent = self.project_repository.get_by_id(parent_id)
            if parent is None:
                raise ValueError(f"El proyecto padre con ID {parent_id} no existe")
            
            # Verificar que no se cree un ciclo en la jerarquía
            hierarchy = self._build_project_hierarchy()
            descendants = hierarchy.get_all_descendants(project_id)
            if any(desc.id == parent_id for desc in descendants):
                raise ValueError("No se puede establecer un descendiente como padre (crearía un ciclo)")
        
        # Actualizar los atributos proporcionados
        for key, value in kwargs.items():
            if hasattr(project, key):
                setattr(project, key, value)
        
        # Guardar el proyecto actualizado
        return self.project_repository.update(project)
    
    def delete_project(self, project_id: str, delete_tasks: bool = False) -> bool:
        """
        Elimina un proyecto.
        
        Args:
            project_id: ID del proyecto a eliminar
            delete_tasks: Si es True, también elimina las tareas asociadas
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        # Verificar que el proyecto existe
        project = self.project_repository.get_by_id(project_id)
        if project is None:
            return False
        
        # Obtener subproyectos
        subprojects = self.project_repository.get_subprojects(project_id)
        
        # Si hay subproyectos, no permitir la eliminación
        if subprojects:
            raise ValueError(f"No se puede eliminar el proyecto porque tiene {len(subprojects)} subproyectos")
        
        # Eliminar tareas asociadas si se solicita y el repositorio de tareas está disponible
        if delete_tasks and self.task_repository is not None:
            tasks = self.task_repository.get_by_project(project_id)
            for task in tasks:
                self.task_repository.delete(task.id)
        
        # Eliminar el proyecto
        return self.project_repository.delete(project_id)
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """
        Obtiene un proyecto por su ID.
        
        Args:
            project_id: ID del proyecto a buscar
            
        Returns:
            El proyecto si existe, None en caso contrario
        """
        return self.project_repository.get_by_id(project_id)
    
    def get_all_projects(self) -> List[Project]:
        """
        Obtiene todos los proyectos.
        
        Returns:
            Lista de todos los proyectos
        """
        return self.project_repository.get_all()
    
    def get_root_projects(self) -> List[Project]:
        """
        Obtiene proyectos raíz (sin padre).
        
        Returns:
            Lista de proyectos raíz
        """
        return self.project_repository.get_root_projects()
    
    def get_subprojects(self, parent_id: str) -> List[Project]:
        """
        Obtiene subproyectos de un proyecto.
        
        Args:
            parent_id: ID del proyecto padre
            
        Returns:
            Lista de subproyectos
        """
        return self.project_repository.get_subprojects(parent_id)
    
    def get_project_hierarchy(self) -> ProjectHierarchy:
        """
        Obtiene la jerarquía completa de proyectos.
        
        Returns:
            Objeto ProjectHierarchy con la estructura jerárquica
        """
        return self._build_project_hierarchy()
    
    def get_project_path(self, project_id: str) -> List[Project]:
        """
        Obtiene la ruta completa desde la raíz hasta el proyecto.
        
        Args:
            project_id: ID del proyecto
            
        Returns:
            Lista de proyectos desde la raíz hasta el proyecto especificado
        """
        hierarchy = self._build_project_hierarchy()
        return hierarchy.get_path(project_id)
    
    def get_all_descendants(self, project_id: str) -> List[Project]:
        """
        Obtiene todos los descendientes de un proyecto.
        
        Args:
            project_id: ID del proyecto
            
        Returns:
            Lista de todos los proyectos descendientes
        """
        hierarchy = self._build_project_hierarchy()
        return hierarchy.get_all_descendants(project_id)
    
    def search_projects(self, query: str) -> List[Project]:
        """
        Busca proyectos por texto.
        
        Args:
            query: El texto a buscar en nombre y descripción
            
        Returns:
            Lista de proyectos que coinciden con la búsqueda
        """
        return self.project_repository.search(query)
    
    def _build_project_hierarchy(self) -> ProjectHierarchy:
        """
        Construye la jerarquía de proyectos a partir de los datos del repositorio.
        
        Returns:
            Objeto ProjectHierarchy con la estructura jerárquica
        """
        hierarchy = ProjectHierarchy()
        projects = self.project_repository.get_all()
        
        for project in projects:
            hierarchy.add_project(project)
        
        return hierarchy
