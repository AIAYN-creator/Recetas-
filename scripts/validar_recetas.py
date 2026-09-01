#!/usr/bin/env python3
"""Valida la coherencia del recetario.

Comprueba tres cosas que es fácil romper al añadir una receta a mano:

1. Que el índice (index.html) y la carpeta recetas/ digan lo mismo:
   ninguna receta huérfana, ningún enlace roto, metadatos con valores válidos.
2. Que la tabla de cada receta sea un rectángulo perfecto: con rowspan y
   colspan es muy fácil dejar un hueco y descuadrar todas las columnas.
3. Que la numeración de pasos sea 1..N sin saltos y que totalSteps coincida.

Uso:
    python scripts/validar_recetas.py

Sale con código 1 si hay errores. Los avisos (warnings) no hacen fallar.
No necesita dependencias: solo la librería estándar de Python 3.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # que los acentos salgan bien en la consola de Windows
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAIZ = Path(__file__).resolve().parent.parent
INDICE = RAIZ / "index.html"
DIR_RECETAS = RAIZ / "recetas"
PLANTILLA = RAIZ / "plantilla" / "receta-plantilla.html"

DIETAS_VALIDAS = {"ninguna", "vegetariana", "vegana"}

errores: list[str] = []
avisos: list[str] = []


def error(msg: str) -> None:
    errores.append(msg)


def aviso(msg: str) -> None:
    avisos.append(msg)


# --------------------------------------------------------------------------
# 1. Índice: lista ALLERGENS y base de datos RECIPES
# --------------------------------------------------------------------------

def sin_comentarios(texto: str) -> str:
    """Quita comentarios // de final de línea sin tocar los de dentro de comillas."""
    limpio = []
    for linea in texto.splitlines():
        fuera = True
        comilla = ""
        for i, ch in enumerate(linea):
            if fuera and ch in "\"'":
                fuera, comilla = False, ch
            elif not fuera and ch == comilla and linea[i - 1] != "\\":
                fuera = True
            elif fuera and ch == "/" and linea[i : i + 2] == "//":
                linea = linea[:i]
                break
        limpio.append(linea)
    return "\n".join(limpio)


def leer_bloque(texto: str, nombre: str) -> str:
    """Devuelve el contenido del array `const NOMBRE = [ ... ];`."""
    inicio = texto.find(f"const {nombre} = [")
    if inicio == -1:
        error(f"index.html: no encuentro la lista `const {nombre} = [`.")
        return ""
    inicio = texto.index("[", inicio)
    profundidad = 0
    for i in range(inicio, len(texto)):
        if texto[i] == "[":
            profundidad += 1
        elif texto[i] == "]":
            profundidad -= 1
            if profundidad == 0:
                return texto[inicio + 1 : i]
    error(f"index.html: la lista `{nombre}` no está bien cerrada.")
    return ""


def trocear_objetos(bloque: str) -> list[str]:
    """Parte `{...}, {...}` en objetos sueltos respetando anidamiento."""
    objetos, profundidad, arranque = [], 0, None
    for i, ch in enumerate(bloque):
        if ch == "{":
            if profundidad == 0:
                arranque = i
            profundidad += 1
        elif ch == "}":
            profundidad -= 1
            if profundidad == 0 and arranque is not None:
                objetos.append(bloque[arranque + 1 : i])
                arranque = None
    return objetos


def campo(objeto: str, clave: str) -> str | None:
    m = re.search(rf'\b{clave}\s*:\s*("[^"]*"|\'[^\']*\'|[^,\n]+)', objeto)
    return m.group(1).strip().strip("\"'") if m else None


def lista_campo(objeto: str, clave: str) -> list[str] | None:
    m = re.search(rf"\b{clave}\s*:\s*\[([^\]]*)\]", objeto)
    if not m:
        return None
    return [x.strip().strip("\"'") for x in m.group(1).split(",") if x.strip()]


def validar_indice() -> list[dict]:
    if not INDICE.exists():
        error("No existe index.html.")
        return []

    texto = sin_comentarios(INDICE.read_text(encoding="utf-8"))
    alergenos_validos = {
        m.group(1) for m in re.finditer(r'id\s*:\s*"([^"]+)"', leer_bloque(texto, "ALLERGENS"))
    }
    if not alergenos_validos:
        error("index.html: la lista ALLERGENS ha salido vacía.")

    recetas = []
    for objeto in trocear_objetos(leer_bloque(texto, "RECIPES")):
        titulo = campo(objeto, "title")
        archivo = campo(objeto, "file")
        etiqueta = titulo or archivo or "(entrada sin título ni archivo)"

        if not titulo:
            error(f"index.html: entrada sin `title` ({archivo or '?'}).")
        if not archivo:
            error(f"index.html: «{etiqueta}» no tiene `file`.")
            continue
        if not archivo.startswith("recetas/"):
            error(f"index.html: `file` de «{etiqueta}» debería empezar por 'recetas/'.")
        if not (RAIZ / archivo).exists():
            error(f"index.html: «{etiqueta}» apunta a {archivo}, que no existe.")

        alergenos = lista_campo(objeto, "allergens")
        if alergenos is None:
            error(f"index.html: «{etiqueta}» no tiene `allergens` (usa [] si no lleva ninguno).")
            alergenos = []
        for a in alergenos:
            if a not in alergenos_validos:
                error(f"index.html: «{etiqueta}» declara el alérgeno desconocido '{a}'.")

        minutos = campo(objeto, "timeMinutes")
        if minutos is None or not minutos.isdigit():
            error(f"index.html: «{etiqueta}» necesita `timeMinutes` como número entero.")

        prep = campo(objeto, "requiresPrep")
        if prep not in ("true", "false"):
            error(f"index.html: «{etiqueta}» necesita `requiresPrep: true` o `false`.")
        elif prep == "true" and not campo(objeto, "prepText"):
            error(f"index.html: «{etiqueta}» tiene requiresPrep: true pero le falta `prepText`.")
        elif prep == "false" and campo(objeto, "prepText"):
            aviso(f"index.html: «{etiqueta}» tiene `prepText` pero requiresPrep es false; no se mostrará.")

        dieta = campo(objeto, "diet")
        if dieta not in DIETAS_VALIDAS:
            error(
                f"index.html: «{etiqueta}» tiene diet: '{dieta}'. "
                f"Valores válidos: {', '.join(sorted(DIETAS_VALIDAS))}."
            )

        recetas.append({"title": titulo, "file": archivo})

    # Recetas en disco que nadie ha dado de alta en el índice
    registradas = {r["file"] for r in recetas}
    for ruta in sorted(DIR_RECETAS.glob("*.html")):
        rel = f"recetas/{ruta.name}"
        if rel not in registradas:
            error(f"{rel} existe pero no está dado de alta en la lista RECIPES de index.html.")

    return recetas


# --------------------------------------------------------------------------
# 2. Geometría de la tabla de cada receta
# --------------------------------------------------------------------------

class TablaParser(HTMLParser):
    """Reconstruye la rejilla de la primera <table> teniendo en cuenta los spans."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.en_tabla = False
        self.tabla_hecha = False
        self.filas: list[list[dict]] = []
        self.pasos: list[int] = []

    def handle_starttag(self, tag, attrs):
        atributos = dict(attrs)
        if tag == "table" and not self.tabla_hecha:
            self.en_tabla = True
        elif tag == "tr" and self.en_tabla:
            self.filas.append([])
        elif tag in ("td", "th") and self.en_tabla and self.filas:
            def entero(clave: str) -> int:
                try:
                    return max(1, int(atributos.get(clave, 1)))
                except ValueError:
                    return 1

            self.filas[-1].append({
                "colspan": entero("colspan"),
                "rowspan": entero("rowspan"),
                "class": atributos.get("class", ""),
                "step": atributos.get("data-step"),
            })
            if atributos.get("data-step", "").isdigit():
                self.pasos.append(int(atributos["data-step"]))

    def handle_endtag(self, tag):
        if tag == "table" and self.en_tabla:
            self.en_tabla, self.tabla_hecha = False, True


def validar_geometria(nombre: str, parser: TablaParser) -> None:
    """Coloca cada celda en la rejilla y avisa de huecos o desbordes."""
    if not parser.filas:
        error(f"{nombre}: no encuentro ninguna tabla con filas.")
        return

    ocupadas: dict[tuple[int, int], bool] = {}
    ancho = 0
    posiciones: list[tuple[int, int]] = []  # (fila, última columna ocupada + 1)

    for f, fila in enumerate(parser.filas):
        col = 0
        for celda in fila:
            while ocupadas.get((f, col)):
                col += 1
            for dc in range(celda["colspan"]):
                for dr in range(celda["rowspan"]):
                    ocupadas[(f + dr, col + dc)] = True
            col += celda["colspan"]
        # La fila puede terminar en celdas que vienen de un rowspan anterior
        while ocupadas.get((f, col)):
            col += 1
        posiciones.append((f, col))
        ancho = max(ancho, col)

    for f, fin in posiciones:
        if fin != ancho:
            error(
                f"{nombre}: la fila {f + 1} de la tabla ocupa {fin} columnas y la tabla tiene {ancho}. "
                f"Faltan {ancho - fin} celdas (normalmente <td class=\"gap\"></td>)."
            )

    # Las celdas a todo lo ancho deben declarar exactamente el ancho de la tabla
    for f, fila in enumerate(parser.filas):
        for celda in fila:
            if "full" in celda["class"].split() and celda["colspan"] != ancho:
                error(
                    f"{nombre}: la fila {f + 1} usa class=\"full\" con colspan={celda['colspan']}, "
                    f"pero la tabla tiene {ancho} columnas."
                )


def validar_receta(ruta: Path) -> None:
    nombre = ruta.relative_to(RAIZ).as_posix()
    texto = ruta.read_text(encoding="utf-8")

    parser = TablaParser()
    parser.feed(texto)
    validar_geometria(nombre, parser)

    # --- pasos ---
    if parser.pasos:
        usados = set(parser.pasos)
        maximo = max(usados)
        faltan = sorted(set(range(1, maximo + 1)) - usados)
        if faltan:
            error(f"{nombre}: faltan los pasos {faltan} (la numeración debe ser 1..N sin saltos).")

        m = re.search(r"const\s+totalSteps\s*=\s*(\d+)", texto)
        if not m:
            error(f"{nombre}: no encuentro `const totalSteps` en el script.")
        elif int(m.group(1)) != maximo:
            error(
                f"{nombre}: totalSteps = {m.group(1)} pero el data-step más alto de la tabla es {maximo}."
            )
    else:
        error(f"{nombre}: ninguna celda tiene data-step; la navegación por pasos no funcionará.")

    # --- comensales ---
    m_base = re.search(r"const\s+BASE_SERVINGS\s*=\s*(\d+)", texto)
    m_input = re.search(r'id="servingsInput"[^>]*value="(\d+)"', texto)
    if not m_base:
        error(f"{nombre}: falta `const BASE_SERVINGS` en el script.")
    elif m_input and m_base.group(1) != m_input.group(1):
        error(
            f"{nombre}: BASE_SERVINGS = {m_base.group(1)} pero el input de comensales arranca "
            f"en {m_input.group(1)}; las cantidades saldrían escaladas de entrada."
        )

    # --- cantidades escalables ---
    for m in re.finditer(r'<span class="qty"([^>]*)>', texto):
        attrs = m.group(1)
        if "data-base=" not in attrs:
            error(f"{nombre}: hay un <span class=\"qty\"> sin data-base; no se escalará.")
        elif not re.search(r'data-base="[\d.]+"', attrs):
            error(f"{nombre}: hay un data-base que no es un número: {attrs.strip()}")
        if "data-unit=" not in attrs:
            aviso(f"{nombre}: hay un <span class=\"qty\"> sin data-unit.")

    # --- cabecera ---
    if not re.search(r"<title>[^<]+</title>", texto):
        error(f"{nombre}: falta el <title> de la página.")
    if 'lang="es"' not in texto:
        aviso(f"{nombre}: el <html> no declara lang=\"es\".")

    # --- marca ---
    if "assets/icono.svg" not in texto:
        error(f'{nombre}: falta el favicon (<link rel="icon" href="../assets/icono.svg">).')
    if 'name="viewport"' not in texto:
        error(f"{nombre}: falta el <meta name=\"viewport\">; en el móvil se vería diminuta.")

    # --- vuelta al índice ---
    if 'class="back"' not in texto:
        error(
            f"{nombre}: falta el enlace de vuelta al índice "
            f'(<a class="back" href="../index.html">◀ Todas las recetas</a>, antes del <h1>).'
        )
    elif not re.search(r'class="back"[^>]*href="\.\./index\.html"', texto):
        error(f'{nombre}: el enlace .back debería apuntar a "../index.html".')


# --------------------------------------------------------------------------

def main() -> int:
    if not DIR_RECETAS.is_dir():
        print("No existe la carpeta recetas/.")
        return 1

    recetas = validar_indice()
    archivos = sorted(DIR_RECETAS.glob("*.html"))
    for ruta in archivos:
        validar_receta(ruta)

    # La plantilla también se valida: si se rompe, todas las recetas nuevas
    # nacerían rotas.
    if PLANTILLA.exists():
        validar_receta(PLANTILLA)
    else:
        aviso(f"No encuentro la plantilla en {PLANTILLA.relative_to(RAIZ)}.")

    for a in avisos:
        print(f"  aviso  {a}")
    for e in errores:
        print(f"  ERROR  {e}")

    print()
    print(f"{len(archivos)} recetas en disco · {len(recetas)} dadas de alta en el índice")
    if errores:
        print(f"{len(errores)} error(es). Corrígelos antes de abrir el PR.")
        return 1
    print("Todo correcto." + (f" ({len(avisos)} aviso(s) sin importancia)" if avisos else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
