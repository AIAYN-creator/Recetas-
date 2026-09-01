#!/usr/bin/env python3
"""Genera los assets de marca del recetario a partir de una sola definición.

La marca es la propia tabla de una receta en miniatura: la columna de
ingredientes a la izquierda, una celda que abarca varias filas con un rowspan
y, en rojo con borde dorado, el paso activo. Es exactamente el estilo td.active
del CSS, que es la imagen que identifica al recetario.

Uso:
    python scripts/generar_logo.py

Escribe en assets/:
    icono.svg       la marca en vectorial (favicon)
    icono-180.png   apple-touch-icon
    logo.svg        marca + nombre, vectorial
    logo.png        marca + nombre, para el README
    banner.png      1200x630, para og:image y la vista previa de GitHub

Necesita Pillow. No se ejecuta en CI: los assets van versionados.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "assets"

# --- paleta corporativa, la misma que el CSS ---
BG = "#1a1210"
BORDE = "#4a2e28"
ORO = "#d1a355"
ORO_APAGADO = "#8a6a45"
ROJO = "#b3312c"
TEXTO = "#f5ece4"
TEXTO_TENUE = "#c9b8ae"

# --- geometría de la marca, en una rejilla de 64x64 ---
TILE = 64
RADIO_TILE = 14
# Celdas: (x, y, ancho, alto, relleno, borde). La rejilla ocupa de 12 a 52.
CELDAS = [
    # columna de ingredientes
    (12, 12, 14, 7, ORO, None),
    (12, 23, 14, 7, ORO, None),
    (12, 34, 14, 7, ORO, None),
    (12, 45, 14, 7, ORO, None),
    # columna de pasos: arriba, el paso activo con rowspan, abajo
    (29, 12, 23, 7, ORO_APAGADO, None),
    (29, 23, 23, 18, ROJO, ORO),     # td.active: rojo con borde dorado
    (29, 45, 23, 7, ORO_APAGADO, None),
]

FUENTE_TITULO = "C:/Windows/Fonts/ARIALNB.TTF"   # condensada, en la línea de Bebas Neue
FUENTE_TEXTO = "C:/Windows/Fonts/seguisb.ttf"

NOMBRE = "MI RECETARIO"
LEMA = "Recetas que se leen de un vistazo"


# --------------------------------------------------------------------------
# SVG
# --------------------------------------------------------------------------

def barras_svg(escala=1.0, dx=0.0, dy=0.0):
    partes = []
    for x, y, w, h, relleno, borde in CELDAS:
        trazo = f' stroke="{borde}" stroke-width="{2 * escala:.2f}"' if borde else ""
        partes.append(
            f'  <rect x="{x * escala + dx:.2f}" y="{y * escala + dy:.2f}" '
            f'width="{w * escala:.2f}" height="{h * escala:.2f}" '
            f'rx="{2 * escala:.2f}" fill="{relleno}"{trazo}/>'
        )
    return chr(10).join(partes)


def escribir_icono_svg():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TILE} {TILE}" role="img" aria-label="Mi Recetario">
  <title>Mi Recetario</title>
  <rect x="1" y="1" width="{TILE - 2}" height="{TILE - 2}" rx="{RADIO_TILE}" fill="{BG}" stroke="{BORDE}" stroke-width="2"/>
{barras_svg()}
</svg>
'''
    (ASSETS / "icono.svg").write_text(svg, encoding="utf-8")


def escribir_logo_svg():
    """Marca + nombre en horizontal. El texto lleva pila de fuentes con reserva."""
    ancho, alto = 480, 128
    marca = 96
    escala = marca / TILE
    mx, my = 16, (alto - marca) / 2
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" role="img" aria-label="Mi Recetario">
  <title>Mi Recetario</title>
  <rect width="{ancho}" height="{alto}" rx="16" fill="{BG}"/>
  <g transform="translate({mx} {my}) scale({escala:.4f})">
    <rect x="1" y="1" width="{TILE - 2}" height="{TILE - 2}" rx="{RADIO_TILE}" fill="{BG}" stroke="{BORDE}" stroke-width="2"/>
{barras_svg()}
  </g>
  <text x="132" y="62" font-family="Bebas Neue, Arial Narrow, Haettenschweiler, sans-serif"
        font-size="42" letter-spacing="2" fill="{ORO}">{NOMBRE}</text>
  <text x="132" y="88" font-family="Work Sans, Segoe UI, Helvetica, Arial, sans-serif"
        font-size="16" fill="{TEXTO_TENUE}">{LEMA}</text>
</svg>
'''
    (ASSETS / "logo.svg").write_text(svg, encoding="utf-8")


# --------------------------------------------------------------------------
# PNG (se dibuja a 4x y se reduce, que Pillow no antialiasa las esquinas)
# --------------------------------------------------------------------------

SS = 4


def dibujar_marca(draw, x0, y0, lado, con_fondo=True):
    """Dibuja la marca con la esquina superior izquierda en (x0, y0)."""
    k = lado / TILE
    if con_fondo:
        draw.rounded_rectangle(
            [x0, y0, x0 + lado, y0 + lado],
            radius=RADIO_TILE * k, fill=BG, outline=BORDE, width=max(1, int(2 * k)),
        )
    for x, y, w, h, relleno, borde in CELDAS:
        draw.rounded_rectangle(
            [x0 + x * k, y0 + y * k, x0 + (x + w) * k, y0 + (y + h) * k],
            radius=2 * k, fill=relleno,
            outline=borde, width=max(1, int(2 * k)) if borde else 0,
        )


def lienzo(ancho, alto, fondo):
    img = Image.new("RGBA", (ancho * SS, alto * SS), fondo)
    return img, ImageDraw.Draw(img)


def reducir(img, ancho, alto, destino):
    img.resize((ancho, alto), Image.LANCZOS).save(ASSETS / destino)
    print(f"  {destino}  {ancho}x{alto}")


def fuente(ruta, tam):
    return ImageFont.truetype(ruta, tam * SS)


def texto_centrado(draw, cx, y, txt, fnt, color):
    ancho = draw.textbbox((0, 0), txt, font=fnt)[2]
    draw.text((cx * SS - ancho / 2, y * SS), txt, font=fnt, fill=color)


def escribir_icono_png():
    lado = 180
    img, draw = lienzo(lado, lado, (0, 0, 0, 0))
    dibujar_marca(draw, 0, 0, lado * SS)
    reducir(img, lado, lado, "icono-180.png")


def escribir_logo_png():
    ancho, alto, marca = 480, 128, 96
    img, draw = lienzo(ancho, alto, (0, 0, 0, 0))
    draw.rounded_rectangle([0, 0, ancho * SS, alto * SS], radius=16 * SS, fill=BG)
    dibujar_marca(draw, 16 * SS, (alto - marca) / 2 * SS, marca * SS)
    draw.text((132 * SS, 26 * SS), NOMBRE, font=fuente(FUENTE_TITULO, 34), fill=ORO)
    draw.text((132 * SS, 74 * SS), LEMA, font=fuente(FUENTE_TEXTO, 15), fill=TEXTO_TENUE)
    reducir(img, ancho, alto, "logo.png")


def escribir_banner():
    ancho, alto, marca = 1200, 630, 200
    img, draw = lienzo(ancho, alto, BG)
    # filo dorado inferior, como el borde de las celdas activas
    draw.rectangle([0, (alto - 8) * SS, ancho * SS, alto * SS], fill=ORO)
    dibujar_marca(draw, (ancho - marca) / 2 * SS, 132 * SS, marca * SS)
    texto_centrado(draw, ancho / 2, 372, NOMBRE, fuente(FUENTE_TITULO, 82), ORO)
    texto_centrado(draw, ancho / 2, 470, LEMA, fuente(FUENTE_TEXTO, 30), TEXTO)
    reducir(img, ancho, alto, "banner.png")


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    escribir_icono_svg()
    print("  icono.svg")
    escribir_logo_svg()
    print("  logo.svg")
    escribir_icono_png()
    escribir_logo_png()
    escribir_banner()
