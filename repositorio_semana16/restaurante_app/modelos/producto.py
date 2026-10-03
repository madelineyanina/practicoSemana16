"""Modelo Producto: un plato o bebida del menú."""


class Producto:
    def __init__(self, id, nombre, precio, stock):
        self.id = id
        self.nombre = nombre
        self.precio = float(precio)
        self.stock = int(stock)

    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre, "precio": self.precio, "stock": self.stock}

    @classmethod
    def from_dict(cls, d):
        return cls(d["id"], d["nombre"], d["precio"], d["stock"])
