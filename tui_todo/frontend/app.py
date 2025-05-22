#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo principal de la interfaz de usuario para TUI ToDo.

Este módulo contiene la clase principal de la aplicación que integra
todos los componentes de la interfaz de usuario y se comunica con el backend.
"""

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Header, Footer

# En el futuro, importaremos los widgets personalizados desde sus respectivos módulos
# from .widgets.calendar_widget import CalendarWidget
# from .widgets.sidebar_widget import Sidebar
# from .widgets.task_list_widget import TaskListWidget


class TodoApp(App):
    """Aplicación principal de TUI ToDo."""

    # Configuración de la aplicación
    CSS_PATH = "styles/textual_terminal_tui.tcss"
    TITLE = "TUI ToDo - Gestión Avanzada de Tareas"
    
    # Atajos de teclado
    BINDINGS = [
        ("q", "quit", "Salir"),
        ("ctrl+h", "toggle_help", "Ayuda"),
        ("ctrl+t", "toggle_theme", "Cambiar Tema"),
    ]

    def compose(self) -> ComposeResult:
        """Compone la interfaz de usuario principal."""
        # Encabezado con reloj
        yield Header(show_clock=True)
        
        # Contenedor principal con layout horizontal
        with Horizontal(id="main_container"):
            # Panel izquierdo (sidebar)
            with Vertical(id="left_panel"):
                # Aquí irán el calendario y la navegación
                # yield CalendarWidget(id="calendar")
                # yield Sidebar(id="sidebar")
                yield Container(id="placeholder_sidebar", classes="placeholder")
            
            # Panel derecho (contenido principal)
            with Vertical(id="right_panel"):
                # Aquí irá la lista de tareas y detalles
                # yield TaskListWidget(id="task_list")
                yield Container(id="placeholder_content", classes="placeholder")
        
        # Pie de página con atajos
        yield Footer()

    def on_mount(self) -> None:
        """Se ejecuta cuando la aplicación se monta."""
        # Aquí se inicializarán los datos y se cargarán las configuraciones
        self.log("Aplicación TUI ToDo iniciada")
        
    def action_toggle_help(self) -> None:
        """Muestra/oculta la ayuda."""
        # En el futuro, implementaremos un diálogo de ayuda
        self.log("Ayuda solicitada")
        
    def action_toggle_theme(self) -> None:
        """Cambia entre temas claro y oscuro."""
        # En el futuro, implementaremos cambio de temas
        self.log("Cambio de tema solicitado")


# Si se ejecuta este archivo directamente
if __name__ == "__main__":
    app = TodoApp()
    app.run()
