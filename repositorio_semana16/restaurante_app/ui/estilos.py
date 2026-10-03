"""Colores, estilos ttk y carga de imágenes de assets/ compartidos por todas las vistas."""
import os
import tkinter as tk
from tkinter import ttk

CARPETA_ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

COLOR_LATERAL = "#3b2a20"
COLOR_ACENTO = "#c8643b"
COLOR_ACENTO_OSCURO = "#a84f2b"
COLOR_FONDO = "#faf6f1"
COLOR_TARJETA = "#ffffff"
COLOR_TEXTO = "#2d2d2d"
COLOR_SUAVE = "#7a6a60"
COLOR_PELIGRO = "#b03a2e"
COLOR_OK = "#2e7d32"
FUENTE = "Segoe UI"


def cargar_imagen(nombre):
    """Devuelve un PhotoImage desde assets/ (o None si el archivo no existe)."""
    ruta = os.path.join(CARPETA_ASSETS, nombre)
    if not os.path.exists(ruta):
        return None
    return tk.PhotoImage(file=ruta)


def cargar_iconos():
    nombres = ["usuarios", "productos", "ventas", "registrar", "actualizar", "eliminar", "limpiar", "salir"]
    return {n: cargar_imagen(f"icono_{n}.png") for n in nombres}


def aplicar_estilos(root):
    estilo = ttk.Style(root)
    estilo.theme_use("clam")
    root.configure(bg=COLOR_FONDO)
    estilo.configure(".", font=(FUENTE, 10), background=COLOR_FONDO, foreground=COLOR_TEXTO)
    estilo.configure("Fondo.TFrame", background=COLOR_FONDO)
    estilo.configure("Tarjeta.TFrame", background=COLOR_TARJETA)
    estilo.configure("Lateral.TFrame", background=COLOR_LATERAL)
    estilo.configure("Tarjeta.TLabel", background=COLOR_TARJETA)
    estilo.configure("Titulo.TLabel", font=(FUENTE, 18, "bold"), background=COLOR_FONDO, foreground=COLOR_LATERAL)
    estilo.configure("Subtitulo.TLabel", font=(FUENTE, 10), background=COLOR_FONDO, foreground=COLOR_SUAVE)
    estilo.configure("Seccion.TLabel", font=(FUENTE, 12, "bold"), background=COLOR_TARJETA, foreground=COLOR_LATERAL)
    estilo.configure("Ayuda.TLabel", font=(FUENTE, 9, "italic"), background=COLOR_TARJETA, foreground=COLOR_SUAVE)
    estilo.configure("LateralTitulo.TLabel", font=(FUENTE, 12, "bold"), background=COLOR_LATERAL, foreground="white")
    estilo.configure("LateralInfo.TLabel", font=(FUENTE, 9), background=COLOR_LATERAL, foreground="#e4d5c9")
    estilo.configure("Estado.TLabel", font=(FUENTE, 10), background=COLOR_FONDO, foreground=COLOR_SUAVE)

    # Botones
    estilo.configure("Accion.TButton", background=COLOR_ACENTO, foreground="white", padding=(10, 6),
                     borderwidth=0, font=(FUENTE, 10, "bold"))
    estilo.map("Accion.TButton", background=[("active", COLOR_ACENTO_OSCURO), ("disabled", "#d8c3b8")])
    estilo.configure("Peligro.TButton", background=COLOR_PELIGRO, foreground="white", padding=(10, 6),
                     borderwidth=0, font=(FUENTE, 10, "bold"))
    estilo.map("Peligro.TButton", background=[("active", "#8e2e24"), ("disabled", "#d8c3b8")])
    estilo.configure("Neutro.TButton", background="#8c7b70", foreground="white", padding=(10, 6),
                     borderwidth=0, font=(FUENTE, 10, "bold"))
    estilo.map("Neutro.TButton", background=[("active", "#6f5f55"), ("disabled", "#d8c3b8")])
    estilo.configure("Menu.TButton", background=COLOR_LATERAL, foreground="white", padding=(14, 10),
                     borderwidth=0, anchor="w", font=(FUENTE, 11))
    estilo.map("Menu.TButton", background=[("active", "#5a4030")])
    estilo.configure("MenuActivo.TButton", background=COLOR_ACENTO, foreground="white", padding=(14, 10),
                     borderwidth=0, anchor="w", font=(FUENTE, 11, "bold"))

    # Entradas y combobox
    estilo.configure("TEntry", padding=5, fieldbackground="white")
    estilo.configure("TCombobox", padding=5, fieldbackground="white")

    # Tabla
    estilo.configure("Treeview", rowheight=28, font=(FUENTE, 10), background="white", fieldbackground="white")
    estilo.configure("Treeview.Heading", font=(FUENTE, 10, "bold"), background=COLOR_LATERAL,
                     foreground="white", padding=6)
    estilo.map("Treeview.Heading", background=[("active", COLOR_LATERAL)])
    estilo.map("Treeview", background=[("selected", COLOR_ACENTO)], foreground=[("selected", "white")])
