"""Pantalla de inicio de sesión."""
import tkinter as tk
from tkinter import ttk

from . import estilos


class LoginView(ttk.Frame):
    def __init__(self, master, servicio, al_iniciar_sesion):
        super().__init__(master, style="Fondo.TFrame")
        self.servicio = servicio
        self.al_iniciar_sesion = al_iniciar_sesion
        self.logo = estilos.cargar_imagen("logo.png")  # se guarda en self para que Tk no lo libere

        tarjeta = ttk.Frame(self, style="Tarjeta.TFrame", padding=35)
        tarjeta.place(relx=0.5, rely=0.5, anchor="center")

        if self.logo:
            ttk.Label(tarjeta, image=self.logo, style="Tarjeta.TLabel").pack(pady=(0, 8))
        ttk.Label(tarjeta, text="Restaurante App", style="Seccion.TLabel", font=(estilos.FUENTE, 18, "bold")).pack()
        ttk.Label(tarjeta, text="Inicie sesión para continuar", style="Ayuda.TLabel").pack(pady=(0, 18))

        ttk.Label(tarjeta, text="Usuario", style="Tarjeta.TLabel").pack(anchor="w")
        self.entrada_usuario = ttk.Entry(tarjeta, width=30)
        self.entrada_usuario.pack(pady=(2, 10))
        ttk.Label(tarjeta, text="Contraseña", style="Tarjeta.TLabel").pack(anchor="w")
        self.entrada_clave = ttk.Entry(tarjeta, width=30, show="•")
        self.entrada_clave.pack(pady=(2, 14))

        ttk.Button(tarjeta, text="Ingresar", style="Accion.TButton", command=self.iniciar_sesion).pack(fill="x")
        self.mensaje = ttk.Label(tarjeta, text="", style="Ayuda.TLabel", foreground=estilos.COLOR_PELIGRO)
        self.mensaje.pack(pady=(10, 0))

        # Evento de teclado: Enter dentro de los campos también inicia sesión.
        for campo in (self.entrada_usuario, self.entrada_clave):
            campo.bind("<Return>", lambda evento: self.iniciar_sesion())
        self.entrada_usuario.focus_set()

    def iniciar_sesion(self):
        usuario = self.servicio.autenticar(self.entrada_usuario.get(), self.entrada_clave.get())
        if usuario is None:
            self.mensaje.config(text="Usuario o contraseña incorrectos.")
            self.entrada_clave.delete(0, "end")
            return
        self.al_iniciar_sesion(usuario)
