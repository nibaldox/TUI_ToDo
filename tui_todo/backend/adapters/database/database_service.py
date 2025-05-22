#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Servicio de base de datos para la aplicación.

Este módulo proporciona un servicio para gestionar la conexión a la base de datos
y realizar operaciones comunes como inicialización y transacciones.
"""

import os
import sqlite3
from typing import Optional, Callable, Any


class DatabaseService:
    """
    Servicio para gestionar la conexión a la base de datos SQLite.
    
    Esta clase proporciona métodos para inicializar la base de datos,
    gestionar conexiones y ejecutar transacciones.
    
    Attributes:
        db_path: Ruta al archivo de base de datos SQLite
        connection: Conexión activa a la base de datos
    """
    
    def __init__(self, db_path: str):
        """
        Inicializa el servicio con la ruta a la base de datos.
        
        Args:
            db_path: Ruta al archivo de base de datos SQLite
        """
        self.db_path = db_path
        self.connection = None
        
        # Asegurar que el directorio existe
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
    
    def connect(self) -> sqlite3.Connection:
        """
        Establece una conexión a la base de datos.
        
        Returns:
            Conexión a la base de datos
        """
        if self.connection is None or self.connection.total_changes == -1: # Check if connection is closed
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        
        return self.connection
    
    def close(self) -> None:
        """Cierra la conexión a la base de datos."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def initialize_database(self) -> None:
        """
        Inicializa la estructura de la base de datos.
        
        Crea las tablas necesarias si no existen.
        """
        connection = self.connect()
        cursor = connection.cursor()
        
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
            tags TEXT,  -- JSON list of strings
            project_id TEXT,
            parent_id TEXT,
            metadata TEXT -- JSON object
        )
        ''')
        
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
            metadata TEXT -- JSON object
        )
        ''')
        
        # Tabla de etiquetas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            color TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT,
            metadata TEXT -- JSON object
        )
        ''')
        
        connection.commit()
    
    def execute_transaction(self, func: Callable[[sqlite3.Connection], Any]) -> Any:
        """
        Ejecuta una función dentro de una transacción.
        
        Args:
            func: Función a ejecutar con la conexión como parámetro
            
        Returns:
            El resultado de la función
        """
        connection = self.connect()
        
        try:
            result = func(connection)
            connection.commit()
            return result
        except Exception as e:
            connection.rollback()
            raise e
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Obtiene la conexión actual a la base de datos.
        
        Returns:
            Conexión a la base de datos
        """
        return self.connect()
    
    def create_backup(self, backup_path: Optional[str] = None) -> str:
        """
        Crea una copia de seguridad de la base de datos.
        
        Args:
            backup_path: Ruta donde guardar la copia de seguridad (opcional)
            
        Returns:
            Ruta a la copia de seguridad creada
        """
        if backup_path is None:
            # Generar nombre de archivo basado en la fecha actual
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = os.path.join(os.path.dirname(self.db_path), "backups")
            os.makedirs(backup_dir, exist_ok=True)
            backup_path = os.path.join(backup_dir, f"backup_{timestamp}.db")
        
        # Asegurar que la conexión está cerrada para evitar problemas
        # No es estrictamente necesario cerrar y reabrir para sqlite3.backup
        # pero si se hiciera copia manual, sí lo sería.
        # Para usar sqlite3.backup, necesitamos una conexión activa.
        
        source_conn = self.connect()
        backup_conn = sqlite3.connect(backup_path)
        
        try:
            with backup_conn:
                source_conn.backup(backup_conn)
        finally:
            backup_conn.close()
            # No cerramos la conexión principal (source_conn) aquí,
            # se gestiona a través de self.connect() y self.close()
            
        return backup_path

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
