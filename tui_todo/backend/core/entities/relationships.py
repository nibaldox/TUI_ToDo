#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo que define las relaciones entre entidades.

Este módulo contiene clases y funciones para manejar las relaciones
entre las diferentes entidades del sistema (tareas, proyectos, etiquetas).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set

from .task import Task
from .project import Project
from .tag import Tag


@dataclass
class ProjectHierarchy:
    """
    Clase que representa la jerarquía de proyectos.
    
    Permite navegar fácilmente la estructura de árbol de proyectos.
    
    Attributes:
        projects: Diccionario de proyectos por ID
        children: Diccionario que mapea IDs de proyectos a sus hijos
        root_projects: Lista de IDs de proyectos raíz
    """
    
    projects: Dict[str, Project] = field(default_factory=dict)
    children: Dict[str, List[str]] = field(default_factory=dict)
    root_projects: List[str] = field(default_factory=list)
    
    def add_project(self, project: Project) -> None:
        """
        Añade un proyecto a la jerarquía.
        
        Args:
            project: El proyecto a añadir
        """
        self.projects[project.id] = project
        
        # Si es un proyecto raíz, añadirlo a la lista de raíces
        if project.parent_id is None:
            if project.id not in self.root_projects:
                self.root_projects.append(project.id)
        else:
            # Si tiene padre, añadirlo a la lista de hijos del padre
            if project.parent_id not in self.children:
                self.children[project.parent_id] = []
            
            if project.id not in self.children[project.parent_id]:
                self.children[project.parent_id].append(project.id)
    
    def get_children(self, project_id: str) -> List[Project]:
        """
        Obtiene los proyectos hijos de un proyecto.
        
        Args:
            project_id: ID del proyecto padre
            
        Returns:
            Lista de proyectos hijos
        """
        child_ids = self.children.get(project_id, [])
        return [self.projects[child_id] for child_id in child_ids if child_id in self.projects]
    
    def get_all_descendants(self, project_id: str) -> List[Project]:
        """
        Obtiene todos los descendientes de un proyecto (hijos, nietos, etc.).
        
        Args:
            project_id: ID del proyecto padre
            
        Returns:
            Lista de todos los proyectos descendientes
        """
        result = []
        
        # Obtener hijos directos
        children = self.get_children(project_id)
        result.extend(children)
        
        # Recursivamente obtener descendientes de cada hijo
        for child in children:
            result.extend(self.get_all_descendants(child.id))
        
        return result
    
    def get_path(self, project_id: str) -> List[Project]:
        """
        Obtiene la ruta completa desde la raíz hasta el proyecto.
        
        Args:
            project_id: ID del proyecto
            
        Returns:
            Lista de proyectos desde la raíz hasta el proyecto especificado
        """
        result = []
        current_id = project_id
        
        while current_id is not None:
            if current_id not in self.projects:
                break
                
            project = self.projects[current_id]
            result.insert(0, project)  # Insertar al principio para mantener el orden
            current_id = project.parent_id
            
        return result


@dataclass
class TaskCollection:
    """
    Clase que representa una colección de tareas con funcionalidades adicionales.
    
    Permite organizar y filtrar tareas de diferentes maneras.
    
    Attributes:
        tasks: Diccionario de tareas por ID
        project_tasks: Diccionario que mapea IDs de proyectos a IDs de tareas
        tag_tasks: Diccionario que mapea etiquetas a IDs de tareas
    """
    
    tasks: Dict[str, Task] = field(default_factory=dict)
    project_tasks: Dict[str, List[str]] = field(default_factory=dict)
    tag_tasks: Dict[str, List[str]] = field(default_factory=dict)
    
    def add_task(self, task: Task) -> None:
        """
        Añade una tarea a la colección.
        
        Args:
            task: La tarea a añadir
        """
        self.tasks[task.id] = task
        
        # Asociar con proyecto si existe
        if task.project_id:
            if task.project_id not in self.project_tasks:
                self.project_tasks[task.project_id] = []
            
            if task.id not in self.project_tasks[task.project_id]:
                self.project_tasks[task.project_id].append(task.id)
        
        # Asociar con etiquetas
        for tag in task.tags:
            if tag not in self.tag_tasks:
                self.tag_tasks[tag] = []
            
            if task.id not in self.tag_tasks[tag]:
                self.tag_tasks[tag].append(task.id)
    
    def remove_task(self, task_id: str) -> None:
        """
        Elimina una tarea de la colección.
        
        Args:
            task_id: ID de la tarea a eliminar
        """
        if task_id not in self.tasks:
            return
            
        task = self.tasks[task_id]
        
        # Eliminar de proyecto
        if task.project_id and task.project_id in self.project_tasks:
            if task_id in self.project_tasks[task.project_id]:
                self.project_tasks[task.project_id].remove(task_id)
        
        # Eliminar de etiquetas
        for tag in task.tags:
            if tag in self.tag_tasks and task_id in self.tag_tasks[tag]:
                self.tag_tasks[tag].remove(task_id)
        
        # Eliminar la tarea
        del self.tasks[task_id]
    
    def get_by_project(self, project_id: str) -> List[Task]:
        """
        Obtiene tareas por proyecto.
        
        Args:
            project_id: ID del proyecto
            
        Returns:
            Lista de tareas del proyecto
        """
        task_ids = self.project_tasks.get(project_id, [])
        return [self.tasks[task_id] for task_id in task_ids if task_id in self.tasks]
    
    def get_by_tag(self, tag: str) -> List[Task]:
        """
        Obtiene tareas por etiqueta.
        
        Args:
            tag: Nombre de la etiqueta
            
        Returns:
            Lista de tareas con la etiqueta
        """
        task_ids = self.tag_tasks.get(tag, [])
        return [self.tasks[task_id] for task_id in task_ids if task_id in self.tasks]
    
    def get_by_status(self, status: str) -> List[Task]:
        """
        Obtiene tareas por estado.
        
        Args:
            status: Estado de las tareas
            
        Returns:
            Lista de tareas con el estado especificado
        """
        return [task for task in self.tasks.values() if task.status.value == status]
    
    def get_overdue(self) -> List[Task]:
        """
        Obtiene tareas vencidas.
        
        Returns:
            Lista de tareas vencidas
        """
        return [task for task in self.tasks.values() if task.is_overdue()]


def get_task_tags(tasks: List[Task]) -> Dict[str, int]:
    """
    Obtiene todas las etiquetas usadas en un conjunto de tareas con su frecuencia.
    
    Args:
        tasks: Lista de tareas a analizar
        
    Returns:
        Diccionario con etiquetas como claves y frecuencia como valores
    """
    tag_counts = {}
    
    for task in tasks:
        for tag in task.tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    return tag_counts
