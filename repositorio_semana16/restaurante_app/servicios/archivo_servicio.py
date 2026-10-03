"""Único módulo que lee y escribe archivos JSON. La interfaz nunca los toca."""
import json
import os


class ArchivoServicio:
    def __init__(self, carpeta):
        self.carpeta = carpeta
        os.makedirs(carpeta, exist_ok=True)

    def _ruta(self, nombre):
        return os.path.join(self.carpeta, nombre)

    def leer(self, nombre):
        ruta = self._ruta(nombre)
        if not os.path.exists(ruta):
            return []
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []

    def escribir(self, nombre, datos):
        ruta = self._ruta(nombre)
        temporal = ruta + ".tmp"
        with open(temporal, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
        os.replace(temporal, ruta)  # evita dejar el JSON a medias si algo falla
