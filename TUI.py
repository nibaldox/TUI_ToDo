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


# --- Custom Widgets ---

class CalendarWidget(Static):
    """Un widget simple para mostrar un calendario."""

    def on_mount(self) -> None:
        self.update_calendar()

    def get_month_calendar(self, year, month):
        """Genera una representación textual simple del calendario del mes."""
        cal_str = f"[b]{datetime(year, month, 1):%B %Y}[/b]\n"
        cal_str += "[u]LUN MAR MIE JUE VIE SAB DOM[/u]\n"

        first_day_of_month = datetime(year, month, 1)
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
            cal_str += f"{day_num: <3} "
            if (start_offset + day_num) % 7 == 0:
                cal_str += "\n"

        cal_str += "\n"
        # Placeholder para iconos de la imagen
        cal_str += "\n[b]Iconos:[/b]\n"
        cal_str += " [ ] Lista  [E] Editar  [Q] Buscar"
        return cal_str

    def update_calendar(self) -> None:
        # Usaremos Octubre 2022 como en la imagen
        # En una app real, esto sería dinámico
        year, month = 2022, 10
        calendar_text = self.get_month_calendar(year, month)
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
        yield tree

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
        else:
            content += f"Contenido para {selection_path}..."

        # Para colores y estilos más precisos, necesitaríamos Rich o CSS de Textual.
        # Ejemplo de cómo se podría hacer con Rich tags (requiere parseo o un widget Markdown que lo soporte bien):
        # content_md = Markdown(content.replace("[!] Warning", "[yellow][!] Warning[/yellow]").replace("[X] Danger", "[red][X] Danger[/red]"))

        # Por ahora, usamos Static y aplicamos CSS a través de clases si es necesario
        self.mount(Static(content, classes="main-text-area"))


# --- App Principal ---
class TerminalApp(App):
    """Una aplicación de terminal basada en la imagen proporcionada."""

    CSS_PATH = "textual_terminal_tui.tcss" # Archivo CSS para estilos
    TITLE = "Theme Test App"

    BINDINGS = [
        Binding("q", "quit", "Salir"),
        Binding("ctrl+t", "toggle_theme_test", "Theme Test") # Para el checkbox
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


if __name__ == "__main__":
    app = TerminalApp()
    app.run()
