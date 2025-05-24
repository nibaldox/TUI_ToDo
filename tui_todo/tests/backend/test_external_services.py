import os
import csv
from datetime import datetime, timedelta
import pytest

from tui_todo.backend.frameworks.external.export_import_service import ExportImportService
from tui_todo.backend.frameworks.external.caldav_sync_service import CalDAVSyncService


def test_export_import_csv(tmp_path):
    # Configurar base de datos de prueba
    db1 = tmp_path / "db1.db"
    service1 = ExportImportService(str(db1))
    # Crear tareas de ejemplo
    t1 = service1.usecases.create_task(
        title="T1", description="Desc1", due_date=datetime.now(), tags=["a", "b"], project_id=None, parent_id=None
    )
    t2 = service1.usecases.create_task(
        title="T2", description=None, due_date=None, tags=[], project_id=None, parent_id=None
    )
    # Exportar a CSV
    csv_file = tmp_path / "tasks.csv"
    service1.export_to_csv(str(csv_file))
    assert csv_file.exists()
    # Importar en otra base de datos
    db2 = tmp_path / "db2.db"
    service2 = ExportImportService(str(db2))
    imported = service2.import_from_csv(str(csv_file))
    assert len(imported) == 2
    titles = {task["title"] for task in imported}
    assert "T1" in titles and "T2" in titles


def test_export_import_ical(tmp_path):
    db1 = tmp_path / "db1.db"
    service1 = ExportImportService(str(db1))
    # Crear tarea con due_date
    dt1 = datetime.now() + timedelta(days=1)
    service1.usecases.create_task(
        title="Evt", description=None, due_date=dt1, tags=None, project_id=None, parent_id=None
    )
    # Exportar a iCal
    ical_file = tmp_path / "tasks.ics"
    service1.export_to_ical(str(ical_file))
    assert ical_file.exists()
    content = ical_file.read_bytes()
    assert b"BEGIN:VCALENDAR" in content
    # Importar en otra base de datos
    db2 = tmp_path / "db2.db"
    service2 = ExportImportService(str(db2))
    imported = service2.import_from_ical(str(ical_file))
    assert len(imported) == 1
    assert imported[0]["title"] == "Evt"


def test_caldav_sync_service_empty():
    svc = CalDAVSyncService("url", "user", "pass")
    svc.calendars = []  # Simular sin calendarios
    events = svc.fetch_events(datetime.now(), datetime.now())
    assert events == []


def test_caldav_sync_service_with_event():
    # Simulación de calendario y evento
    class FakeVEvent:
        def __init__(self, summary, dtstart, dtend):
            self.summary = type("X", (), {"value": summary})
            self.dtstart = type("X", (), {"value": dtstart})
            self.dtend = type("X", (), {"value": dtend})

    class FakeResult:
        def __init__(self, summary, start, end):
            self.vobject_instance = type("Y", (), {"vevent": FakeVEvent(summary, start, end)})

    class FakeCalendar:
        def __init__(self, name):
            self.name = name

        def date_search(self, start, end):
            return [FakeResult("E1", start, end)]

    svc = CalDAVSyncService("url", "user", "pass")
    svc.calendars = [FakeCalendar("Cal1")]
    start = datetime(2025, 1, 1)
    end = datetime(2025, 1, 2)
    events = svc.fetch_events(start, end)
    assert len(events) == 1
    ev = events[0]
    assert ev["summary"] == "E1"
    assert ev["calendar"] == "Cal1"
    assert ev["start"] == start
