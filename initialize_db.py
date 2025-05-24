#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para inicializar la base de datos y poblarla con datos de ejemplo.

Este script utiliza el DatabaseService para crear las tablas necesarias
y, opcionalmente, añade datos de ejemplo para facilitar el desarrollo y las pruebas.
"""

import os
import sys
from datetime import datetime, timedelta

# Añadir el directorio raíz del proyecto al PYTHONPATH
# Esto permite importar módulos del proyecto como tui_todo.backend, etc.
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from tui_todo.backend.adapters.database.database_service import DatabaseService
from tui_todo.backend.core.entities.task import Task, TaskStatus, TaskPriority
from tui_todo.backend.core.entities.project import Project
from tui_todo.backend.core.entities.tag import Tag
from tui_todo.backend.adapters.repositories.sqlite_task_repository import SQLiteTaskRepository
from tui_todo.backend.adapters.repositories.sqlite_project_repository import SQLiteProjectRepository
from tui_todo.backend.adapters.repositories.sqlite_tag_repository import SQLiteTagRepository

# Configuración de la base de datos
DB_FILE = os.path.join(current_dir, "tui_todo_data", "todo.db")


def populate_sample_data(db_service: DatabaseService):
    """
    Puebla la base de datos con datos de ejemplo.
    
    Args:
        db_service: Instancia del DatabaseService
    """
    print("Poblando la base de datos con datos de ejemplo...")
    
    # Inicializar repositorios usando db_service
    task_repo = SQLiteTaskRepository(db_service=db_service)
    project_repo = SQLiteProjectRepository(db_service=db_service)
    tag_repo = SQLiteTagRepository(db_service=db_service)
    
    try:
        # Crear etiquetas de ejemplo
        tag_importante = tag_repo.save(Tag(name="importante", color="red"))
        tag_trabajo = tag_repo.save(Tag(name="trabajo", color="blue"))
        tag_personal = tag_repo.save(Tag(name="personal", color="green"))
        tag_urgente = tag_repo.save(Tag(name="urgente", color="orange"))
        
        # Crear proyectos de ejemplo
        proyecto_casa = project_repo.save(Project(name="Casa", description="Tareas del hogar"))
        proyecto_trabajo = project_repo.save(Project(name="Trabajo", description="Proyectos laborales"))
        subproyecto_cocina = project_repo.save(Project(name="Cocina", parent_id=proyecto_casa.id, color="yellow"))
        
        # Crear tareas de ejemplo
        task_repo.save(Task(
            title="Comprar leche", 
            description="Ir al supermercado a comprar leche desnatada.",
            priority=TaskPriority.HIGH, 
            tags=[tag_personal.name, tag_importante.name],
            project_id=proyecto_casa.id,
            due_date=datetime.now() + timedelta(days=2)
        ))
        
        task_repo.save(Task(
            title="Preparar presentación", 
            description="Terminar slides para la reunión del viernes.",
            status=TaskStatus.IN_PROGRESS, 
            priority=TaskPriority.URGENT, 
            tags=[tag_trabajo.name, tag_urgente.name],
            project_id=proyecto_trabajo.id,
            due_date=datetime.now() + timedelta(days=3)
        ))
        
        task_repo.save(Task(
            title="Llamar al fontanero", 
            description="El grifo de la cocina gotea.",
            status=TaskStatus.PENDING, 
            priority=TaskPriority.MEDIUM, 
            tags=[tag_personal.name, tag_importante.name],
            project_id=subproyecto_cocina.id,
            due_date=datetime.now() + timedelta(days=1)
        ))
        
        task_repo.save(Task(
            title="Leer documentación de Textual", 
            description="Investigar sobre widgets avanzados.",
            status=TaskStatus.PENDING, 
            priority=TaskPriority.LOW, 
            tags=[tag_trabajo.name],
            project_id=proyecto_trabajo.id
        ))
        
        task_repo.save(Task(
            title="Hacer ejercicio", 
            description="Salir a correr 30 minutos.",
            status=TaskStatus.COMPLETED, 
            priority=TaskPriority.MEDIUM, 
            tags=[tag_personal.name],
            completed_at=datetime.now() - timedelta(days=1)
        ))
        
        print("Datos de ejemplo creados exitosamente.")
        
    except Exception as e:
        print(f"Error al poblar la base de datos: {e}")


def main():
    """
    Función principal del script.
    """
    print(f"Inicializando la base de datos en: {DB_FILE}")
    
    # Crear el directorio para la base de datos si no existe
    db_dir = os.path.dirname(DB_FILE)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f"Directorio '{db_dir}' creado.")
    
    # Inicializar el servicio de base de datos
    db_service = DatabaseService(db_path=DB_FILE)
    
    try:
        # Inicializar las tablas
        db_service.initialize_database()
        print("Tablas de la base de datos inicializadas (o ya existían).")
        
        # Preguntar al usuario si desea poblar con datos de ejemplo
        populate = input("¿Desea poblar la base de datos con datos de ejemplo? (s/N): ").lower()
        if populate == 's':
            populate_sample_data(db_service)
        else:
            print("La base de datos no se poblará con datos de ejemplo.")
            
    except Exception as e:
        print(f"Ocurrió un error durante la inicialización: {e}")
    finally:
        db_service.close()
        print("Proceso de inicialización finalizado.")


if __name__ == "__main__":
    main()
