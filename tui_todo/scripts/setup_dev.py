#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de configuración inicial para el entorno de desarrollo de TUI ToDo.

Este script prepara el entorno de desarrollo, crea directorios necesarios,
inicializa la base de datos y configura archivos de ejemplo.
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path

# Asegurar que el directorio raíz del proyecto esté en el path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))


def setup_directories():
    """Crea directorios necesarios para el funcionamiento de la aplicación."""
    print("Configurando directorios de datos...")
    
    # Directorio para datos de usuario
    data_dir = Path.home() / ".tui_todo"
    data_dir.mkdir(exist_ok=True)
    
    # Directorios para almacenamiento de datos
    (data_dir / "db").mkdir(exist_ok=True)
    (data_dir / "backups").mkdir(exist_ok=True)
    (data_dir / "exports").mkdir(exist_ok=True)
    
    print(f"Directorios creados en: {data_dir}")
    return data_dir


def create_sample_data(data_dir):
    """Crea datos de ejemplo para pruebas."""
    print("Creando datos de ejemplo...")
    
    # Ejemplo de proyectos
    projects = [
        {"id": 1, "name": "Personal", "description": "Tareas personales", "color": "blue", "parent_id": None},
        {"id": 2, "name": "Trabajo", "description": "Tareas laborales", "color": "green", "parent_id": None},
        {"id": 3, "name": "Proyecto X", "description": "Proyecto especial", "color": "purple", "parent_id": 2},
    ]
    
    # Ejemplo de tareas
    tasks = [
        {
            "id": 1, 
            "title": "Comprar víveres", 
            "description": "Ir al supermercado a comprar víveres", 
            "status": "pending", 
            "created_at": "2025-05-22T09:00:00", 
            "due_date": "2025-05-23T18:00:00", 
            "priority": "medium", 
            "tags": ["compras", "hogar"], 
            "project_id": 1
        },
        {
            "id": 2, 
            "title": "Preparar presentación", 
            "description": "Preparar presentación para la reunión", 
            "status": "in_progress", 
            "created_at": "2025-05-22T10:00:00", 
            "due_date": "2025-05-24T14:00:00", 
            "priority": "high", 
            "tags": ["reunión", "presentación"], 
            "project_id": 2
        },
        {
            "id": 3, 
            "title": "Investigar API", 
            "description": "Investigar API para integración", 
            "status": "pending", 
            "created_at": "2025-05-22T11:00:00", 
            "due_date": "2025-05-25T17:00:00", 
            "priority": "medium", 
            "tags": ["desarrollo", "investigación"], 
            "project_id": 3
        },
    ]
    
    # Guardar datos en archivos JSON
    with open(data_dir / "db" / "projects.json", "w", encoding="utf-8") as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)
    
    with open(data_dir / "db" / "tasks.json", "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
    
    print("Datos de ejemplo creados correctamente.")


def setup_config(data_dir):
    """Crea archivo de configuración inicial."""
    print("Creando configuración inicial...")
    
    config = {
        "app": {
            "name": "TUI ToDo",
            "version": "0.1.0",
            "theme": "dark"
        },
        "storage": {
            "type": "json",  # Opciones: json, sqlite
            "path": str(data_dir / "db")
        },
        "ui": {
            "show_calendar": True,
            "default_view": "tasks",
            "date_format": "%Y-%m-%d"
        }
    }
    
    with open(data_dir / "config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("Configuración inicial creada.")


def main():
    """Función principal del script de configuración."""
    parser = argparse.ArgumentParser(description="Configuración del entorno de desarrollo para TUI ToDo")
    parser.add_argument("--with-examples", action="store_true", help="Crear datos de ejemplo")
    args = parser.parse_args()
    
    print("=== Configuración del entorno de desarrollo de TUI ToDo ===")
    
    try:
        # Crear directorios
        data_dir = setup_directories()
        
        # Crear configuración
        setup_config(data_dir)
        
        # Crear datos de ejemplo si se solicita
        if args.with_examples:
            create_sample_data(data_dir)
        
        print("\n¡Configuración completada con éxito!")
        print(f"Directorio de datos: {data_dir}")
        print("\nPara ejecutar la aplicación:")
        print("  python main.py")
        
        return 0
    except Exception as e:
        print(f"Error durante la configuración: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
