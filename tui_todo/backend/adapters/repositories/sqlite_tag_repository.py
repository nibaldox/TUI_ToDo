#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implementación del repositorio de etiquetas usando SQLite.

Este módulo contiene la implementación concreta del repositorio de etiquetas
utilizando SQLite como mecanismo de persistencia.
"""

import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any
import json

from ...core.entities.tag import Tag
from ...core.interfaces.repositories import TagRepository


class SQLiteTagRepository(TagRepository):
    """
    Implementación del repositorio de etiquetas usando SQLite.
    
    Esta clase implementa la interfaz TagRepository utilizando
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
        
        # Tabla de etiquetas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            color TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT,
            metadata TEXT
        )
        ''')
        
        self.connection.commit()
    
    def save(self, tag: Tag) -> Tag:
        """
        Guarda una etiqueta en la base de datos.
        
        Args:
            tag: La etiqueta a guardar
            
        Returns:
            La etiqueta guardada
        """
        cursor = self.connection.cursor()
        
        # Convertir diccionario a JSON
        metadata_json = json.dumps(tag.metadata)
        
        # Convertir fechas a ISO format
        created_at = tag.created_at.isoformat() if tag.created_at else None
        updated_at = datetime.now().isoformat()
        
        cursor.execute('''
        INSERT OR REPLACE INTO tags (
            id, name, description, color, created_at, updated_at, metadata
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            tag.id, tag.name, tag.description, tag.color,
            created_at, updated_at, metadata_json
        ))
        
        self.connection.commit()
        return tag
    
    def get_by_id(self, tag_id: str) -> Optional[Tag]:
        """
        Obtiene una etiqueta por su ID.
        
        Args:
            tag_id: El ID de la etiqueta a buscar
            
        Returns:
            La etiqueta si se encuentra, None en caso contrario
        """
        cursor = self.connection.cursor()
        
        cursor.execute('SELECT * FROM tags WHERE id = ?', (tag_id,))
        row = cursor.fetchone()
        
        if row is None:
            return None
        
        return self._row_to_tag(row)
    
    def get_all(self) -> List[Tag]:
        """
        Obtiene todas las etiquetas.
        
        Returns:
            Lista de todas las etiquetas
        """
        cursor = self.connection.cursor()
        
        cursor.execute('SELECT * FROM tags')
        rows = cursor.fetchall()
        
        return [self._row_to_tag(row) for row in rows]
    
    def delete(self, tag_id: str) -> bool:
        """
        Elimina una etiqueta por su ID.
        
        Args:
            tag_id: El ID de la etiqueta a eliminar
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        cursor = self.connection.cursor()
        
        cursor.execute('DELETE FROM tags WHERE id = ?', (tag_id,))
        self.connection.commit()
        
        return cursor.rowcount > 0
    
    def update(self, tag: Tag) -> Optional[Tag]:
        """
        Actualiza una etiqueta existente.
        
        Args:
            tag: La etiqueta con los datos actualizados
            
        Returns:
            La etiqueta actualizada si se encuentra, None en caso contrario
        """
        # Verificar si la etiqueta existe
        existing_tag = self.get_by_id(tag.id)
        if existing_tag is None:
            return None
        
        # Guardar la etiqueta actualizada
        return self.save(tag)
    
    def get_by_name(self, name: str) -> Optional[Tag]:
        """
        Obtiene una etiqueta por su nombre.
        
        Args:
            name: El nombre de la etiqueta
            
        Returns:
            La etiqueta si se encuentra, None en caso contrario
        """
        cursor = self.connection.cursor()
        
        cursor.execute('SELECT * FROM tags WHERE name = ?', (name,))
        row = cursor.fetchone()
        
        if row is None:
            return None
        
        return self._row_to_tag(row)
    
    def get_all_with_count(self) -> list:
        """
        Obtiene todas las etiquetas con el número de tareas asociadas.

        Returns:
            Lista de diccionarios con los campos principales de la etiqueta y el conteo de uso:
            [{"id": ..., "name": ..., "color": ..., "description": ..., "count": ...}, ...]
        """
        cursor = self.connection.cursor()
        tags = self.get_all()
        result = []
        for tag in tags:
            cursor.execute('''
                SELECT COUNT(*) as count FROM tasks 
                WHERE tags LIKE ?
            ''', (f'%"{tag.name}"%',))
            row = cursor.fetchone()
            count = row['count'] if row else 0
            result.append({
                "id": tag.id,
                "name": tag.name,
                "color": tag.color,
                "description": tag.description,
                "count": count
            })
        return result

    
    def _row_to_tag(self, row: sqlite3.Row) -> Tag:
        """
        Convierte una fila de la base de datos a una instancia de Tag.
        
        Args:
            row: Fila de la base de datos
            
        Returns:
            Instancia de Tag
        """
        # Convertir JSON a diccionario
        metadata = json.loads(row['metadata']) if row['metadata'] else {}
        
        # Convertir strings de fecha a objetos datetime
        created_at = datetime.fromisoformat(row['created_at']) if row['created_at'] else None
        
        # Crear y retornar la etiqueta
        return Tag(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            color=row['color'],
            created_at=created_at,
            metadata=metadata
        )
    
    def close(self) -> None:
        """Cierra la conexión a la base de datos."""
        if self.connection:
            self.connection.close()
