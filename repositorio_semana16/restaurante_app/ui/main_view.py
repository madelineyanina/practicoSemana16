"""Ventana principal: menú lateral, navegación entre secciones y control de acceso por rol."""
import tkinter as tk
from tkinter import ttk, messagebox

from servicios import ValidacionError
from . import estilos
from .usuarios_view import UsuariosView


class ProductosView(ttk.Frame):
    """Sección de Productos (menú del restaurante)."""

    def __init__(self, master, servicio, iconos):
        super().__init__(master, style="Fondo.TFrame", padding=20)
        self.servicio = servicio
        ttk.Label(self, text="Productos", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(self, text="Menú disponible del restaurante.", style="Subtitulo.TLabel").pack(anchor="w", pady=(0, 12))

        cuerpo = ttk.Frame(self, style="Fondo.TFrame")
        cuerpo.pack(fill="both", expand=True)
        form = ttk.Frame(cuerpo, style="Tarjeta.TFrame", padding=18)
        form.pack(side="left", fill="y", padx=(0, 16))
        ttk.Label(form, text="Nuevo producto", style="Seccion.TLabel").pack(anchor="w", pady=(0, 6))
        self.var_nombre, self.var_precio, self.var_stock = tk.StringVar(), tk.StringVar(), tk.StringVar()
        for texto, var in (("Nombre", self.var_nombre), ("Precio ($)", self.var_precio), ("Stock", self.var_stock)):
            ttk.Label(form, text=texto, style="Tarjeta.TLabel").pack(anchor="w", pady=(8, 0))
            ttk.Entry(form, textvariable=var, width=28).pack(pady=(2, 0))
        ttk.Button(form, text=" Registrar", image=iconos["registrar"], compound="left", style="Accion.TButton",
                   command=self.registrar).pack(fill="x", pady=(14, 4))
        ttk.Button(form, text=" Eliminar", image=iconos["eliminar"], compound="left", style="Peligro.TButton",
                   command=self.eliminar).pack(fill="x")

        tarjeta = ttk.Frame(cuerpo, style="Tarjeta.TFrame", padding=12)
        tarjeta.pack(side="left", fill="both", expand=True)
        self.tabla = ttk.Treeview(tarjeta, columns=("id", "nombre", "precio", "stock"), show="headings",
                                  selectmode="browse")
        for col, texto, ancho in (("id", "ID", 70), ("nombre", "Producto", 220), ("precio", "Precio", 90),
                                  ("stock", "Stock", 80)):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho)
        self.tabla.pack(fill="both", expand=True)
        self.refrescar()

    def refrescar(self):
        self.tabla.delete(*self.tabla.get_children())
        for p in self.servicio.listar_productos():
            self.tabla.insert("", "end", iid=p.id, values=(p.id, p.nombre, f"${p.precio:.2f}", p.stock))

    def registrar(self):
        try:
            self.servicio.registrar_producto(self.var_nombre.get(), self.var_precio.get(), self.var_stock.get())
        except ValidacionError as error:
            messagebox.showwarning("Producto no válido", str(error), parent=self)
            return
        for var in (self.var_nombre, self.var_precio, self.var_stock):
            var.set("")
        self.refrescar()

    def eliminar(self):
        seleccion = self.tabla.selection()
        if seleccion and messagebox.askyesno("Confirmar", "¿Eliminar el producto seleccionado?", parent=self):
            self.servicio.eliminar_producto(seleccion[0])
            self.refrescar()


class VentasView(ttk.Frame):
    """Sección de Ventas."""

    def __init__(self, master, servicio, usuario_sesion, iconos):
        super().__init__(master, style="Fondo.TFrame", padding=20)
        self.servicio, self.usuario_sesion = servicio, usuario_sesion
        ttk.Label(self, text="Ventas", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(self, text="Registre ventas y consulte el historial.", style="Subtitulo.TLabel").pack(anchor="w", pady=(0, 12))

        cuerpo = ttk.Frame(self, style="Fondo.TFrame")
        cuerpo.pack(fill="both", expand=True)
        form = ttk.Frame(cuerpo, style="Tarjeta.TFrame", padding=18)
        form.pack(side="left", fill="y", padx=(0, 16))
        ttk.Label(form, text="Nueva venta", style="Seccion.TLabel").pack(anchor="w", pady=(0, 6))
        ttk.Label(form, text="Producto", style="Tarjeta.TLabel").pack(anchor="w", pady=(8, 0))
        self.var_producto, self.var_cantidad = tk.StringVar(), tk.StringVar(value="1")
        self.combo = ttk.Combobox(form, textvariable=self.var_producto, state="readonly", width=26)
        self.combo.pack(pady=(2, 0))
        ttk.Label(form, text="Cantidad", style="Tarjeta.TLabel").pack(anchor="w", pady=(8, 0))
        ttk.Entry(form, textvariable=self.var_cantidad, width=28).pack(pady=(2, 0))
        ttk.Button(form, text=" Registrar venta", image=iconos["registrar"], compound="left", style="Accion.TButton",
                   command=self.registrar).pack(fill="x", pady=(14, 0))

        tarjeta = ttk.Frame(cuerpo, style="Tarjeta.TFrame", padding=12)
        tarjeta.pack(side="left", fill="both", expand=True)
        cols = ("id", "fecha", "producto", "cantidad", "total", "vendedor")
        self.tabla = ttk.Treeview(tarjeta, columns=cols, show="headings", selectmode="browse")
        for col, texto, ancho in (("id", "ID", 60), ("fecha", "Fecha", 130), ("producto", "Producto", 150),
                                  ("cantidad", "Cant.", 55), ("total", "Total", 80), ("vendedor", "Vendedor", 110)):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho)
        self.tabla.pack(fill="both", expand=True)
        self.refrescar()

    def refrescar(self):
        self._mapa = {f"{p.nombre} (stock {p.stock})": p.id for p in self.servicio.listar_productos()}
        self.combo["values"] = list(self._mapa)
        self.tabla.delete(*self.tabla.get_children())
        for v in self.servicio.listar_ventas():
            self.tabla.insert("", "end", iid=v.id, values=(v.id, v.fecha, v.producto, v.cantidad,
                                                          f"${v.total:.2f}", v.vendedor))

    def registrar(self):
        try:
            self.servicio.registrar_venta(self._mapa.get(self.var_producto.get(), ""), self.var_cantidad.get(),
                                          self.usuario_sesion.usuario)
        except ValidacionError as error:
            messagebox.showwarning("Venta no válida", str(error), parent=self)
            return
        self.var_producto.set("")
        self.var_cantidad.set("1")
        self.refrescar()


class MainView(ttk.Frame):
    def __init__(self, master, servicio, usuario_sesion, al_cerrar_sesion):
        super().__init__(master, style="Fondo.TFrame")
        self.servicio = servicio
        self.usuario_sesion = usuario_sesion
        self.al_cerrar_sesion = al_cerrar_sesion
        self.iconos = estilos.cargar_iconos()
        self.logo = estilos.cargar_imagen("logo_pequeno.png")

        self._construir_menu()
        self.contenedor = ttk.Frame(self, style="Fondo.TFrame")
        self.contenedor.pack(side="left", fill="both", expand=True)

        self.secciones = {}
        self.mostrar_seccion("productos")

    def _construir_menu(self):
        menu = ttk.Frame(self, style="Lateral.TFrame", width=210)
        menu.pack(side="left", fill="y")
        menu.pack_propagate(False)

        cabecera = ttk.Frame(menu, style="Lateral.TFrame", padding=(14, 18))
        cabecera.pack(fill="x")
        if self.logo:
            ttk.Label(cabecera, image=self.logo, background=estilos.COLOR_LATERAL).pack(side="left")
        ttk.Label(cabecera, text=" Restaurante", style="LateralTitulo.TLabel").pack(side="left")

        self.botones = {}
        opciones = [("productos", "Productos"), ("ventas", "Ventas")]
        if self.usuario_sesion.es_administrador:  # solo el Administrador ve la gestión de usuarios
            opciones.append(("usuarios", "Usuarios"))
        for clave, texto in opciones:
            boton = ttk.Button(menu, text=f"  {texto}", image=self.iconos[clave], compound="left",
                               style="Menu.TButton", command=lambda c=clave: self.mostrar_seccion(c))
            boton.pack(fill="x")
            self.botones[clave] = boton

        pie = ttk.Frame(menu, style="Lateral.TFrame", padding=14)
        pie.pack(side="bottom", fill="x")
        ttk.Label(pie, text=self.usuario_sesion.nombre, style="LateralTitulo.TLabel", wraplength=170).pack(anchor="w")
        ttk.Label(pie, text=f"Rol: {self.usuario_sesion.rol}", style="LateralInfo.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Button(pie, text="  Cerrar sesión", image=self.iconos["salir"], compound="left",
                   style="Menu.TButton", command=self.al_cerrar_sesion).pack(fill="x")

    def mostrar_seccion(self, clave):
        if clave == "usuarios" and not self.usuario_sesion.es_administrador:
            messagebox.showwarning("Acceso restringido", "Solo el Administrador puede gestionar usuarios.", parent=self)
            return
        for seccion in self.secciones.values():
            seccion.pack_forget()
        if clave not in self.secciones:
            if clave == "productos":
                self.secciones[clave] = ProductosView(self.contenedor, self.servicio, self.iconos)
            elif clave == "ventas":
                self.secciones[clave] = VentasView(self.contenedor, self.servicio, self.usuario_sesion, self.iconos)
            else:
                self.secciones[clave] = UsuariosView(self.contenedor, self.servicio, self.usuario_sesion, self.iconos)
        elif hasattr(self.secciones[clave], "refrescar"):
            self.secciones[clave].refrescar()
        self.secciones[clave].pack(fill="both", expand=True)
        for k, boton in self.botones.items():
            boton.configure(style="MenuActivo.TButton" if k == clave else "Menu.TButton")
