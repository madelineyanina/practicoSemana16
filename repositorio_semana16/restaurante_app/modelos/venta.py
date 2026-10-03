"""Modelo Venta: registro de una venta realizada por un usuario."""


class Venta:
    def __init__(self, id, fecha, producto, cantidad, total, vendedor):
        self.id = id
        self.fecha = fecha
        self.producto = producto
        self.cantidad = int(cantidad)
        self.total = float(total)
        self.vendedor = vendedor

    def to_dict(self):
        return {"id": self.id, "fecha": self.fecha, "producto": self.producto,
                "cantidad": self.cantidad, "total": self.total, "vendedor": self.vendedor}

    @classmethod
    def from_dict(cls, d):
        return cls(d["id"], d["fecha"], d["producto"], d["cantidad"], d["total"], d["vendedor"])
