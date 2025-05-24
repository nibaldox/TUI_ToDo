from datetime import datetime, timedelta

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.css.query import DOMQuery
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import (
    Header,
    Footer,
    Static,
    Label,
    Button,
    Tree,
    Markdown,
    Checkbox,
    Input
)
from textual.binding import Binding
from textual import events
from initialize_db import DB_FILE  # nueva importación del path de la DB
from tui_todo.backend.frameworks.controllers.task_controller import TaskController  # controlador de tareas
import os
import holidays
from tui_todo.backend.frameworks.external.export_import_service import ExportImportService
from tui_todo.backend.frameworks.external.caldav_sync_service import CalDAVSyncService

CALDAV_URL = os.getenv("CALDAV_URL", "")
CALDAV_USER = os.getenv("CALDAV_USER", "")
CALDAV_PASS = os.getenv("CALDAV_PASS", "")

# --- Custom Widgets ---

class CalendarWidget(Static):
    """Un widget simple para mostrar un calendario."""

    def __init__(self, *args, **kwargs):
        # Permitir rich markup para resaltar feriados
        kwargs.setdefault('markup', True)
        super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        # Inicializar mes actual y mostrar calendario
        today = datetime.today()
        self.year, self.month = today.year, today.month
        self.update_calendar()

    def on_key(self, event: events.Key) -> None:
        # Navegar entre meses con flechas izquierda/derecha
        if event.key == "left":
            self.month -= 1
            if self.month < 1:
                self.month = 12
                self.year -= 1
        elif event.key == "right":
            self.month += 1
            if self.month > 12:
                self.month = 1
                self.year += 1
        else:
            return
        self.update_calendar()

    def get_month_calendar(self, year, month):
        """Genera una representación textual simple del calendario del mes."""
        # Obtener feriados de Chile para el año
        try:
            cl_holidays = holidays.CountryHoliday('CL', years=[year])
        except Exception:
            cl_holidays = {}
        cal_str = f"{datetime(year, month, 1):%B %Y}\n"
        cal_str += "LUN MAR MIE JUE VIE SAB DOM\n"

        first_day_of_month = datetime(year, month, 1)
        # Obtener tareas del mes para marcar días
        controller = TaskController(DB_FILE)
        tasks = controller.list_all()
        due_days = set()
        for t in tasks:
            due_str = t.get('due_date')
            if due_str:
                try:
                    dt_due = datetime.fromisoformat(due_str)
                except ValueError:
                    continue
                if dt_due.year == year and dt_due.month == month:
                    due_days.add(dt_due.day)
        # weekday() devuelve 0 para lunes, 6 para domingo
        start_offset = first_day_of_month.weekday()
        cal_str += "    " * start_offset

        current_day = first_day_of_month
        # Corrección para el cálculo de días del mes
        if month == 12:
            days_in_month = (datetime(year + 1, 1, 1) - datetime(year, month, 1)).days
        else:
            days_in_month = (datetime(year, month + 1, 1) - datetime(year, month, 1)).days

        # Corrección del bucle del calendario
        for day_num in range(1, days_in_month + 1):
            date_obj = datetime(year, month, day_num).date()
            if date_obj in cl_holidays:
                # resaltar feriado en rojo
                cal_str += f"[red]{day_num:>2}[/red] "
            elif day_num in due_days:
                # marcar día con tarea con asterisco
                cal_str += f"{day_num:>2}* "
            else:
                cal_str += f"{day_num:>3} "
            if (start_offset + day_num) % 7 == 0:
                cal_str += "\n"

        cal_str += "\n"
        # Placeholder para iconos de la imagen
        cal_str += "\nIconos:\n"
        cal_str += " ( ) Lista  (E) Editar  (Q) Buscar"
        return cal_str

    def update_calendar(self) -> None:
        # Mostrar calendario para mes actual
        calendar_text = self.get_month_calendar(self.year, self.month)
        self.update(calendar_text)


class Sidebar(Vertical):
    """Barra lateral con navegación."""

    def compose(self) -> ComposeResult:
        # Usaremos un Tree widget para la navegación, como en la imagen
        tree: Tree[dict] = Tree("Navegación")
        tree.root.expand()

        # Añadir nodos basados en la imagen
        the_aether = tree.root.add("TheAether", data={"path": "theaether"})
        meta = the_aether.add("00 Meta", data={"path": "meta"})
        meta.add_leaf("00 Meta", data={"path": "meta/meta"}) # Sub-item
        meta.add_leaf("01 Periodics", data={"path": "meta/periodics"})
        meta.add_leaf("02 Templates", data={"path": "meta/templates"})
        meta.add_leaf("03 Objects", data={"path": "meta/objects"})
        meta.add_leaf("04 Projects", data={"path": "meta/projects"})
        tickets = meta.add("05 Tickets", data={"path": "meta/tickets"})
        tickets.add_leaf("> deferred", data={"path": "meta/tickets/deferred"})
        meta.add_leaf("06 Ideas", data={"path": "meta/ideas"})

        the_aether.add("10 Life", data={"path": "life"})
        the_aether.add("20 IT", data={"path": "it"})
        the_aether.add("30 Hobbies", data={"path": "hobbies"})
        the_aether.add("50 Dev0 Systems", data={"path": "devsystems"})
        the_aether.add("Unsorted", data={"path": "unsorted"})
        tree.root.add_leaf("Tareas", data={"path": "tasks"})  # nodo para listar tareas
        yield tree

class TaskDetail(Static):
    """Muestra detalles de una tarea seleccionada."""
    def __init__(self, task: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task = task

    def on_mount(self) -> None:
        content = (
            f"**Título:** {self.task.get('title')}\n"
            f"**Descripción:** {self.task.get('description') or ''}\n"
            f"**Estado:** {self.task.get('status')}\n"
            f"**Prioridad:** {self.task.get('priority')}\n"
            f"**Fecha vencimiento:** {self.task.get('due_date')}\n"
        )
        self.update(content)
        # Botones para editar y eliminar
        self.mount(Button("Editar", id=f"edit_task_{self.task['id']}"))
        self.mount(Button("Eliminar", id=f"delete_task_{self.task['id']}"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button.id
        controller = TaskController(DB_FILE)
        if btn.startswith("edit_task_"):
            # abrir formulario de edición
            self.parent.mount(TaskEditForm(self.task, id="task_edit_form"))
            self.remove()
            return
        if btn.startswith("delete_task_"):
            def cb(confirm: bool):
                if confirm:
                    TaskController(DB_FILE).delete(self.task['id'])
                self.parent.mount(TaskList(id="task_list"))
            self.parent.mount(ConfirmDialog("Confirmar eliminación?", cb, id="confirm_dialog"))
            self.remove()
            return

class TaskList(Widget):
    def compose(self) -> ComposeResult:
        yield Button(label="Nueva tarea", id="new_task")
        controller = TaskController(DB_FILE)
        self.tasks = controller.list_all()
        for t in self.tasks:
            yield Button(label=t.get('title', '<sin título>'), id=str(t.get('id')))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "new_task":
            # abrir formulario de creación
            self.parent.mount(TaskForm(id="task_form"))
            self.remove()
            return
        task_id = event.button.id
        detail = TaskDetail(TaskController(DB_FILE).get(task_id), id='task_detail')
        # Reemplazar TaskList por detalle
        self.parent.mount(detail)
        self.remove()

class TaskForm(Static):
    """Formulario modal para crear una nueva tarea."""
    def compose(self) -> ComposeResult:
        self.controller = TaskController(DB_FILE)
        yield Label("Crear Tarea", id="form_title")
        yield Input(placeholder="Título", id="title_input")
        yield Input(placeholder="Descripción", id="description_input")
        yield Input(placeholder="Fecha vencimiento (YYYY-MM-DD)", id="due_date_input")
        yield Button("Guardar", id="save_task")
        yield Button("Cancelar", id="cancel_task")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        parent = self.parent
        if event.button.id == "save_task":
            title = self.query_one(Input, id="title_input").value.strip()
            if not title:
                for lbl in self.query(Label, classes="error"):
                    lbl.remove()
                self.mount(Label("Error: Título obligatorio", classes="error"))
                return
            due_str = self.query_one(Input, id="due_date_input").value
            try:
                due = datetime.fromisoformat(due_str) if due_str else None
            except ValueError:
                for lbl in self.query(Label, classes="error"):
                    lbl.remove()
                self.mount(Label("Error: Fecha inválida", classes="error"))
                return
            desc = self.query_one(Input, id="description_input").value
            self.controller.create(title, desc, due)
        # Volver a la lista de tareas
        parent.mount(TaskList(id="task_list"))
        self.remove()

class TaskEditForm(Static):
    """Formulario modal para editar una tarea existente."""
    def __init__(self, task: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task = task
        self.controller = TaskController(DB_FILE)

    def compose(self) -> ComposeResult:
        yield Label("Editar Tarea", id="form_title")
        yield Input(value=self.task.get('title', ''), id="title_input")
        yield Input(value=self.task.get('description', ''), id="description_input")
        due_str = self.task.get('due_date').isoformat() if self.task.get('due_date') else ''
        yield Input(value=due_str, id="due_date_input")
        yield Button("Guardar", id="save_edit")
        yield Button("Cancelar", id="cancel_edit")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        parent = self.parent
        if event.button.id == "save_edit":
            title = self.query_one(Input, id="title_input").value.strip()
            if not title:
                for lbl in self.query(Label, classes="error"):
                    lbl.remove()
                self.mount(Label("Error: Título obligatorio", classes="error"))
                return
            due_str = self.query_one(Input, id="due_date_input").value
            try:
                due = datetime.fromisoformat(due_str) if due_str else None
            except ValueError:
                for lbl in self.query(Label, classes="error"):
                    lbl.remove()
                self.mount(Label("Error: Fecha inválida", classes="error"))
                return
            desc = self.query_one(Input, id="description_input").value
            self.controller.update(self.task['id'], title, desc, due)
        # volver a lista de tareas
        parent.mount(TaskList(id="task_list"))
        self.remove()

class ConfirmDialog(Static):
    """Diálogo para confirmar acciones."""
    def __init__(self, message: str, on_confirm: callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message
        self.on_confirm = on_confirm

    def compose(self) -> ComposeResult:
        yield Label(self.message)
        yield Button("Sí", id="confirm_yes")
        yield Button("No", id="confirm_no")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        result = event.button.id == "confirm_yes"
        self.on_confirm(result)
        self.remove()

class MainContent(Container):
    """Área de contenido principal."""
    current_selection = reactive("Inicio")

    def watch_current_selection(self, new_selection: str) -> None:
        """Se llama cuando current_selection cambia."""
        self.update_content(new_selection)

    def on_mount(self) -> None:
        self.update_content(self.current_selection)

    def update_content(self, selection_path: str) -> None:
        """Actualiza el contenido basado en la selección."""
        # Limpiar contenido anterior
        self.query("Static, Markdown").remove()

        # Contenido de ejemplo basado en la imagen (simplificado)
        # Usaremos Markdown para facilitar el formato
        content = f"# {selection_path.split('/')[-1].replace('-', ' ').title()}\n\n"

        if "meta" in selection_path or selection_path == "Inicio": # Contenido por defecto
            content += "## Quote\n> blocks\n\n"
            content += "## Info\n"
            content += "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip.\n\n"
            content += "## Alertas\n"
            # Usar Rich markup en lugar de HTML
            content += "[yellow][!] Warning[/yellow]\n\n"
            content += "[red][X] Danger[/red]\n\n"

            content += "## Enlaces\n"
            content += "* Unresolved link\n"
            content += "* Internal Link\n"
            content += "* External Link\n\n"

            content += "## Estados\n"
            content += "* [ ] open\n"
            content += "* [x] complete\n" # Usar Rich tags para el check
            content += "* [!] Important\n"
            content += "* [>] deferred\n"
            content += "* [?] question\n"
            content += "* [i] info\n"
            content += "* [-] canceled\n"
            content += "* [p] partial\n"
        elif selection_path == "tasks":  # mostrar lista de tareas
            self.mount(TaskList(id="task_list"))
            return
        else:
            content += f"Contenido para {selection_path}..."

        # Para colores y estilos más precisos, necesitaríamos Rich o CSS de Textual.
        # Ejemplo de cómo se podría hacer con Rich tags (requiere parseo o un widget Markdown que lo soporte bien):
        # content_md = Markdown(content.replace("[!] Warning", "[yellow][!] Warning[/yellow]").replace("[X] Danger", "[red][X] Danger[/red]"))

        # Por ahora, usamos Static y aplicamos CSS a través de clases si es necesario
        self.mount(Static(content, markup=False, classes="main-text-area"))

# --- App Principal ---
class TerminalApp(App):
    """Una aplicación de terminal basada en la imagen proporcionada."""

    CSS_PATH = "textual_terminal_tui.tcss" # Archivo CSS para estilos
    TITLE = "Theme Test App"

    BINDINGS = [
        Binding("q", "quit", "Salir"),
        Binding("ctrl+t", "toggle_theme_test", "Theme Test"), # Para el checkbox
        Binding("n", "new_task", "Nueva tarea"),
        Binding("e", "edit_task", "Editar tarea seleccionada"),
        Binding("d", "delete_task", "Eliminar tarea seleccionada"),
        Binding("s", "sync_caldav", "Sincronizar CalDAV"),
        Binding("b", "sync_bidirectional", "Sincronizar bidireccional CalDAV"),
        Binding("x", "export_csv", "Exportar CSV"),
        Binding("i", "import_csv", "Importar CSV"),
        Binding("c", "export_ical", "Exportar iCal"),
        Binding("k", "import_ical", "Importar iCal"),
    ]

    theme_test_checked = reactive(False)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main_app_container"):
            with Vertical(id="left_panel"):
                yield Checkbox("Theme Test", self.theme_test_checked, id="theme_test_checkbox")
                yield CalendarWidget(id="calendar")
                yield Sidebar(id="sidebar")
            yield MainContent(id="main_content")
        yield Footer()

    def on_mount(self) -> None:
        """Se llama cuando la app se monta."""
        self.query_one("#theme_test_checkbox", Checkbox).value = self.theme_test_checked


    def on_tree_node_selected(self, event: Tree.NodeSelected[dict]) -> None:
        """Maneja la selección de un nodo en el árbol de la barra lateral."""
        node_data = event.node.data
        if node_data:
            path = node_data.get("path", "Desconocido")
            main_content_area = self.query_one(MainContent)
            main_content_area.current_selection = path # Esto activará watch_current_selection

    def action_toggle_theme_test(self) -> None:
        """Alterna el estado del checkbox 'Theme Test'."""
        checkbox = self.query_one("#theme_test_checkbox", Checkbox)
        checkbox.toggle()
        self.theme_test_checked = checkbox.value
        # Podrías añadir lógica aquí para cambiar el tema de la app si es necesario

    def action_new_task(self) -> None:
        """Atajo: abrir formulario para nueva tarea."""
        main = self.query_one(MainContent)
        main.mount(TaskForm(id="task_form"))

    def action_edit_task(self) -> None:
        """Atajo: editar tarea seleccionada en MainContent."""
        detail = self.query_one(TaskDetail, allow_none=True)
        if detail:
            detail.post_message(Button.Pressed(detail.query_one(Button, id=lambda i: i.startswith("edit_task_"))))

    def action_delete_task(self) -> None:
        """Atajo: borrar tarea seleccionada en MainContent."""
        detail = self.query_one(TaskDetail, allow_none=True)
        if detail:
            def cb(confirm: bool):
                if confirm:
                    TaskController(DB_FILE).delete(detail.task['id'])
                self.query_one(MainContent).mount(TaskList(id="task_list"))
            self.query_one(MainContent).mount(ConfirmDialog("Confirmar eliminación?", cb, id="confirm_dialog"))
            detail.remove()
            return

    def action_sync_caldav(self) -> None:
        """Atajo: sincronizar eventos CalDAV."""
        service = CalDAVSyncService(CALDAV_URL, CALDAV_USER, CALDAV_PASS)
        start = datetime.today()
        end = start + timedelta(days=1)
        events = service.fetch_events(start, end)
        entries = [f"{e['start']}: {e['summary']}" for e in events]
        content = '\n'.join(entries) if entries else 'No events found'
        main = self.query_one(MainContent)
        main.mount(Static(content, markup=False, classes='caldav-events'))

    def action_sync_bidirectional(self) -> None:
        """Atajo: sincronización bidireccional CalDAV."""
        service = CalDAVSyncService(CALDAV_URL, CALDAV_USER, CALDAV_PASS)
        # Obtener tareas locales como objetos Task
        from tui_todo.backend.frameworks.controllers.task_controller import TaskController
        ctrl = TaskController(DB_FILE)
        tasks = ctrl.usecases.get_all_tasks()
        start = datetime.today()
        end = start + timedelta(days=1)
        result = service.sync_bidirectional(start, end, tasks)
        entries = [f"{e['uid']}: {e['summary']}" for e in result.get('remote_changes', [])]
        content = '\n'.join(entries) if entries else 'No remote changes'
        main = self.query_one(MainContent)
        main.mount(Static(content, markup=False, classes='caldav-sync'))

    def action_export_csv(self) -> None:
        service = ExportImportService(DB_FILE)
        service.export_to_csv('export.csv')
        self.log('Exported tasks to export.csv')

    def action_import_csv(self) -> None:
        service = ExportImportService(DB_FILE)
        imported = service.import_from_csv('export.csv')
        self.log(f'Imported {len(imported)} tasks from export.csv')

    def action_export_ical(self) -> None:
        service = ExportImportService(DB_FILE)
        service.export_to_ical('export.ics')
        self.log('Exported tasks to export.ics')

    def action_import_ical(self) -> None:
        service = ExportImportService(DB_FILE)
        imported = service.import_from_ical('export.ics')
        self.log(f'Imported {len(imported)} tasks from export.ics')


if __name__ == "__main__":
    app = TerminalApp()
    app.run()
