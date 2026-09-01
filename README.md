# Mi Recetario

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

## Verlo

No hay que compilar ni instalar nada: es HTML, CSS y JavaScript a pelo, sin
dependencias ni proceso de build.

La forma rápida es abrir `index.html` con doble clic. Para que se comporte
exactamente igual que publicado, levanta un servidor local:

```bash
python -m http.server 5173
```

y abre <http://localhost:5173>.

Cómo usar los filtros, el ajustador de comensales y la navegación por pasos:
**[USAGE.md](USAGE.md)**.

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
- que las cantidades sean escalables y que `BASE_SERVINGS` case con el número
  de comensales de partida.

Se ejecuta solo en cada Pull Request.

## Licencia

[MIT](LICENSE).
