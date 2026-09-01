# Cómo añadir una receta

Se aceptan recetas de fuera, y con ganas. Este documento explica el formato para
que tu receta se vea y se comporte como el resto.

Todas las recetas entran por **Pull Request** y las reviso y apruebo yo
([@AIAYN-creator](https://github.com/AIAYN-creator)) antes de fusionarlas. No es
burocracia: es la única forma de que el recetario mantenga un criterio.

**¿No sabes HTML?** No hace falta que aprendas para proponer una receta. Abre un
[issue con la plantilla "Proponer una receta"](../../issues/new/choose), escribe
ingredientes y pasos en texto normal, y ya la montaré yo o alguien más.

- [Antes de empezar](#antes-de-empezar)
- [El proceso](#el-proceso)
- [1. Copia la plantilla](#1-copia-la-plantilla)
- [2. Escribe la tabla](#2-escribe-la-tabla)
- [3. Las cantidades](#3-las-cantidades)
- [4. Da de alta la receta en el índice](#4-da-de-alta-la-receta-en-el-índice)
- [5. Valida y abre el PR](#5-valida-y-abre-el-pr)
- [Qué miro al revisar](#qué-miro-al-revisar)

## Antes de empezar

Encaja bien aquí una receta que:

- **la hayas cocinado tú**, más de una vez, y te salga bien;
- se pueda escribir en cantidades concretas (gramos, ml, unidades), no en
  "un poco de" ni "al gusto" para todo;
- tenga varias cosas pasando a la vez. El formato de tabla luce cuando hay
  paralelismo (algo cuece mientras otra cosa se sofríe). Una receta de tres
  pasos lineales cabe, pero desaprovecha el invento.

Y sobre el criterio: **las recetas tradicionales van sin atajos ni versiones
libres**. Si quieres proponer una variante de algo que ya está, dale un título
que lo deje claro en lugar de reescribir la existente.

Antes de escribir nada, comprueba que la receta no está ya en `index.html`.

## El proceso

```bash
# 1. Haz un fork en GitHub y clónalo
git clone https://github.com/<tu-usuario>/Recetas-.git
cd Recetas-

# 2. Una rama por receta
git checkout -b receta/fideua-de-marisco

# 3. Copia la plantilla y edítala
cp plantilla/receta-plantilla.html recetas/fideua-de-marisco.html

# 4. Da de alta la receta en index.html (ver más abajo)

# 5. Comprueba que no has descuadrado nada
python scripts/validar_recetas.py

# 6. Sube y abre el Pull Request
git add . && git commit -m "Añadir fideuá de marisco"
git push origin receta/fideua-de-marisco
```

## 1. Copia la plantilla

`plantilla/receta-plantilla.html` es una receta completa y funcionando, con los
huecos marcados con comentarios `RELLENAR` / `FIN RELLENAR`. Todo lo que hay
fuera de esos bloques —estilos y script— **se deja tal cual**: es lo que hace
que todas las recetas se vean igual y funcione el ajuste de comensales.

**Nombre del archivo:** en minúsculas, con guiones, sin acentos ni eñes:
`fideua-de-marisco.html`, `pollo-al-ajillo.html`. Va en `recetas/`.

En la cabecera rellenas el `<title>`, el `<h1>` y el subtítulo. El subtítulo
lleva el tiempo total y, si hace falta, una nota corta:
`~45 min` o `~20 min activos + mínimo 2h de nevera`.

## 2. Escribe la tabla

Esta es la parte con miga. La tabla se lee como un **diagrama de Gantt**: cada
fila es un ingrediente y las columnas avanzan en el tiempo.

| Clase | Para qué |
| --- | --- |
| `td.full` | Fila entera: algo sin ingrediente asociado (poner agua a hervir, precalentar el horno). Su `colspan` debe ser el ancho total de la tabla. |
| `td.ing` | El ingrediente y su cantidad. Siempre en la primera columna. |
| `td.prep` | Preparación en frío: picar, pelar, escurrir. Se pinta en gris. |
| `td.cook` | Lo que se hace al fuego. Se pinta en blanco y negrita. |
| `td.final` | El emplatado. Última columna, normalmente con un `rowspan` grande. |
| `td.gap` | Celda vacía de relleno. |

**La regla de oro:** todas las filas tienen que sumar el mismo número de
columnas, contando lo que ocupan los `rowspan` que vienen de filas de arriba.
Rellena los huecos con `<td class="gap"></td>`. Si te descuadras aunque sea una
celda, la tabla entera se deforma. El validador te dice exactamente qué fila
falla y cuántas celdas le faltan, así que no lo cuentes a mano: escríbela y
pásalo.

Agrupa con `rowspan` los ingredientes que entran juntos. Eso es lo que hace que
la tabla se lea de un vistazo:

```html
<tr>
  <td class="ing">... tomate ...</td>
  <td class="prep" data-step="2" rowspan="3">picar fino</td>
  <td class="cook" data-step="2" rowspan="3">sofreír 10 min a fuego medio</td>
  ...
</tr>
<tr>
  <td class="ing">... cebolla ...</td>
  <!-- las columnas de prep y cook ya las ocupa el rowspan de arriba -->
</tr>
<tr>
  <td class="ing">... pimiento ...</td>
</tr>
```

**Los pasos.** El atributo `data-step` numera los pasos de la navegación de
abajo. Van de **1 a N sin saltos**, y varias celdas pueden compartir número: se
iluminan a la vez, que es justo lo que quieres cuando un paso toca a tres
ingredientes. Al final del archivo, `const totalSteps` tiene que valer N.

Sobre la redacción: en minúscula y en infinitivo (`sofreír 5 min a fuego
medio`), concretando temperatura y tiempo siempre que se pueda. Para separar dos
acciones dentro de una misma celda se usa `·`. `td.final` es la excepción: empieza
en mayúscula, porque es una frase completa.

## 3. Las cantidades

Las cantidades que se escalan van dentro de un `<span class="qty">`:

```html
<td class="ing"><span class="qty" data-base="400" data-unit="g">400</span> g de arroz bomba</td>
```

| Atributo | Qué es |
| --- | --- |
| `data-base` | La cantidad **para 4 comensales**. Es el número que se multiplica. |
| `data-unit` | La unidad: `g`, `ml`, `ud`. |
| `data-decimals` | Decimales al escalar. Si no lo pones, **1**. Para cosas que se cuentan (dientes de ajo, huevos) pon `data-decimals="0"`: nadie echa 1,5 huevos. |

Todas las recetas se escriben **para 4 comensales**. `BASE_SERVINGS` y el
`value` del input de comensales se quedan en `4`.

Lo que no se escala —"sal al gusto", "pimienta recién molida"— se escribe como
texto normal, sin `span`.

## 4. Da de alta la receta en el índice

Una receta que no esté en la lista `RECIPES` de `index.html` existe en disco
pero **no la ve nadie**. Añade una entrada al final de la lista:

```js
{
  title: "Fideuá de Marisco",
  file: "recetas/fideua-de-marisco.html",
  allergens: ["gluten", "crustaceos", "moluscos"],
  timeMinutes: 50,
  requiresPrep: true,
  prepText: "Fumet de pescado hecho con antelación",
  diet: "ninguna"
},
```

| Campo | Qué poner |
| --- | --- |
| `title` | El mismo título que el `<h1>` de la receta. |
| `file` | La ruta, empezando por `recetas/`. |
| `allergens` | Lista de identificadores de la tabla de abajo. `[]` si no lleva ninguno. |
| `timeMinutes` | Tiempo **activo** en minutos, el que pasas en la cocina. Las horas de nevera o de fermentación no cuentan: eso va en `prepText`. |
| `requiresPrep` | `true` si hace falta trabajo por adelantado (un caldo del día antes, horas de reposo). |
| `prepText` | Solo si `requiresPrep` es `true`. Sale como aviso rojo en la tarjeta. |
| `diet` | `"ninguna"`, `"vegetariana"` o `"vegana"`. |

Identificadores de alérgeno (son los 14 de la normativa europea):

`gluten` · `crustaceos` · `huevo` · `pescado` · `cacahuete` · `soja` ·
`lacteos` · `frutos_cascara` · `apio` · `mostaza` · `sesamo` · `sulfitos` ·
`altramuces` · `moluscos`

Sé generoso declarando alérgenos, y **deja un comentario cuando no sea obvio de
dónde sale**, como se hace en las entradas que ya están:

```js
allergens: ["gluten", "pescado"], // pescado: las anchoas
```

Casos que se cuelan a menudo: el vino lleva `sulfitos`; muchas morcillas y
embutidos llevan pan rallado (`gluten`); la salsa Worcestershire lleva anchoa
(`pescado`).

Sobre `diet`: `"vegetariana"` admite huevo y lácteos; `"vegana"` no admite
ningún producto animal. Cuidado con el caldo de carne, las anchoas y la
mantequilla, que descartan una receta que por lo demás parecería vegetal.

## 5. Valida y abre el PR

```bash
python scripts/validar_recetas.py
```

Solo necesita Python 3, sin instalar nada. Tiene que decir `Todo correcto`. Lo
mismo se ejecuta automáticamente al abrir el Pull Request, así que si falla en
local, fallará también allí.

Después, abre la receta en el navegador y comprueba a mano lo que el validador
no puede ver:

- que la tabla no tenga huecos raros ni columnas descolocadas;
- que al recorrer los pasos se ilumine lo que toca, y solo lo que toca;
- que al cambiar de comensales las cantidades salgan con sentido;
- que en pantalla estrecha se pueda seguir usando.

**Una receta por Pull Request**, con la rama llamada `receta/<nombre>`. Así se
revisa y se discute cada una por separado.

## Qué miro al revisar

Al revisar el PR miro, más o menos por este orden:

1. **Que la receta sea correcta.** Es lo único que no puede arreglar el
   validador. Si es un plato tradicional, que respete la tradición.
2. **Alérgenos y dieta bien declarados.** Aquí soy tiquismiquis: hay gente que
   se fía de esa etiqueta.
3. **Que la tabla aproveche el formato**, agrupando de verdad lo que va junto en
   lugar de una fila por paso.
4. **Que los tiempos y temperaturas sean concretos.**
5. **Que no se hayan tocado los estilos ni el script.** Si crees que hay que
   cambiar algo del diseño, mejor un issue aparte: eso afecta a todas las
   recetas a la vez.

Es posible que te pida cambios, y no pasa nada: casi todas las recetas los
llevan. Si algo del formato no está claro o se te queda corto para lo que
quieres contar, abre un issue y lo hablamos.

Gracias por cocinar.
