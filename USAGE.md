# Manual de uso

Cómo se usa el recetario, tanto en el índice como dentro de una receta.

- [Abrirlo](#abrirlo)
- [El índice: buscar y filtrar](#el-índice-buscar-y-filtrar)
- [Dentro de una receta](#dentro-de-una-receta)
- [Leer la tabla](#leer-la-tabla)
- [Publicarlo en internet](#publicarlo-en-internet)

## Abrirlo

Doble clic en `index.html` y listo: no hay servidor, ni build, ni dependencias.

Si vas a tocar el código, es mejor servirlo por HTTP, que es como se comportará
una vez publicado:

```bash
python -m http.server 5173
```

Y abre <http://localhost:5173>.

En la cocina lo cómodo es abrirlo en el móvil o la tablet: la tabla hace scroll
horizontal y la barra de pasos queda fija abajo, al alcance del pulgar.

## El índice: buscar y filtrar

El índice muestra una tarjeta por receta con su tiempo total, sus alérgenos y,
si la tiene, un aviso rojo de preparación previa. Arriba hay cuatro controles,
que se **combinan entre sí**:

| Control | Qué hace |
| --- | --- |
| **Buscador** | Filtra por nombre según escribes. No busca dentro de los ingredientes. |
| **Excluir alérgenos** | Se marcan los que quieres **fuera**. Marcar 🥛 Lácteos esconde toda receta que lleve lácteos. Puedes marcar varios. |
| **Tiempo de preparación** | `< 30 min`, `30–60 min` o `+ 60 min`. Es el tiempo **activo**, el que pasas en la cocina; las horas de nevera o de fermentación no cuentan aquí. |
| **Preparación previa** | Aísla las recetas que exigen trabajo del día antes (un caldo, un fumet) o, al revés, las que se hacen del tirón. |
| **Dieta** | Vegetariana o vegana. **Vegana también aparece al filtrar por vegetariana**, porque toda receta vegana lo es. |

Los tres últimos son de selección única: al elegir una opción se desmarca la
anterior. Los alérgenos no: puedes acumular tantos como quieras.

Si no queda nada, sale un aviso en lugar de una rejilla vacía.

> **Los alérgenos son orientativos.** Están declarados a mano, receta a receta,
> y las trazas dependen de las marcas concretas que compres. Si hay una alergia
> seria de por medio, lee las etiquetas.

## Dentro de una receta

**Volver.** Arriba a la izquierda, *◀ Todas las recetas* te devuelve al
índice con los filtros en blanco.

**Comensales.** Arriba del todo. Con `−` / `+` o escribiendo el número. Todas
las cantidades en dorado se recalculan al instante. Las recetas están escritas
para **4 comensales**, así que pedir 6 multiplica por 1,5.

Ojo con el escalado: es una regla de tres pura. Para ingredientes principales va
bien, pero las especias, la sal y la levadura rara vez escalan de forma lineal,
y el tiempo de cocción no cambia solo porque dobles las cantidades. Úsalo como
punto de partida, no como dogma.

**Pasos.** La barra fija de abajo dice *Paso 3 de 7* y avanza con
`◀ Paso anterior` / `Paso siguiente ▶`. El paso activo se resalta en rojo con
borde dorado **en toda la tabla a la vez**: si un paso implica tres
ingredientes, se iluminan los tres. Eso es lo que te dice qué tienes entre manos
ahora mismo y qué está esperando.

La numeración es el orden recomendado, no una obligación: los pasos que caen en
la misma columna suelen poder hacerse a la vez.

## Leer la tabla

Es la parte que más se agradece cuando le pillas el truco. Se lee como un
**diagrama de Gantt**:

- cada **fila** es un ingrediente;
- las **columnas** avanzan en el tiempo, de izquierda a derecha;
- una celda que ocupa varias filas significa **"todos estos ingredientes van
  juntos en este momento"**;
- las celdas vacías son tiempo muerto para ese ingrediente: aún no le toca.

Los tipos de celda:

| Celda | Qué es |
| --- | --- |
| Fila entera resaltada | Algo que se hace sin ingrediente asociado: poner agua a hervir, precalentar el horno. |
| Ingrediente (izquierda) | El ingrediente y su cantidad, en dorado y escalable. |
| Texto gris | Preparación en frío: picar, pelar, escurrir. |
| Texto blanco en negrita | Lo que se hace al fuego. |
| Última columna | El emplatado y el servicio. |

Leyendo una fila entera de izquierda a derecha tienes la vida completa de ese
ingrediente. Leyendo una columna de arriba abajo tienes todo lo que pasa en ese
momento de la receta.

## Publicarlo en internet

Al ser HTML estático, GitHub Pages lo sirve tal cual: en **Settings → Pages**,
elige la rama `main` y la carpeta raíz (`/`). En un par de minutos queda en
`https://<usuario>.github.io/<repositorio>/`.

No hace falta nada más: ni acción de despliegue, ni configuración, ni build.
