"""Genera el logo y los íconos PNG de assets/ (se ejecuta una sola vez, opcional)."""
import os
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
S = 8      # factor de supersampling para bordes suaves
N = 24     # tamaño final de los íconos
W = (255, 255, 255, 255)


def lienzo(n):
    return Image.new("RGBA", (n * S, n * S), (0, 0, 0, 0))


def guardar(img, nombre, n):
    img.resize((n, n), Image.LANCZOS).save(os.path.join(AQUI, nombre))


def icono(nombre, dibujar):
    img = lienzo(N)
    dibujar(ImageDraw.Draw(img))
    guardar(img, nombre, N)


def u(v):  # unidades de 24 px a píxeles de trabajo
    return v * S


def usuarios(d):
    d.ellipse([u(8), u(3), u(16), u(11)], fill=W)
    d.pieslice([u(3), u(13), u(21), u(31)], 180, 360, fill=W)


def productos(d):
    d.rectangle([u(4), u(8), u(20), u(20)], outline=W, width=u(2))
    d.rectangle([u(4), u(4), u(20), u(8)], fill=W)
    d.line([u(12), u(8), u(12), u(14)], fill=W, width=u(2))


def ventas(d):
    d.ellipse([u(3), u(3), u(21), u(21)], outline=W, width=u(2))
    d.line([u(12), u(6), u(12), u(18)], fill=W, width=u(2))
    d.arc([u(8), u(7), u(16), u(12)], 90, 360, fill=W, width=u(2))
    d.arc([u(8), u(12), u(16), u(17)], 270, 180, fill=W, width=u(2))


def registrar(d):
    d.line([u(12), u(5), u(12), u(19)], fill=W, width=u(3))
    d.line([u(5), u(12), u(19), u(12)], fill=W, width=u(3))


def actualizar(d):
    d.arc([u(4), u(4), u(20), u(20)], 30, 300, fill=W, width=u(3))
    d.polygon([(u(16), u(2)), (u(21), u(9)), (u(12), u(9))], fill=W)


def eliminar(d):
    d.rectangle([u(6), u(8), u(18), u(21)], outline=W, width=u(2))
    d.rectangle([u(4), u(5), u(20), u(7)], fill=W)
    d.rectangle([u(9), u(3), u(15), u(5)], fill=W)
    d.line([u(10), u(11), u(10), u(18)], fill=W, width=u(1))
    d.line([u(14), u(11), u(14), u(18)], fill=W, width=u(1))


def limpiar(d):
    d.line([u(5), u(5), u(19), u(19)], fill=W, width=u(3))
    d.line([u(19), u(5), u(5), u(19)], fill=W, width=u(3))


def salir(d):
    d.line([u(10), u(4), u(4), u(4), u(4), u(20), u(10), u(20)], fill=W, width=u(2))
    d.line([u(9), u(12), u(19), u(12)], fill=W, width=u(2))
    d.polygon([(u(20), u(12)), (u(15), u(7)), (u(15), u(17))], fill=W)


for nombre, f in [("usuarios", usuarios), ("productos", productos), ("ventas", ventas),
                  ("registrar", registrar), ("actualizar", actualizar), ("eliminar", eliminar),
                  ("limpiar", limpiar), ("salir", salir)]:
    icono(f"icono_{nombre}.png", f)

# ---- Logo: plato con cubiertos sobre círculo de color
def logo(n, nombre):
    img = lienzo(n)
    d = ImageDraw.Draw(img)
    k = n / 100
    p = lambda v: v * k * S
    d.ellipse([p(2), p(2), p(98), p(98)], fill=(200, 100, 59, 255))
    d.ellipse([p(24), p(24), p(76), p(76)], fill=(255, 255, 255, 255))
    d.ellipse([p(31), p(31), p(69), p(69)], outline=(200, 100, 59, 255), width=int(p(2)))
    # tenedor (izquierda)
    d.line([p(14), p(30), p(14), p(70)], fill=W, width=int(p(4)))
    for x in (10, 14, 18):
        d.line([p(x), p(30), p(x), p(44)], fill=W, width=int(p(2.5)))
    # cuchillo (derecha)
    d.line([p(86), p(30), p(86), p(70)], fill=W, width=int(p(4)))
    d.polygon([(p(84), p(30)), (p(90), p(30)), (p(90), p(52)), (p(84), p(52))], fill=W)
    guardar(img, nombre, n)

logo(128, "logo.png")
logo(32, "logo_pequeno.png")
print("Assets generados en", AQUI)
