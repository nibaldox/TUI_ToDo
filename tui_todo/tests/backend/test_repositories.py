#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pruebas unitarias e integración para los repositorios SQLite.

Se valida la persistencia, recuperación, actualización y borrado de
Tareas, Proyectos y Etiquetas en la base de datos.
"""

import os
import unittest
from datetime import datetime, timedelta
from uuid import uuid4

from tui_todo.backend.core.entities.task import Task, TaskStatus, TaskPriority
from tui_todo.backend.core.entities.project import Project
from tui_todo.backend.core.entities.tag import Tag
from tui_todo.backend.adapters.repositories.sqlite_task_repository import SQLiteTaskRepository
from tui_todo.backend.adapters.repositories.sqlite_project_repository import SQLiteProjectRepository
from tui_todo.backend.adapters.repositories.sqlite_tag_repository import SQLiteTagRepository
from tui_todo.backend.adapters.database.database_service import DatabaseService

TEST_DB = "test_tui_todo.db"

class TestSQLiteRepositories(unittest.TestCase):
    """Pruebas para los repositorios SQLite de Task, Project y Tag."""
    
    def setUp(self):
        # Usar una base de datos temporal para pruebas
        self.db_path = TEST_DB
        self.db_service = DatabaseService(self.db_path)
        self.db_service.initialize_database()
        self.task_repo = SQLiteTaskRepository(self.db_path)
        self.project_repo = SQLiteProjectRepository(self.db_path)
        self.tag_repo = SQLiteTagRepository(self.db_path)

    def tearDown(self):
        # Cerrar conexiones y borrar la base de datos temporal
        self.task_repo.close()
        self.project_repo.close()
        self.tag_repo.close()
        self.db_service.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_crud_task(self):
        """CRUD básico para tareas."""
        task = Task(title="Tarea CRUD", description="Desc", priority=TaskPriority.HIGH)
        saved_task = self.task_repo.save(task)
        self.assertIsNotNone(saved_task.id)
        
        # Recuperar
        fetched = self.task_repo.get_by_id(saved_task.id)
        self.assertEqual(fetched.title, "Tarea CRUD")
        self.assertEqual(fetched.priority, TaskPriority.HIGH)
        
        # Actualizar
        fetched.title = "Tarea Actualizada"
        self.task_repo.save(fetched)
        updated = self.task_repo.get_by_id(fetched.id)
        self.assertEqual(updated.title, "Tarea Actualizada")
        
        # Eliminar
        self.task_repo.delete(updated.id)
        self.assertIsNone(self.task_repo.get_by_id(updated.id))

    def test_crud_project(self):
        """CRUD básico para proyectos."""
        project = Project(name="Proyecto CRUD", description="Proyecto test")
        saved_project = self.project_repo.save(project)
        self.assertIsNotNone(saved_project.id)
        
        # Recuperar
        fetched = self.project_repo.get_by_id(saved_project.id)
        self.assertEqual(fetched.name, "Proyecto CRUD")
        
        # Actualizar
        fetched.name = "Proyecto Actualizado"
        self.project_repo.save(fetched)
        updated = self.project_repo.get_by_id(fetched.id)
        self.assertEqual(updated.name, "Proyecto Actualizado")
        
        # Eliminar
        self.project_repo.delete(updated.id)
        self.assertIsNone(self.project_repo.get_by_id(updated.id))

    def test_crud_tag(self):
        """CRUD básico para etiquetas."""
        tag = Tag(name="importante", color="red")
        saved_tag = self.tag_repo.save(tag)
        self.assertIsNotNone(saved_tag.id)
        
        # Recuperar
        fetched = self.tag_repo.get_by_id(saved_tag.id)
        self.assertEqual(fetched.name, "importante")
        
        # Actualizar
        fetched.name = "urgente"
        self.tag_repo.save(fetched)
        updated = self.tag_repo.get_by_id(fetched.id)
        self.assertEqual(updated.name, "urgente")
        
        # Eliminar
        self.tag_repo.delete(updated.id)
        self.assertIsNone(self.tag_repo.get_by_id(updated.id))

    def test_task_filtering(self):
        """Filtrado de tareas por estado, proyecto y etiqueta."""
        # Crear proyectos y etiquetas
        project = self.project_repo.save(Project(name="Trabajo"))
        tag1 = self.tag_repo.save(Tag(name="importante", color="red"))
        tag2 = self.tag_repo.save(Tag(name="personal", color="blue"))
        # Crear tareas
        t1 = self.task_repo.save(Task(title="Tarea 1", status=TaskStatus.PENDING, project_id=project.id, tags=[tag1.name]))
        t2 = self.task_repo.save(Task(title="Tarea 2", status=TaskStatus.COMPLETED, project_id=project.id, tags=[tag2.name]))
        t3 = self.task_repo.save(Task(title="Tarea 3", status=TaskStatus.PENDING, project_id=None, tags=[tag1.name, tag2.name]))
        # Filtrar por estado
        pending = self.task_repo.get_by_status(TaskStatus.PENDING)
        self.assertGreaterEqual(len(pending), 2)
        # Filtrar por proyecto
        by_project = self.task_repo.get_by_project(project.id)
        self.assertEqual(len(by_project), 2)
        # Filtrar por etiqueta
        by_tag = self.task_repo.get_by_tag(tag1.name)
        self.assertGreaterEqual(len(by_tag), 2)

    def test_tag_count(self):
        """Contar etiquetas usadas en tareas."""
        tag1 = self.tag_repo.save(Tag(name="importante", color="red"))
        tag2 = self.tag_repo.save(Tag(name="personal", color="blue"))
        self.task_repo.save(Task(title="Tarea 1", tags=[tag1.name]))
        self.task_repo.save(Task(title="Tarea 2", tags=[tag1.name, tag2.name]))
        counts = self.tag_repo.get_all_with_count()
        tag1_count = next((c['count'] for c in counts if c['name'] == tag1.name), 0)
        tag2_count = next((c['count'] for c in counts if c['name'] == tag2.name), 0)
        self.assertEqual(tag1_count, 2)
        self.assertEqual(tag2_count, 1)


if __name__ == "__main__":
    unittest.main()
