#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pruebas unitarias para las entidades del core.

Este módulo contiene las pruebas para las clases Task, Project y Tag,
así como sus relaciones.
"""

import unittest
from datetime import datetime, timedelta
from uuid import uuid4

from tui_todo.backend.core.entities.task import Task, TaskStatus, TaskPriority
from tui_todo.backend.core.entities.project import Project
from tui_todo.backend.core.entities.tag import Tag
from tui_todo.backend.core.entities.relationships import ProjectHierarchy, TaskCollection


class TestTask(unittest.TestCase):
    """Pruebas para la clase Task."""
    
    def test_task_creation(self):
        """Prueba la creación básica de una tarea."""
        task = Task(title="Prueba de tarea")
        
        self.assertEqual(task.title, "Prueba de tarea")
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertEqual(task.priority, TaskPriority.MEDIUM)
        self.assertIsNotNone(task.id)
        self.assertIsNotNone(task.created_at)
        self.assertIsNone(task.description)
        self.assertIsNone(task.due_date)
        self.assertIsNone(task.completed_at)
        self.assertEqual(task.tags, [])
        self.assertIsNone(task.project_id)
        self.assertIsNone(task.parent_id)
        self.assertEqual(task.metadata, {})
    
    def test_task_complete(self):
        """Prueba marcar una tarea como completada."""
        task = Task(title="Tarea para completar")
        
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertIsNone(task.completed_at)
        
        task.complete()
        
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertIsNotNone(task.completed_at)
    
    def test_task_reopen(self):
        """Prueba reabrir una tarea completada."""
        task = Task(title="Tarea para reabrir")
        task.complete()
        
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertIsNotNone(task.completed_at)
        
        task.reopen()
        
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertIsNone(task.completed_at)
    
    def test_task_is_overdue(self):
        """Prueba la detección de tareas vencidas."""
        # Tarea con fecha de vencimiento en el pasado
        past_date = datetime.now() - timedelta(days=1)
        task_overdue = Task(title="Tarea vencida", due_date=past_date)
        
        # Tarea con fecha de vencimiento en el futuro
        future_date = datetime.now() + timedelta(days=1)
        task_not_overdue = Task(title="Tarea no vencida", due_date=future_date)
        
        # Tarea sin fecha de vencimiento
        task_no_due_date = Task(title="Tarea sin fecha")
        
        self.assertTrue(task_overdue.is_overdue())
        self.assertFalse(task_not_overdue.is_overdue())
        self.assertFalse(task_no_due_date.is_overdue())
    
    def test_task_tags(self):
        """Prueba la gestión de etiquetas en tareas."""
        task = Task(title="Tarea con etiquetas")
        
        self.assertEqual(task.tags, [])
        
        task.add_tag("importante")
        task.add_tag("trabajo")
        
        self.assertEqual(task.tags, ["importante", "trabajo"])
        
        # Añadir etiqueta duplicada
        task.add_tag("importante")
        self.assertEqual(task.tags, ["importante", "trabajo"])
        
        # Eliminar etiqueta
        task.remove_tag("importante")
        self.assertEqual(task.tags, ["trabajo"])
        
        # Eliminar etiqueta que no existe
        task.remove_tag("no-existe")
        self.assertEqual(task.tags, ["trabajo"])
    
    def test_task_to_dict(self):
        """Prueba la conversión de Task a diccionario."""
        task = Task(
            title="Tarea de prueba",
            description="Descripción de prueba",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            tags=["importante", "trabajo"],
            project_id="proyecto-1"
        )
        
        task_dict = task.to_dict()
        
        self.assertEqual(task_dict["title"], "Tarea de prueba")
        self.assertEqual(task_dict["description"], "Descripción de prueba")
        self.assertEqual(task_dict["status"], "in_progress")
        self.assertEqual(task_dict["priority"], "high")
        self.assertEqual(task_dict["tags"], ["importante", "trabajo"])
        self.assertEqual(task_dict["project_id"], "proyecto-1")
    
    def test_task_from_dict(self):
        """Prueba la creación de Task desde un diccionario."""
        task_id = str(uuid4())
        now = datetime.now()
        
        task_dict = {
            "id": task_id,
            "title": "Tarea desde diccionario",
            "description": "Descripción de prueba",
            "status": "important",
            "created_at": now.isoformat(),
            "priority": "urgent",
            "tags": ["prueba", "diccionario"],
            "project_id": "proyecto-test"
        }
        
        task = Task.from_dict(task_dict)
        
        self.assertEqual(task.id, task_id)
        self.assertEqual(task.title, "Tarea desde diccionario")
        self.assertEqual(task.description, "Descripción de prueba")
        self.assertEqual(task.status, TaskStatus.IMPORTANT)
        self.assertEqual(task.priority, TaskPriority.URGENT)
        self.assertEqual(task.tags, ["prueba", "diccionario"])
        self.assertEqual(task.project_id, "proyecto-test")


class TestProject(unittest.TestCase):
    """Pruebas para la clase Project."""
    
    def test_project_creation(self):
        """Prueba la creación básica de un proyecto."""
        project = Project(name="Proyecto de prueba")
        
        self.assertEqual(project.name, "Proyecto de prueba")
        self.assertIsNotNone(project.id)
        self.assertIsNotNone(project.created_at)
        self.assertIsNone(project.description)
        self.assertEqual(project.color, "blue")
        self.assertIsNone(project.parent_id)
        self.assertEqual(project.metadata, {})
    
    def test_project_is_root(self):
        """Prueba la detección de proyectos raíz."""
        root_project = Project(name="Proyecto raíz")
        child_project = Project(name="Proyecto hijo", parent_id="proyecto-padre")
        
        self.assertTrue(root_project.is_root())
        self.assertFalse(child_project.is_root())
    
    def test_project_update_metadata(self):
        """Prueba la actualización de metadatos de un proyecto."""
        project = Project(name="Proyecto con metadatos")
        
        self.assertEqual(project.metadata, {})
        
        project.update_metadata("orden", 1)
        project.update_metadata("visible", True)
        
        self.assertEqual(project.metadata, {"orden": 1, "visible": True})
        
        # Sobrescribir un valor existente
        project.update_metadata("orden", 2)
        self.assertEqual(project.metadata, {"orden": 2, "visible": True})
    
    def test_project_to_dict(self):
        """Prueba la conversión de Project a diccionario."""
        project = Project(
            name="Proyecto de prueba",
            description="Descripción de prueba",
            color="red",
            parent_id="proyecto-padre"
        )
        
        project_dict = project.to_dict()
        
        self.assertEqual(project_dict["name"], "Proyecto de prueba")
        self.assertEqual(project_dict["description"], "Descripción de prueba")
        self.assertEqual(project_dict["color"], "red")
        self.assertEqual(project_dict["parent_id"], "proyecto-padre")
    
    def test_project_from_dict(self):
        """Prueba la creación de Project desde un diccionario."""
        project_id = str(uuid4())
        now = datetime.now()
        
        project_dict = {
            "id": project_id,
            "name": "Proyecto desde diccionario",
            "description": "Descripción de prueba",
            "color": "green",
            "created_at": now.isoformat(),
            "parent_id": "proyecto-padre",
            "metadata": {"orden": 3}
        }
        
        project = Project.from_dict(project_dict)
        
        self.assertEqual(project.id, project_id)
        self.assertEqual(project.name, "Proyecto desde diccionario")
        self.assertEqual(project.description, "Descripción de prueba")
        self.assertEqual(project.color, "green")
        self.assertEqual(project.parent_id, "proyecto-padre")
        self.assertEqual(project.metadata, {"orden": 3})


class TestTag(unittest.TestCase):
    """Pruebas para la clase Tag."""
    
    def test_tag_creation(self):
        """Prueba la creación básica de una etiqueta."""
        tag = Tag(name="etiqueta-prueba")
        
        self.assertEqual(tag.name, "etiqueta-prueba")
        self.assertIsNotNone(tag.id)
        self.assertIsNotNone(tag.created_at)
        self.assertIsNone(tag.description)
        self.assertEqual(tag.color, "gray")
        self.assertEqual(tag.metadata, {})
    
    def test_tag_to_dict(self):
        """Prueba la conversión de Tag a diccionario."""
        tag = Tag(
            name="etiqueta-prueba",
            description="Descripción de prueba",
            color="yellow"
        )
        
        tag_dict = tag.to_dict()
        
        self.assertEqual(tag_dict["name"], "etiqueta-prueba")
        self.assertEqual(tag_dict["description"], "Descripción de prueba")
        self.assertEqual(tag_dict["color"], "yellow")
    
    def test_tag_from_dict(self):
        """Prueba la creación de Tag desde un diccionario."""
        tag_id = str(uuid4())
        now = datetime.now()
        
        tag_dict = {
            "id": tag_id,
            "name": "etiqueta-diccionario",
            "description": "Descripción de prueba",
            "color": "purple",
            "created_at": now.isoformat(),
            "metadata": {"prioridad": "alta"}
        }
        
        tag = Tag.from_dict(tag_dict)
        
        self.assertEqual(tag.id, tag_id)
        self.assertEqual(tag.name, "etiqueta-diccionario")
        self.assertEqual(tag.description, "Descripción de prueba")
        self.assertEqual(tag.color, "purple")
        self.assertEqual(tag.metadata, {"prioridad": "alta"})


class TestRelationships(unittest.TestCase):
    """Pruebas para las relaciones entre entidades."""
    
    def test_project_hierarchy(self):
        """Prueba la jerarquía de proyectos."""
        # Crear proyectos
        root1 = Project(name="Raíz 1", id="root1")
        root2 = Project(name="Raíz 2", id="root2")
        child1 = Project(name="Hijo 1", id="child1", parent_id="root1")
        child2 = Project(name="Hijo 2", id="child2", parent_id="root1")
        grandchild = Project(name="Nieto", id="grandchild", parent_id="child1")
        
        # Crear jerarquía
        hierarchy = ProjectHierarchy()
        hierarchy.add_project(root1)
        hierarchy.add_project(root2)
        hierarchy.add_project(child1)
        hierarchy.add_project(child2)
        hierarchy.add_project(grandchild)
        
        # Verificar raíces
        self.assertEqual(set(hierarchy.root_projects), {"root1", "root2"})
        
        # Verificar hijos
        children = hierarchy.get_children("root1")
        self.assertEqual(len(children), 2)
        self.assertEqual({child.id for child in children}, {"child1", "child2"})
        
        # Verificar descendientes
        descendants = hierarchy.get_all_descendants("root1")
        self.assertEqual(len(descendants), 3)
        self.assertEqual({desc.id for desc in descendants}, {"child1", "child2", "grandchild"})
        
        # Verificar ruta
        path = hierarchy.get_path("grandchild")
        self.assertEqual(len(path), 3)
        self.assertEqual([p.id for p in path], ["root1", "child1", "grandchild"])
    
    def test_task_collection(self):
        """Prueba la colección de tareas."""
        # Crear tareas
        task1 = Task(title="Tarea 1", id="task1", project_id="project1", tags=["importante", "trabajo"])
        task2 = Task(title="Tarea 2", id="task2", project_id="project1", tags=["personal"])
        task3 = Task(title="Tarea 3", id="task3", project_id="project2", tags=["importante"])
        task4 = Task(title="Tarea 4", id="task4", status=TaskStatus.COMPLETED)
        
        # Crear colección
        collection = TaskCollection()
        collection.add_task(task1)
        collection.add_task(task2)
        collection.add_task(task3)
        collection.add_task(task4)
        
        # Verificar tareas por proyecto
        project1_tasks = collection.get_by_project("project1")
        self.assertEqual(len(project1_tasks), 2)
        self.assertEqual({task.id for task in project1_tasks}, {"task1", "task2"})
        
        # Verificar tareas por etiqueta
        important_tasks = collection.get_by_tag("importante")
        self.assertEqual(len(important_tasks), 2)
        self.assertEqual({task.id for task in important_tasks}, {"task1", "task3"})
        
        # Verificar tareas por estado
        completed_tasks = collection.get_by_status("completed")
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(completed_tasks[0].id, "task4")
        
        # Verificar eliminación de tarea
        collection.remove_task("task1")
        self.assertEqual(len(collection.tasks), 3)
        self.assertNotIn("task1", collection.tasks)
        
        # Verificar que se actualizaron las relaciones
        project1_tasks_after = collection.get_by_project("project1")
        self.assertEqual(len(project1_tasks_after), 1)
        self.assertEqual(project1_tasks_after[0].id, "task2")
        
        important_tasks_after = collection.get_by_tag("importante")
        self.assertEqual(len(important_tasks_after), 1)
        self.assertEqual(important_tasks_after[0].id, "task3")


if __name__ == "__main__":
    unittest.main()
