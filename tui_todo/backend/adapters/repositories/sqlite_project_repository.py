#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implementación del repositorio de proyectos usando SQLite.

Este módulo contiene la implementación concreta del repositorio de proyectos
utilizando SQLite como mecanismo de persistencia.
"""

import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any
import json

from ...core.entities.project import Project
from ...core.interfaces.repositories import ProjectRepository


class SQLiteProjectRepository(ProjectRepository):
    """
    Implementación del repositorio de proyectos usando SQLite.
    
    Esta clase implementa la interfaz ProjectRepository utilizando
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
        
        # Tabla de proyectos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            color TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT,
            parent_id TEXT,
            metadata TEXT
        )
        ''')
        
        self.connection.commit()
    
    def save(self, project: Project) -> Project:
        """
        Guarda un proyecto en la base de datos.
        
        Args:
            project: El proyecto a guardar
            
        Returns:
            El proyecto guardado
        """
        cursor = self.connection.cursor()
        
        # Convertir diccionario a JSON
        metadata_json = json.dumps(project.metadata)
        
        # Convertir fechas a ISO format
        created_at = project.created_at.isoformat() if project.created_at else None
        updated_at = datetime.now().isoformat()
        
        cursor.execute('''
        INSERT OR REPLACE INTO projects (
            id, name, description, color, created_at, updated_at, parent_id, metadata
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            project.id, project.name, project.description, project.color,
            created_at, updated_at, project.parent_id, metadata_json
        ))
        
        self.connection.commit()
        return project
    
    def get_by_id(self, project_id: str) -> Optional[Project]:
        """
        Obtiene un proyecto por su ID.
        
        Args:
            project_id: El ID del proyecto a buscar
            
        Returns:
            El proyecto si se encuentra, None en caso contrario
        """
        cursor = self.connection.cursor()
        
        cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        row = cursor.fetchone()
        
        if row is None:
            return None
        
        return self._row_to_project(row)
    
    def get_all(self) -> List[Project]:
        """
        Obtiene todos los proyectos.
        
        Returns:
            Lista de todos los proyectos
        """
        cursor = self.connection.cursor()
        
        cursor.execute('SELECT * FROM projects')
        rows = cursor.fetchall()
        
        return [self._row_to_project(row) for row in rows]
    
    def delete(self, project_id: str) -> bool:
        """
        Elimina un proyecto por su ID.
        
        Args:
            project_id: El ID del proyecto a eliminar
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        cursor = self.connection.cursor()
        
        cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        self.connection.commit()
        
        return cursor.rowcount > 0
    
    def update(self, project: Project) -> Optional[Project]:
        """
        Actualiza un proyecto existente.
        
        Args:
            project: El proyecto con los datos actualizados
            
        Returns:
            El proyecto actualizado si se encuentra, None en caso contrario
        """
        # Verificar si el proyecto existe
        existing_project = self.get_by_id(project.id)
        if existing_project is None:
            return None
        
        # Guardar el proyecto actualizado
        return self.save(project)
    
    def get_root_projects(self) -> List[Project]:
        """
        Obtiene proyectos raíz (sin padre).
        
        Returns:
            Lista de proyectos raíz
        """
        cursor = self.connection.cursor()
        
        cursor.execute('SELECT * FROM projects WHERE parent_id IS NULL')
        rows = cursor.fetchall()
        
        return [self._row_to_project(row) for row in rows]
    
    def get_subprojects(self, parent_id: str) -> List[Project]:
        """
        Obtiene subproyectos de un proyecto.
        
        Args:
            parent_id: El ID del proyecto padre
            
        Returns:
            Lista de subproyectos
        """
        cursor = self.connection.cursor()
        
        cursor.execute('SELECT * FROM projects WHERE parent_id = ?', (parent_id,))
        rows = cursor.fetchall()
        
        return [self._row_to_project(row) for row in rows]
    
    def search(self, query: str) -> List[Project]:
        """
        Busca proyectos por texto.
        
        Args:
            query: El texto a buscar en nombre y descripción
            
        Returns:
            Lista de proyectos que coinciden con la búsqueda
        """
        cursor = self.connection.cursor()
        search_term = f"%{query}%"
        
        cursor.execute('''
        SELECT * FROM projects 
        WHERE name LIKE ? OR description LIKE ?
        ''', (search_term, search_term))
        
        rows = cursor.fetchall()
        return [self._row_to_project(row) for row in rows]
    
    def _row_to_project(self, row: sqlite3.Row) -> Project:
        """
        Convierte una fila de la base de datos a una instancia de Project.
        
        Args:
            row: Fila de la base de datos
            
        Returns:
            Instancia de Project
        """
        # Convertir JSON a diccionario
        metadata = json.loads(row['metadata']) if row['metadata'] else {}
        
        # Convertir strings de fecha a objetos datetime
        created_at = datetime.fromisoformat(row['created_at']) if row['created_at'] else None
        
        # Crear y retornar el proyecto
        return Project(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            color=row['color'],
            created_at=created_at,
            parent_id=row['parent_id'],
            metadata=metadata
        )
    
    def close(self) -> None:
        """Cierra la conexión a la base de datos."""
        if self.connection:
            self.connection.close()
