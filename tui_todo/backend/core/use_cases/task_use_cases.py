#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Casos de uso para la gestión de tareas.

Este módulo contiene los casos de uso relacionados con la gestión de tareas,
que implementan la lógica de negocio de la aplicación.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any

from ..entities.task import Task, TaskStatus, TaskPriority
from ..interfaces.repositories import TaskRepository


class TaskUseCases:
    """
    Casos de uso para la gestión de tareas.
    
    Esta clase implementa la lógica de negocio relacionada con las tareas,
    utilizando el repositorio de tareas para la persistencia.
    
    Attributes:
        task_repository: Repositorio de tareas
    """
    
    def __init__(self, task_repository: TaskRepository):
        """
        Inicializa los casos de uso con el repositorio de tareas.
        
        Args:
            task_repository: Repositorio de tareas a utilizar
        """
        self.task_repository = task_repository
    
    def create_task(self, title: str, description: Optional[str] = None,
                   due_date: Optional[datetime] = None, 
                   priority: TaskPriority = TaskPriority.MEDIUM,
                   tags: List[str] = None, project_id: Optional[str] = None,
                   parent_id: Optional[str] = None) -> Task:
        """
        Crea una nueva tarea.
        
        Args:
            title: Título de la tarea
            description: Descripción de la tarea (opcional)
            due_date: Fecha de vencimiento (opcional)
            priority: Prioridad de la tarea
            tags: Lista de etiquetas (opcional)
            project_id: ID del proyecto asociado (opcional)
            parent_id: ID de la tarea padre (opcional)
            
        Returns:
            La tarea creada
        """
        # Crear la tarea con los parámetros proporcionados
        task = Task(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            tags=tags or [],
            project_id=project_id,
            parent_id=parent_id
        )
        
        # Guardar la tarea en el repositorio
        return self.task_repository.save(task)
    
    def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        """
        Actualiza una tarea existente.
        
        Args:
            task_id: ID de la tarea a actualizar
            **kwargs: Atributos a actualizar
            
        Returns:
            La tarea actualizada si existe, None en caso contrario
        """
        # Obtener la tarea existente
        task = self.task_repository.get_by_id(task_id)
        if task is None:
            return None
        
        # Actualizar los atributos proporcionados
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        # Guardar la tarea actualizada
        return self.task_repository.update(task)
    
    def delete_task(self, task_id: str) -> bool:
        """
        Elimina una tarea.
        
        Args:
            task_id: ID de la tarea a eliminar
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        return self.task_repository.delete(task_id)
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Obtiene una tarea por su ID.
        
        Args:
            task_id: ID de la tarea a buscar
            
        Returns:
            La tarea si existe, None en caso contrario
        """
        return self.task_repository.get_by_id(task_id)
    
    def get_all_tasks(self) -> List[Task]:
        """
        Obtiene todas las tareas.
        
        Returns:
            Lista de todas las tareas
        """
        return self.task_repository.get_all()
    
    def complete_task(self, task_id: str) -> Optional[Task]:
        """
        Marca una tarea como completada.
        
        Args:
            task_id: ID de la tarea a completar
            
        Returns:
            La tarea actualizada si existe, None en caso contrario
        """
        task = self.task_repository.get_by_id(task_id)
        if task is None:
            return None
        
        task.complete()
        return self.task_repository.update(task)
    
    def reopen_task(self, task_id: str) -> Optional[Task]:
        """
        Reabre una tarea completada.
        
        Args:
            task_id: ID de la tarea a reabrir
            
        Returns:
            La tarea actualizada si existe, None en caso contrario
        """
        task = self.task_repository.get_by_id(task_id)
        if task is None:
            return None
        
        task.reopen()
        return self.task_repository.update(task)
    
    def change_task_status(self, task_id: str, status: TaskStatus) -> Optional[Task]:
        """
        Cambia el estado de una tarea.
        
        Args:
            task_id: ID de la tarea
            status: Nuevo estado
            
        Returns:
            La tarea actualizada si existe, None en caso contrario
        """
        task = self.task_repository.get_by_id(task_id)
        if task is None:
            return None
        
        task.status = status
        
        # Si se marca como completada, establecer la fecha de completado
        if status == TaskStatus.COMPLETED and task.completed_at is None:
            task.completed_at = datetime.now()
        # Si se cambia de completada a otro estado, eliminar la fecha de completado
        elif status != TaskStatus.COMPLETED and task.completed_at is not None:
            task.completed_at = None
        
        return self.task_repository.update(task)
    
    def add_tag_to_task(self, task_id: str, tag: str) -> Optional[Task]:
        """
        Añade una etiqueta a una tarea.
        
        Args:
            task_id: ID de la tarea
            tag: Etiqueta a añadir
            
        Returns:
            La tarea actualizada si existe, None en caso contrario
        """
        task = self.task_repository.get_by_id(task_id)
        if task is None:
            return None
        
        task.add_tag(tag)
        return self.task_repository.update(task)
    
    def remove_tag_from_task(self, task_id: str, tag: str) -> Optional[Task]:
        """
        Elimina una etiqueta de una tarea.
        
        Args:
            task_id: ID de la tarea
            tag: Etiqueta a eliminar
            
        Returns:
            La tarea actualizada si existe, None en caso contrario
        """
        task = self.task_repository.get_by_id(task_id)
        if task is None:
            return None
        
        task.remove_tag(tag)
        return self.task_repository.update(task)
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """
        Obtiene tareas por su estado.
        
        Args:
            status: Estado de las tareas a buscar
            
        Returns:
            Lista de tareas con el estado especificado
        """
        return self.task_repository.get_by_status(status.value)
    
    def get_tasks_by_project(self, project_id: str) -> List[Task]:
        """
        Obtiene tareas por su proyecto.
        
        Args:
            project_id: ID del proyecto
            
        Returns:
            Lista de tareas asociadas al proyecto
        """
        return self.task_repository.get_by_project(project_id)
    
    def get_tasks_by_tag(self, tag: str) -> List[Task]:
        """
        Obtiene tareas por una etiqueta.
        
        Args:
            tag: La etiqueta a buscar
            
        Returns:
            Lista de tareas con la etiqueta especificada
        """
        return self.task_repository.get_by_tag(tag)
    
    def get_overdue_tasks(self) -> List[Task]:
        """
        Obtiene tareas vencidas.
        
        Returns:
            Lista de tareas vencidas
        """
        return self.task_repository.get_overdue()
    
    def search_tasks(self, query: str) -> List[Task]:
        """
        Busca tareas por texto.
        
        Args:
            query: El texto a buscar en título y descripción
            
        Returns:
            Lista de tareas que coinciden con la búsqueda
        """
        return self.task_repository.search(query)
    
    def get_subtasks(self, parent_id: str) -> List[Task]:
        """
        Obtiene las subtareas de una tarea.
        
        Args:
            parent_id: ID de la tarea padre
            
        Returns:
            Lista de subtareas
        """
        # Implementación simple: filtrar todas las tareas por parent_id
        all_tasks = self.task_repository.get_all()
        return [task for task in all_tasks if task.parent_id == parent_id]
