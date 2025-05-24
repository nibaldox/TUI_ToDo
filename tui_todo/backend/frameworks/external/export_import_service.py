"""
Servicio para exportar e importar tareas en formatos CSV e iCal.
"""
import csv
from datetime import datetime
from typing import List, Dict

from tui_todo.backend.adapters.repositories.sqlite_task_repository import SQLiteTaskRepository
from tui_todo.backend.core.use_cases.task_use_cases import TaskUseCases

try:
    from icalendar import Calendar, Event
except ImportError:
    Calendar = None  # type: ignore
    Event = None  # type: ignore


class ExportImportService:
    """Servicio para exportar e importar tareas en CSV e iCal."""

    def __init__(self, db_file: str):
        """Inicializa el servicio con la ruta de la base de datos."""
        repo = SQLiteTaskRepository(db_file)
        self.usecases = TaskUseCases(repo)

    def export_to_csv(self, file_path: str) -> None:
        """Exporta todas las tareas a un archivo CSV."""
        tasks = self.usecases.get_all_tasks()
        fieldnames = [
            'id', 'title', 'description', 'status',
            'due_date', 'priority', 'tags',
            'project_id', 'parent_id'
        ]
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for task in tasks:
                # Preparar datos para CSV
                data = task.to_dict()
                # Serializar fecha de vencimiento
                data['due_date'] = task.due_date.isoformat() if task.due_date else ''
                # Serializar etiquetas
                data['tags'] = ','.join(task.tags or [])
                writer.writerow({k: data.get(k, '') for k in fieldnames})

    def import_from_csv(self, file_path: str) -> List[Dict]:
        """Importa tareas desde un archivo CSV y las crea en la base de datos."""
        imported = []
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                due = datetime.fromisoformat(row['due_date']) if row.get('due_date') else None
                tags = row['tags'].split(',') if row.get('tags') else []
                created = self.usecases.create_task(
                    title=row['title'],
                    description=row.get('description'),
                    due_date=due,
                    tags=tags,
                    project_id=row.get('project_id'),
                    parent_id=row.get('parent_id')
                )
                imported.append(created.to_dict())
        return imported

    def export_to_ical(self, file_path: str) -> None:
        """Exporta tareas con fecha de vencimiento a un archivo iCal."""
        tasks = self.usecases.get_all_tasks()
        if Calendar is not None:
            cal = Calendar()
            for task in tasks:
                if not task.due_date:
                    continue
                event = Event()
                event.add('uid', task.id)
                event.add('summary', task.title)
                event.add('dtstart', task.due_date)
                event.add('dtstamp', datetime.now())
                cal.add_component(event)
            with open(file_path, 'wb') as f:
                f.write(cal.to_ical())
        else:
            # Fallback: generar ICS manualmente
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//TUI ToDo//EN\n")
                for task in tasks:
                    f.write("BEGIN:VEVENT\n")
                    f.write(f"UID:{task.id}\n")
                    f.write(f"SUMMARY:{task.title}\n")
                    if task.due_date:
                        f.write(f"DTSTART:{task.due_date.isoformat()}\n")
                    f.write("END:VEVENT\n")
                f.write("END:VCALENDAR\n")

    def import_from_ical(self, file_path: str) -> List[Dict]:
        """Importa tareas desde un archivo iCal y las crea en la base de datos."""
        imported = []
        if Calendar is not None:
            with open(file_path, 'rb') as f:
                cal = Calendar.from_ical(f.read())
                for comp in cal.walk():
                    if comp.name == 'VEVENT':
                        summary = str(comp.get('summary'))
                        dtstart = comp.get('dtstart').dt
                        created = self.usecases.create_task(
                            title=summary,
                            description=None,
                            due_date=dtstart
                        )
                        imported.append(created.to_dict())
        else:
            # Fallback: parse ICS manualmente
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            event_data = {}
            for line in lines:
                line = line.strip()
                if line == 'BEGIN:VEVENT':
                    event_data = {}
                elif line.startswith('SUMMARY:'):
                    event_data['summary'] = line[len('SUMMARY:'):]
                elif line == 'END:VEVENT':
                    summary = event_data.get('summary', '')
                    created = self.usecases.create_task(
                        title=summary,
                        description=None,
                        due_date=None
                    )
                    imported.append(created.to_dict())
        return imported
