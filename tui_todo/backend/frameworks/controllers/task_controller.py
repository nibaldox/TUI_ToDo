"""
Controlador de tareas para la capa de presentación.
"""
from tui_todo.backend.adapters.repositories.sqlite_task_repository import SQLiteTaskRepository
from tui_todo.backend.core.use_cases.task_use_cases import TaskUseCases


class TaskController:
    """Controlador que orquesta los casos de uso de tareas para la UI."""

    def __init__(self, db_file: str):
        """Inicializa repositorio y casos de uso."""
        repo = SQLiteTaskRepository(db_file)
        self.usecases = TaskUseCases(repo)

    def list_all(self) -> list:
        """Retorna todas las tareas como diccionarios."""
        tasks = self.usecases.get_all_tasks()
        return [t.to_dict() for t in tasks]

    def get(self, task_id: str) -> dict:
        """Obtiene una tarea por ID y retorna su diccionario."""
        task = self.usecases.get_task(task_id)
        return task.to_dict() if task else None

    def create(self, title: str, description: str, due_date=None) -> dict:
        """Crea una tarea y retorna su diccionario."""
        task = self.usecases.create_task(title, description, due_date)
        return task.to_dict()

    def update(self, task_id: str, title: str, description: str, due_date=None) -> dict:
        """Actualiza una tarea existente y retorna su diccionario."""
        task = self.usecases.update_task(task_id, title=title, description=description, due_date=due_date)
        return task.to_dict() if task else None

    def delete(self, task_id: str) -> bool:
        """Elimina una tarea por su ID."""
        return self.usecases.delete_task(task_id)
