"""Sección de Usuarios: formulario + Treeview con manejo de eventos.

Flujo: interacción del usuario → evento → bind() → callback → servicio → persistencia → respuesta visual.
La vista solo captura eventos y actualiza widgets; validaciones y JSON viven en RestauranteServicio.
"""
import tkinter as tk
from tkinter import ttk, messagebox

from modelos import ROLES_GESTIONABLES, ROL_EMPLEADO, ROL_CLIENTE
from servicios import ValidacionError
from . import estilos

DESCRIPCION_ROL = {
    ROL_EMPLEADO: "Empleado: personal del restaurante que atiende productos y ventas.",
    ROL_CLIENTE: "Cliente: persona registrada que consume en el restaurante.",
}


class UsuariosView(ttk.Frame):
    def __init__(self, master, servicio, usuario_sesion, iconos):
        super().__init__(master, style="Fondo.TFrame", padding=20)
        self.servicio = servicio
        self.usuario_sesion = usuario_sesion
        self.iconos = iconos
        self.id_seleccionado = None  # id del usuario cargado en el formulario (None = formulario vacío)

        ttk.Label(self, text="Gestión de usuarios", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(self, text="Registre, consulte, actualice o elimine empleados y clientes.",
                  style="Subtitulo.TLabel").pack(anchor="w", pady=(0, 12))

        cuerpo = ttk.Frame(self, style="Fondo.TFrame")
        cuerpo.pack(fill="both", expand=True)
        self._construir_formulario(cuerpo)
        self._construir_tabla(cuerpo)

        self.estado = ttk.Label(self, text="", style="Estado.TLabel")
        self.estado.pack(anchor="w", pady=(8, 0))

        self._vincular_eventos()
        self.refrescar_tabla()
        self.limpiar()

    # ------------------------------------------------------------ construcción de la interfaz
    def _construir_formulario(self, padre):
        tarjeta = ttk.Frame(padre, style="Tarjeta.TFrame", padding=18)
        tarjeta.pack(side="left", fill="y", padx=(0, 16))
        ttk.Label(tarjeta, text="Datos del usuario", style="Seccion.TLabel").pack(anchor="w", pady=(0, 10))

        self.var_nombre = tk.StringVar()
        self.var_usuario = tk.StringVar()
        self.var_clave = tk.StringVar()
        self.var_rol = tk.StringVar()

        self.entrada_nombre = self._campo(tarjeta, "Nombre completo", self.var_nombre)
        self.entrada_usuario = self._campo(tarjeta, "Usuario", self.var_usuario)
        self.entrada_clave = self._campo(tarjeta, "Contraseña", self.var_clave, oculto=True)
        self.ayuda_clave = ttk.Label(tarjeta, text="", style="Ayuda.TLabel")
        self.ayuda_clave.pack(anchor="w")

        ttk.Label(tarjeta, text="Rol", style="Tarjeta.TLabel").pack(anchor="w", pady=(8, 0))
        self.combo_rol = ttk.Combobox(tarjeta, textvariable=self.var_rol, values=ROLES_GESTIONABLES,
                                      state="readonly", width=24)
        self.combo_rol.pack(fill="x", pady=(2, 2))
        self.ayuda_rol = ttk.Label(tarjeta, text="", style="Ayuda.TLabel", wraplength=230, justify="left")
        self.ayuda_rol.pack(anchor="w", pady=(0, 12))

        # Botones asociados con command= (a diferencia de los eventos de teclado y tabla, que usan bind()).
        marco = ttk.Frame(tarjeta, style="Tarjeta.TFrame")
        marco.pack(fill="x")
        self.btn_registrar = ttk.Button(marco, text=" Registrar", image=self.iconos["registrar"], compound="left",
                                        style="Accion.TButton", command=self.registrar)
        self.btn_actualizar = ttk.Button(marco, text=" Actualizar", image=self.iconos["actualizar"], compound="left",
                                         style="Accion.TButton", command=self.actualizar)
        self.btn_eliminar = ttk.Button(marco, text=" Eliminar", image=self.iconos["eliminar"], compound="left",
                                       style="Peligro.TButton", command=self.eliminar)
        self.btn_limpiar = ttk.Button(marco, text=" Limpiar", image=self.iconos["limpiar"], compound="left",
                                      style="Neutro.TButton", command=self.limpiar)
        for i, boton in enumerate((self.btn_registrar, self.btn_actualizar, self.btn_eliminar, self.btn_limpiar)):
            boton.grid(row=i // 2, column=i % 2, sticky="ew", padx=3, pady=3)
        marco.columnconfigure((0, 1), weight=1)

        ttk.Label(tarjeta, text="Atajos: Enter = registrar · Esc = limpiar", style="Ayuda.TLabel").pack(
            anchor="w", pady=(10, 0))

    def _campo(self, padre, etiqueta, variable, oculto=False):
        ttk.Label(padre, text=etiqueta, style="Tarjeta.TLabel").pack(anchor="w", pady=(8, 0))
        entrada = ttk.Entry(padre, textvariable=variable, width=24, show="•" if oculto else "")
        entrada.pack(fill="x", pady=(2, 0))
        return entrada

    def _construir_tabla(self, padre):
        tarjeta = ttk.Frame(padre, style="Tarjeta.TFrame", padding=12)
        tarjeta.pack(side="left", fill="both", expand=True)
        ttk.Label(tarjeta, text="Usuarios registrados", style="Seccion.TLabel").pack(anchor="w", pady=(0, 8))

        columnas = ("id", "nombre", "usuario", "rol")  # la contraseña NO se muestra en la tabla
        self.tabla = ttk.Treeview(tarjeta, columns=columnas, show="headings", selectmode="browse")
        for col, texto, ancho in (("id", "ID", 50), ("nombre", "Nombre", 140), ("usuario", "Usuario", 90),
                                  ("rol", "Rol", 110)):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho, minwidth=50, anchor="w", stretch=True)
        barra = ttk.Scrollbar(tarjeta, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")  # primero la barra, para que la tabla se ajuste al espacio restante
        self.tabla.pack(side="left", fill="both", expand=True)

    # ------------------------------------------------------------ eventos (bind)
    def _vincular_eventos(self):
        # Selección de fila: evento virtual de ttk.
        self.tabla.bind("<<TreeviewSelect>>", self.al_seleccionar_fila)
        # Cambio de opción en el Combobox: evento virtual de ttk.
        self.combo_rol.bind("<<ComboboxSelected>>", self.al_cambiar_rol)
        # Atajos de teclado en los controles del formulario y en la tabla.
        for widget in (self.entrada_nombre, self.entrada_usuario, self.entrada_clave, self.combo_rol):
            widget.bind("<Return>", self.al_presionar_enter)
        for widget in (self.entrada_nombre, self.entrada_usuario, self.entrada_clave, self.combo_rol, self.tabla):
            widget.bind("<Escape>", self.al_presionar_escape)

    # ------------------------------------------------------------ callbacks (solo coordinan)
    def al_seleccionar_fila(self, evento=None):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        id_usuario = seleccion[0]  # el iid de la fila es el id; no se guarda nada sensible en la tabla
        usuario = self.servicio.obtener_usuario(id_usuario)
        if usuario is None:
            self.refrescar_tabla()
            return
        self.id_seleccionado = usuario.id
        self.var_nombre.set(usuario.nombre)
        self.var_usuario.set(usuario.usuario)
        self.var_clave.set("")
        self.var_rol.set(usuario.rol)
        self.ayuda_clave.config(text="Deje vacío para conservar la contraseña actual.")
        self.ayuda_rol.config(text=DESCRIPCION_ROL.get(usuario.rol, "Cuenta administrativa (solo lectura)."))
        self._actualizar_botones(usuario)
        self._mostrar_estado(f"Usuario «{usuario.usuario}» cargado en el formulario.")

    def al_cambiar_rol(self, evento=None):
        rol = self.var_rol.get()
        self.ayuda_rol.config(text=DESCRIPCION_ROL.get(rol, ""))
        self._mostrar_estado(f"Rol seleccionado: {rol}.")

    def al_presionar_enter(self, evento=None):
        self.registrar()  # reutiliza el mismo método del botón Registrar; no se repite la lógica
        return "break"

    def al_presionar_escape(self, evento=None):
        self.limpiar()
        return "break"

    # ------------------------------------------------------------ acciones (usadas por botones y atajos)
    def registrar(self):
        try:
            nuevo = self.servicio.registrar_usuario(self.var_nombre.get(), self.var_usuario.get(),
                                                    self.var_clave.get(), self.var_rol.get())
        except ValidacionError as error:
            messagebox.showwarning("Registro no válido", str(error), parent=self)
            return
        self.refrescar_tabla()
        self.limpiar()
        self._mostrar_estado(f"Usuario «{nuevo.usuario}» registrado como {nuevo.rol}.", ok=True)

    def actualizar(self):
        if self.id_seleccionado is None:
            messagebox.showinfo("Actualizar", "Seleccione primero un usuario de la tabla.", parent=self)
            return
        try:
            usuario = self.servicio.actualizar_usuario(self.id_seleccionado, self.var_nombre.get(),
                                                       self.var_usuario.get(), self.var_clave.get(),
                                                       self.var_rol.get())
        except ValidacionError as error:
            messagebox.showwarning("Actualización no válida", str(error), parent=self)
            return
        self.refrescar_tabla()
        self.limpiar()
        self._mostrar_estado(f"Usuario «{usuario.usuario}» actualizado.", ok=True)

    def eliminar(self):
        if self.id_seleccionado is None:
            messagebox.showinfo("Eliminar", "Seleccione primero un usuario de la tabla.", parent=self)
            return
        usuario = self.servicio.obtener_usuario(self.id_seleccionado)
        nombre = usuario.usuario if usuario else self.id_seleccionado
        if not messagebox.askyesno("Confirmar eliminación",
                                   f"¿Desea eliminar al usuario «{nombre}»?\nEsta acción no se puede deshacer.",
                                   parent=self):
            return
        try:
            self.servicio.eliminar_usuario(self.id_seleccionado, self.usuario_sesion.id)
        except ValidacionError as error:
            messagebox.showwarning("No se pudo eliminar", str(error), parent=self)
            return
        self.refrescar_tabla()
        self.limpiar()
        self._mostrar_estado(f"Usuario «{nombre}» eliminado.", ok=True)

    def limpiar(self):
        """Estado inicial: formulario vacío, sin fila seleccionada y botones acordes."""
        self.id_seleccionado = None
        self.tabla.selection_remove(self.tabla.selection())
        for variable in (self.var_nombre, self.var_usuario, self.var_clave):
            variable.set("")
        self.var_rol.set(ROL_EMPLEADO)
        self.ayuda_clave.config(text="")
        self.ayuda_rol.config(text=DESCRIPCION_ROL[ROL_EMPLEADO])
        self._actualizar_botones(None)
        self._mostrar_estado("Formulario listo para un nuevo usuario.")
        self.entrada_nombre.focus_set()

    # ------------------------------------------------------------ auxiliares de la vista
    def refrescar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        for u in self.servicio.listar_usuarios():
            self.tabla.insert("", "end", iid=u.id, values=(u.id, u.nombre, u.usuario, u.rol))

    def _actualizar_botones(self, usuario):
        editable = usuario is not None and not usuario.es_administrador
        self.btn_actualizar.state(["!disabled"] if editable else ["disabled"])
        self.btn_eliminar.state(["!disabled"] if editable else ["disabled"])
        self.btn_registrar.state(["!disabled"])

    def _mostrar_estado(self, texto, ok=False):
        self.estado.config(text=texto, foreground=estilos.COLOR_OK if ok else estilos.COLOR_SUAVE)
