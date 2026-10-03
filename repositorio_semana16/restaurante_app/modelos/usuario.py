"""Modelo Usuario: representa a una persona que usa el sistema del restaurante."""

ROL_ADMIN = "Administrador"
ROL_EMPLEADO = "Empleado"
ROL_CLIENTE = "Cliente"

ROLES = (ROL_ADMIN, ROL_EMPLEADO, ROL_CLIENTE)
# Roles que el administrador puede crear y gestionar desde la pantalla de Usuarios.
ROLES_GESTIONABLES = (ROL_EMPLEADO, ROL_CLIENTE)


class Usuario:
    def __init__(self, id, nombre, usuario, contrasena, rol=ROL_CLIENTE):
        self.id = id
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol

    @property
    def es_administrador(self):
        return self.rol == ROL_ADMIN

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "rol": self.rol,
        }

    @classmethod
    def from_dict(cls, datos):
        # Si el JSON es de una semana anterior y no trae "rol", se asume Cliente.
        return cls(
            datos["id"],
            datos["nombre"],
            datos["usuario"],
            datos["contrasena"],
            datos.get("rol", ROL_CLIENTE),
        )

    def __str__(self):
        return f"{self.nombre} ({self.usuario}) - {self.rol}"
