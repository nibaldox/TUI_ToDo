#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TUI ToDo - Sistema Avanzado de Gestión de Tareas en Terminal

Este es el punto de entrada principal para la aplicación TUI ToDo.
Inicializa los componentes necesarios y lanza la interfaz de usuario.
"""

import sys
import os

# Asegurar que el directorio raíz del proyecto esté en el path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from frontend.app import TodoApp


def main():
    """Función principal que inicia la aplicación."""
    try:
        # En el futuro, aquí se podrían procesar argumentos de línea de comandos
        app = TodoApp()
        app.run()
    except KeyboardInterrupt:
        print("\nAplicación cerrada por el usuario.")
        return 0
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
