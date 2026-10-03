"""Lógica de negocio, validaciones y persistencia del restaurante."""
from datetime import datetime

from modelos import (Usuario, Producto, Venta, ROL_ADMIN, ROLES_GESTIONABLES)


class ValidacionError(Exception):
    """Error de regla de negocio; el mensaje se muestra tal cual al usuario."""


class RestauranteServicio:
    def __init__(self, archivos):
        self.archivos = archivos
        self.usuarios = [Usuario.from_dict(d) for d in archivos.leer("usuarios.json")]
        self.productos = [Producto.from_dict(d) for d in archivos.leer("productos.json")]
        self.ventas = [Venta.from_dict(d) for d in archivos.leer("ventas.json")]
        self._migrar_roles()

    # ------------------------------------------------------------ utilidades
    def _migrar_roles(self):
        """Si el JSON viene de la Semana 15 (sin roles), el usuario 'admin' pasa a Administrador."""
        if self.usuarios and not any(u.es_administrador for u in self.usuarios):
            for u in self.usuarios:
                if u.usuario.lower() == "admin":
                    u.rol = ROL_ADMIN
            self._guardar_usuarios()

    def _siguiente_id(self, lista, prefijo):
        numeros = [int(x.id[len(prefijo):]) for x in lista if x.id.startswith(prefijo) and x.id[len(prefijo):].isdigit()]
        return f"{prefijo}{(max(numeros) + 1 if numeros else 1):03d}"

    def _guardar_usuarios(self):
        self.archivos.escribir("usuarios.json", [u.to_dict() for u in self.usuarios])

    def _guardar_productos(self):
        self.archivos.escribir("productos.json", [p.to_dict() for p in self.productos])

    def _guardar_ventas(self):
        self.archivos.escribir("ventas.json", [v.to_dict() for v in self.ventas])

    # ------------------------------------------------------------ autenticación
    def autenticar(self, usuario, contrasena):
        usuario = usuario.strip().lower()
        for u in self.usuarios:
            if u.usuario.lower() == usuario and u.contrasena == contrasena:
                return u
        return None

    # ------------------------------------------------------------ usuarios (CRUD)
    def listar_usuarios(self):
        return list(self.usuarios)

    def obtener_usuario(self, id_usuario):
        for u in self.usuarios:
            if u.id == id_usuario:
                return u
        return None

    def _validar_usuario(self, nombre, usuario, contrasena, rol, id_actual=None, contrasena_obligatoria=True):
        if len(nombre.strip()) < 3:
            raise ValidacionError("El nombre debe tener al menos 3 caracteres.")
        if len(usuario.strip()) < 4 or " " in usuario.strip():
            raise ValidacionError("El usuario debe tener al menos 4 caracteres y no puede contener espacios.")
        if contrasena_obligatoria and len(contrasena) < 4:
            raise ValidacionError("La contraseña debe tener al menos 4 caracteres.")
        if contrasena and len(contrasena) < 4:
            raise ValidacionError("La nueva contraseña debe tener al menos 4 caracteres.")
        if rol not in ROLES_GESTIONABLES:
            raise ValidacionError("Seleccione un rol válido: Empleado o Cliente.")
        for u in self.usuarios:
            if u.usuario.lower() == usuario.strip().lower() and u.id != id_actual:
                raise ValidacionError(f"El usuario «{usuario.strip()}» ya está registrado.")

    def registrar_usuario(self, nombre, usuario, contrasena, rol):
        self._validar_usuario(nombre, usuario, contrasena, rol)
        nuevo = Usuario(self._siguiente_id(self.usuarios, "U"), nombre.strip(), usuario.strip(), contrasena, rol)
        self.usuarios.append(nuevo)
        self._guardar_usuarios()
        return nuevo

    def actualizar_usuario(self, id_usuario, nombre, usuario, contrasena, rol):
        existente = self.obtener_usuario(id_usuario)
        if existente is None:
            raise ValidacionError("El usuario seleccionado ya no existe.")
        if existente.es_administrador:
            raise ValidacionError("Las cuentas de administrador no se modifican desde esta pantalla.")
        self._validar_usuario(nombre, usuario, contrasena, rol, id_actual=id_usuario, contrasena_obligatoria=False)
        existente.nombre = nombre.strip()
        existente.usuario = usuario.strip()
        existente.rol = rol
        if contrasena:  # contraseña vacía = conservar la actual
            existente.contrasena = contrasena
        self._guardar_usuarios()
        return existente

    def eliminar_usuario(self, id_usuario, id_sesion):
        existente = self.obtener_usuario(id_usuario)
        if existente is None:
            raise ValidacionError("El usuario seleccionado ya no existe.")
        if id_usuario == id_sesion:
            raise ValidacionError("No puede eliminar la cuenta con la que inició sesión.")
        if existente.es_administrador:
            raise ValidacionError("Las cuentas de administrador no se eliminan desde esta pantalla.")
        self.usuarios.remove(existente)
        self._guardar_usuarios()

    # ------------------------------------------------------------ productos
    def listar_productos(self):
        return list(self.productos)

    def registrar_producto(self, nombre, precio, stock):
        if len(nombre.strip()) < 3:
            raise ValidacionError("El nombre del producto debe tener al menos 3 caracteres.")
        try:
            precio, stock = float(precio.replace(",", ".")), int(stock)
        except ValueError:
            raise ValidacionError("Precio y stock deben ser numéricos.")
        if precio <= 0 or stock < 0:
            raise ValidacionError("El precio debe ser mayor que 0 y el stock no puede ser negativo.")
        p = Producto(self._siguiente_id(self.productos, "P"), nombre.strip(), precio, stock)
        self.productos.append(p)
        self._guardar_productos()
        return p

    def eliminar_producto(self, id_producto):
        self.productos = [p for p in self.productos if p.id != id_producto]
        self._guardar_productos()

    # ------------------------------------------------------------ ventas
    def listar_ventas(self):
        return list(self.ventas)

    def registrar_venta(self, id_producto, cantidad, vendedor):
        producto = next((p for p in self.productos if p.id == id_producto), None)
        if producto is None:
            raise ValidacionError("Seleccione un producto.")
        try:
            cantidad = int(cantidad)
        except ValueError:
            raise ValidacionError("La cantidad debe ser un número entero.")
        if cantidad <= 0:
            raise ValidacionError("La cantidad debe ser mayor que 0.")
        if cantidad > producto.stock:
            raise ValidacionError(f"Stock insuficiente: solo quedan {producto.stock} unidades.")
        producto.stock -= cantidad
        venta = Venta(self._siguiente_id(self.ventas, "V"), datetime.now().strftime("%Y-%m-%d %H:%M"),
                      producto.nombre, cantidad, round(producto.precio * cantidad, 2), vendedor)
        self.ventas.append(venta)
        self._guardar_productos()
        self._guardar_ventas()
        return venta
