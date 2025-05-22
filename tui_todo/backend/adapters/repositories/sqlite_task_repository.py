#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implementación del repositorio de tareas usando SQLite.

Este módulo contiene la implementación concreta del repositorio de tareas
utilizando SQLite como mecanismo de persistencia.
"""

import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any
import json

from ...core.entities.task import Task, TaskStatus, TaskPriority
from ...core.interfaces.repositories import TaskRepository


class SQLiteTaskRepository(TaskRepository):
    """
    Implementación del repositorio de tareas usando SQLite.
    
    Esta clase implementa la interfaz TaskRepository utilizando
    SQLite como mecanismo de persistencia.
    
    Attributes:
        db_path: Ruta al archivo de base de datos SQLite
        connection: Conexión a la base de datos
    """
    
    def __init__(self, db_path: str):
        """
        Inicializa el repositorio con la ruta a la base de datos.
        
        Args:
            db_path: Ruta al archivo de base de datos SQLite
        """
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self._create_tables()
    
    def _create_tables(self) -> None:
        """Crea las tablas necesarias si no existen."""
        cursor = self.connection.cursor()
        
        # Tabla de tareas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT,
            due_date TEXT,
            completed_at TEXT,
            priority TEXT NOT NULL,
            tags TEXT,
            project_id TEXT,
            parent_id TEXT,
            metadata TEXT
        )
        ''')
        
        self.connection.commit()
    
    def save(self, task: Task) -> Task:
        """
        Guarda una tarea en la base de datos.
        
        Args:
            task: La tarea a guardar
            
        Returns:
            La tarea guardada
        """
        cursor = self.connection.cursor()
        
        # Convertir listas y diccionarios a JSON
        tags_json = json.dumps(task.tags)
        metadata_json = json.dumps(task.metadata)
        
        # Convertir fechas a ISO format
        created_at = task.created_at.isoformat() if task.created_at else None
        updated_at = datetime.now().isoformat()
        due_date = task.due_date.isoformat() if task.due_date else None
        completed_at = task.completed_at.isoformat() if task.completed_at else None
        
        cursor.execute('''
        INSERT OR REPLACE INTO tasks (
            id, title, description, status, created_at, updated_at, due_date,
            completed_at, priority, tags, project_id, parent_id, metadata
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            task.id, task.title, task.description, task.status.value, created_at,
            updated_at, due_date, completed_at, task.priority.value, tags_json,
            task.project_id, task.parent_id, metadata_json
        ))
        
        self.connection.commit()
        return task
    
    def get_by_id(self, task_id: str) -> Optional[Task]:
        """
        Obtiene una tarea por su ID.
        
        Args:
            task_id: El ID de la tarea a buscar
            
        Returns:
            La tarea si se encuentra, None en caso contrario
        """
        cursor = self.connection.cursor()
        
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        
        if row is None:
            return None
        
        return self._row_to_task(row)
    
    def get_all(self) -> List[Task]:
        """
        Obtiene todas las tareas.
        
        Returns:
            Lista de todas las tareas
        """
        cursor = self.connection.cursor()
        
        cursor.execute('SELECT * FROM tasks')
        rows = cursor.fetchall()
        
        return [self._row_to_task(row) for row in rows]
    
    def delete(self, task_id: str) -> bool:
        """
        Elimina una tarea por su ID.
        
        Args:
            task_id: El ID de la tarea a eliminar
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        cursor = self.connection.cursor()
        
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.connection.commit()
        
        return cursor.rowcount > 0
    
    def update(self, task: Task) -> Optional[Task]:
        """
        Actualiza una tarea existente.
        
        Args:
            task: La tarea con los datos actualizados
            
        Returns:
            La tarea actualizada si se encuentra, None en caso contrario
        """
        # Verificar si la tarea existe
        existing_task = self.get_by_id(task.id)
        if existing_task is None:
            return None
        
        # Guardar la tarea actualizada
        return self.save(task)
    
    def get_by_status(self, status: str) -> List[Task]:
        """
        Obtiene tareas por su estado.
        
        Args:
            status: El estado de las tareas a buscar
            
        Returns:
            Lista de tareas con el estado especificado
        """
        cursor = self.connection.cursor()
        
        cursor.execute('SELECT * FROM tasks WHERE status = ?', (status,))
        rows = cursor.fetchall()
        
        return [self._row_to_task(row) for row in rows]
    
    def get_by_project(self, project_id: str) -> List[Task]:
        """
        Obtiene tareas por su proyecto.
        
        Args:
            project_id: El ID del proyecto
            
        Returns:
            Lista de tareas asociadas al proyecto
        """
        cursor = self.connection.cursor()
        
        cursor.execute('SELECT * FROM tasks WHERE project_id = ?', (project_id,))
        rows = cursor.fetchall()
        
        return [self._row_to_task(row) for row in rows]
    
    def get_by_tag(self, tag: str) -> List[Task]:
        """
        Obtiene tareas por una etiqueta.
        
        Args:
            tag: La etiqueta a buscar
            
        Returns:
            Lista de tareas con la etiqueta especificada
        """
        cursor = self.connection.cursor()
        
        # Buscar tareas que contengan la etiqueta (usando LIKE con JSON)
        cursor.execute("SELECT * FROM tasks WHERE tags LIKE ?", (f'%"{tag}"%',))
        rows = cursor.fetchall()
        
        # Filtrar para asegurarse de que la etiqueta está realmente presente
        tasks = []
        for row in rows:
            task = self._row_to_task(row)
            if tag in task.tags:
                tasks.append(task)
        
        return tasks
    
    def get_overdue(self) -> List[Task]:
        """
        Obtiene tareas vencidas.
        
        Returns:
            Lista de tareas vencidas
        """
        cursor = self.connection.cursor()
        now = datetime.now().isoformat()
        
        # Obtener tareas con fecha de vencimiento anterior a ahora y no completadas
        cursor.execute('''
        SELECT * FROM tasks 
        WHERE due_date IS NOT NULL 
        AND due_date < ? 
        AND status != ?
        ''', (now, TaskStatus.COMPLETED.value))
        
        rows = cursor.fetchall()
        return [self._row_to_task(row) for row in rows]
    
    def search(self, query: str) -> List[Task]:
        """
        Busca tareas por texto.
        
        Args:
            query: El texto a buscar en título y descripción
            
        Returns:
            Lista de tareas que coinciden con la búsqueda
        """
        cursor = self.connection.cursor()
        search_term = f"%{query}%"
        
        cursor.execute('''
        SELECT * FROM tasks 
        WHERE title LIKE ? OR description LIKE ?
        ''', (search_term, search_term))
        
        rows = cursor.fetchall()
        return [self._row_to_task(row) for row in rows]
    
    def _row_to_task(self, row: sqlite3.Row) -> Task:
        """
        Convierte una fila de la base de datos a una instancia de Task.
        
        Args:
            row: Fila de la base de datos
            
        Returns:
            Instancia de Task
        """
        # Convertir JSON a listas y diccionarios
        tags = json.loads(row['tags']) if row['tags'] else []
        metadata = json.loads(row['metadata']) if row['metadata'] else {}
        
        # Convertir strings de fecha a objetos datetime
        created_at = datetime.fromisoformat(row['created_at']) if row['created_at'] else None
        due_date = datetime.fromisoformat(row['due_date']) if row['due_date'] else None
        completed_at = datetime.fromisoformat(row['completed_at']) if row['completed_at'] else None
        
        # Crear y retornar la tarea
        return Task(
            id=row['id'],
            title=row['title'],
            description=row['description'],
            status=TaskStatus(row['status']),
            created_at=created_at,
            due_date=due_date,
            completed_at=completed_at,
            priority=TaskPriority(row['priority']),
            tags=tags,
            project_id=row['project_id'],
            parent_id=row['parent_id'],
            metadata=metadata
        )
    
    def close(self) -> None:
        """Cierra la conexión a la base de datos."""
        if self.connection:
            self.connection.close()
