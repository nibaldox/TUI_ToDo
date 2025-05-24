"""Servicio para sincronización con servidores CalDAV."""

try:
    from caldav import DAVClient
except ImportError:
    DAVClient = None  # type: ignore

from datetime import datetime
from typing import List, Dict, Any
from ...core.entities.task import Task
try:
    from icalendar import Event
except ImportError:
    Event = None  # type: ignore


class CalDAVSyncService:
    """Sincronización bidireccional de eventos CalDAV."""

    def __init__(self, url: str, username: str, password: str):
        """Inicializa el cliente CalDAV con credenciales. Si no está instalado, no hace nada."""
        if DAVClient is None:
            self.client = None  # type: ignore
            self.principal = None  # type: ignore
            self.calendars: List[Any] = []
            return
        self.client = DAVClient(url, username=username, password=password)
        self.principal = self.client.principal()
        self.calendars = self.principal.calendars()

    def fetch_events(self, start: datetime, end: datetime) -> List[Dict[str, Any]]:
        """
        Obtiene eventos entre las fechas especificadas.

        Args:
            start: Fecha y hora de inicio.
            end: Fecha y hora de fin.

        Returns:
            Lista de diccionarios con campos básicos de los eventos.
        """
        events: List[Dict[str, Any]] = []
        for calendar in self.calendars:
            # Buscar eventos en el rango de fechas
            for result in calendar.date_search(start=start, end=end):
                vevent = result.vobject_instance.vevent  # objeto vEvent
                summary = getattr(vevent.summary, 'value', '')
                dtstart = getattr(vevent.dtstart, 'value', None)
                dtend = getattr(vevent.dtend, 'value', None)
                events.append({
                    'calendar': calendar.name if hasattr(calendar, 'name') else None,
                    'summary': summary,
                    'start': dtstart,
                    'end': dtend,
                })
        return events

    def fetch_remote_changes(self, start: datetime, end: datetime) -> List[Dict[str, Any]]:
        """
        Obtiene eventos nuevos o actualizados en el servidor CalDAV dentro del rango.

        Devuelve lista de diccionarios con: uid, summary, start, end, etag, last_modified
        """
        changes: List[Dict[str, Any]] = []
        for calendar in self.calendars:
            for result in calendar.date_search(start=start, end=end):
                vevent = result.vobject_instance.vevent
                uid = getattr(vevent.uid, 'value', None)
                summary = getattr(vevent.summary, 'value', '')
                dtstart = getattr(vevent.dtstart, 'value', None)
                dtend = getattr(vevent.dtend, 'value', None)
                etag = getattr(result, 'etag', None)
                last_mod = getattr(vevent.lastmodified, 'value', None)
                changes.append({
                    'uid': uid,
                    'summary': summary,
                    'start': dtstart,
                    'end': dtend,
                    'etag': etag,
                    'last_modified': last_mod,
                })
        return changes

    def push_local_changes(self, tasks: List[Task]) -> None:
        """
        Envía cambios locales al servidor CalDAV.

        Crea o actualiza eventos según etag y last_modified de las tareas.
        """
        if DAVClient is None or Event is None:
            return
        for calendar in self.calendars:
            for task in tasks:
                if not task.due_date:
                    continue
                try:
                    event = calendar.event_by_uid(task.id)
                except Exception:
                    event = None
                if event:
                    vevent = event.vobject_instance.vevent
                    remote_mod = getattr(vevent.lastmodified, 'value', None)
                    if task.last_modified and (remote_mod is None or task.last_modified > remote_mod):
                        vevent.summary.value = task.title
                        vevent.dtstart.value = task.due_date
                        vevent.dtstamp.value = datetime.now()
                        event.save()
                else:
                    new_event = Event()
                    new_event.add('uid', task.id)
                    new_event.add('summary', task.title)
                    new_event.add('dtstart', task.due_date)
                    new_event.add('dtstamp', datetime.now())
                    # crear evento en el calendario
                    calendar.add_event(new_event.to_ical())

    def sync_bidirectional(self, start: datetime, end: datetime, tasks: List[Task]) -> Dict[str, Any]:
        """
        Sincroniza cambios entre el servidor CalDAV y la base local.

        1) Obtiene cambios remotos (fetch_remote_changes)
        2) Envía cambios locales (push_local_changes)

        Retorna resumen con listas de cambios aplicados.
        """
        remote = self.fetch_remote_changes(start, end)
        self.push_local_changes(tasks)
        # Detectar eliminaciones remotas comparando UIDs
        local_ids = {t.id for t in tasks}
        remote_uids = {c['uid'] for c in remote if c.get('uid') is not None}
        deleted = list(local_ids - remote_uids)
        return {'remote_changes': remote, 'remote_deleted': deleted}
