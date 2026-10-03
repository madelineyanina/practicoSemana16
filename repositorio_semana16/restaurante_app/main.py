"""Punto de entrada de restaurante_app (Semana 16: manejo de eventos en la gestión de usuarios)."""
import os
import tkinter as tk

from servicios import ArchivoServicio, RestauranteServicio
from ui import LoginView, MainView
from ui import estilos

CARPETA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")


class Aplicacion:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Restaurante App")
        self.root.geometry("1100x640")
        self.root.minsize(1000, 600)
        estilos.aplicar_estilos(self.root)
        self.servicio = RestauranteServicio(ArchivoServicio(CARPETA_DATOS))
        self.vista = None
        self.mostrar_login()

    def _cambiar_vista(self, vista):
        if self.vista is not None:
            self.vista.destroy()
        self.vista = vista
        self.vista.pack(fill="both", expand=True)

    def mostrar_login(self):
        self._cambiar_vista(LoginView(self.root, self.servicio, self.mostrar_principal))

    def mostrar_principal(self, usuario):
        self._cambiar_vista(MainView(self.root, self.servicio, usuario, self.mostrar_login))

    def ejecutar(self):
        self.root.mainloop()


if __name__ == "__main__":
    Aplicacion().ejecutar()
