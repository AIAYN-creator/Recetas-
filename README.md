<p align="center">
  <img src="assets/logo.png" alt="Mi Recetario" width="480">
</p>

<p align="center">
  <a href="https://aiayn-creator.github.io/Recetas-/"><strong>Abrir el recetario &rarr;</strong></a>
</p>

Un recetario web pensado para usarse **con las manos llenas de harina**: cada
receta es una sola página que te dice, paso a paso, qué ingrediente entra en
cada momento y qué se hace con él.

No es una lista de la compra seguida de un muro de texto. Cada receta es una
**tabla tipo diagrama de Gantt**: las filas son los ingredientes, las columnas
avanzan en el tiempo. De un vistazo ves qué va en paralelo (mientras se hace el
sofrito, cuece la pasta) y qué tiene que esperar. La idea del formato viene de
las tablas de [Cooking for Engineers](https://www.cookingforengineers.com/).

Además, cada receta:

- **escala las cantidades** al número de comensales que le digas;
- **ilumina el paso actual** para que no te pierdas a medio guiso;
- declara sus **alérgenos** y si necesita **preparación previa** (un caldo del
  día antes, horas de nevera), que es justo lo que se descubre demasiado tarde.

El índice permite buscar por nombre y filtrar por alérgenos a excluir, tiempo
total, preparación previa y dieta (vegetariana / vegana).

Está publicado en internet, así que basta con pasar el enlace: quien lo reciba
puede consultar todas las recetas desde el móvil, la tablet o el ordenador, sin
instalar nada y sin tener cuenta de GitHub.

## Verlo

**https://aiayn-creator.github.io/Recetas-/**

Ese es el enlace que hay que compartir. Se republica solo: cada push a `main`
deja el sitio actualizado en un par de minutos.

Cómo usar los filtros, el ajustador de comensales y la navegación por pasos:
**[USAGE.md](USAGE.md)**.

### En local

Solo hace falta si vas a tocar el código. No hay que compilar ni instalar nada
—es HTML, CSS y JavaScript a pelo, sin dependencias ni proceso de build—, pero
conviene servirlo por HTTP para que se comporte igual que publicado:

```bash
python -m http.server 5173
```

y abrir <http://localhost:5173>.

## Qué hay dentro

```
index.html                        el índice: buscador, filtros y la lista de recetas
recetas/                          una receta = un archivo HTML autónomo
plantilla/receta-plantilla.html   punto de partida para una receta nueva
scripts/validar_recetas.py        comprueba que nada se ha descuadrado
USAGE.md                          manual de uso
CONTRIBUTING.md                   cómo añadir una receta
```

Dos decisiones de diseño que conviene conocer antes de tocar nada:

- **Cada receta es autónoma.** Lleva sus propios estilos y su propio script
  dentro del archivo. Se duplica CSS entre recetas, sí, pero a cambio cualquier
  receta se puede abrir, mandar por correo o imprimir por su cuenta, y tocar una
  no puede romper las demás.
- **El índice es la única base de datos.** La lista `RECIPES` de `index.html`
  guarda el título, la ruta, los alérgenos, el tiempo, la preparación previa y
  la dieta. Una receta que no esté en esa lista existe en disco pero es
  invisible: nadie llega a ella.

## Añadir una receta

El proceso completo está en **[CONTRIBUTING.md](CONTRIBUTING.md)**. En corto:
copia la plantilla, rellénala, da de alta la receta en `index.html`, pasa el
validador y abre un Pull Request.

Todas las recetas entran por Pull Request y **las apruebo yo antes de
fusionarse**. Ni las mejores intenciones libran de que a una paella se le cuele
el chorizo.

## Validar antes de subir

```bash
python scripts/validar_recetas.py
```

Solo necesita Python 3, sin instalar nada. Comprueba lo que es fácil romper a
mano y difícil de ver a ojo:

- que el índice y la carpeta `recetas/` digan lo mismo (sin enlaces rotos ni
  recetas huérfanas) y que los metadatos tengan valores válidos;
- que la tabla de cada receta sea un rectángulo perfecto — con `rowspan` y
  `colspan` basta una celda de menos para descuadrar todas las columnas;
- que los pasos vayan de 1 a N sin saltos y que `totalSteps` coincida;
- que el título y el tiempo digan lo mismo en la receta y en el índice, que es
  información duplicada y se separa sola;
- que las cantidades sean escalables y que `BASE_SERVINGS` case con el número
  de comensales de partida.

Se ejecuta solo en cada Pull Request.

## Hoja de ruta

### v1.5.0 — pulir lo que se ve y quitar el doble trabajo

- **Cantidades sin decimales de adorno.** Ahora mismo todas las recetas muestran
  `150.0 g` o `250.0 ml`: `data-decimals` vale 1 por defecto y el redondeo se
  aplica también a los números enteros. Es un `if` en `renderServings` que
  mejora las 13 páginas a la vez.
- **Que no se apague la pantalla.** `navigator.wakeLock` mientras la receta está
  abierta. Hoy el móvil se bloquea a la media res de un sofrito y hay que
  desbloquearlo con las manos pringadas.
- **Índice autogenerado.** Que cada receta declare sus metadatos en su propia
  cabecera y que un script construya la lista `RECIPES` leyendo los archivos.
  Añadir una receta pasa a ser **editar un solo archivo** en vez de dos, que es
  donde se equivoca todo el mundo, y desaparece la duplicación que hoy hay que
  vigilar a mano: el título vive en tres sitios y el tiempo en dos.

### v2.0.0 — que salga de la cocina y aguante sin cobertura

- **Standalone.** Un manifest y un service worker para que el recetario se
  instale como una app y siga abriendo sin datos. Icono y viewport ya están; es
  el paso que falta.
- **Lista de la compra.** Marcar varias recetas, cada una con sus comensales, y
  obtener la lista combinada de ingredientes, sumando los 400 g de tomate de una
  con los 300 de otra. Los datos ya están en las tablas (`data-base`,
  `data-unit`): solo hay que juntarlos. Es lo que convierte el recetario en algo
  que se usa **antes** de cocinar, no solo durante.

Lo que no está previsto: cuentas de usuario, valoraciones, comentarios ni base
de datos. En cuanto haya un backend se pierde lo que hace bueno a esto —cero
mantenimiento, cero coste y nada que se pueda caer—, y el modelo de archivos
estáticos con revisión humana en el merge es una decisión, no una limitación.

## La marca

Los assets viven en `assets/` y se generan desde un único script, para que la
geometría y los colores no se dupliquen a mano:

```bash
python scripts/generar_logo.py
```

| Archivo | Para qué |
| --- | --- |
| `icono.svg` | Favicon de todas las páginas. |
| `icono-180.png` | Icono al guardar en la pantalla de inicio del móvil. |
| `logo.png` / `logo.svg` | El logotipo con el nombre, para el README. |
| `banner.png` | 1200×630, la imagen que sale al compartir el enlace. |

La marca es la propia tabla de una receta en miniatura: la columna de
ingredientes a la izquierda, una celda con `rowspan` y, en rojo con borde
dorado, el paso activo — el mismo estilo `td.active` del CSS.

El banner se usa como `og:image` en `index.html`. Para que salga también al
compartir el enlace **del repositorio**, hay que subirlo a mano en
*Settings → General → Social preview*: GitHub no lo coge del `og:image`.

## Licencia

[MIT](LICENSE).
