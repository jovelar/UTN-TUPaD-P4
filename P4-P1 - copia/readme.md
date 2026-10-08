# Food Store — Catálogo

Primera Evaluación Parcial — Programación IV
Tecnicatura Universitaria en Programación (UTN)
Ovelar, Isaías Javier

Modelo de dominio en memoria para el catálogo de un comercio: productos que se
venden por pieza, por peso y combos armados con productos existentes. Cada
producto se clasifica en una o más categorías, con una marcada como principal, y
el catálogo completo se exporta al sistema de caja de un tercero.

## Ejecución

Requiere Python 3.12 o superior. No hay dependencias externas ni entorno virtual.

```bash
python main.py
```

## Archivos

| Archivo | Qué resuelve |
|---|---|
| `catalogo.py` | Dominio completo: `Producto` y sus subclases, `Categoria`, `ProductoCategoria`, `UnidadMedida`, `ProductoDestacado`, el `Protocol` `Exportable` y `exportar_catalogo()`. Requerimientos 1 a 4. |
| `libreria_externa.py` | `FichaPuntoDeVenta`, clase de un tercero. Se entrega y no se modifica. |
| `main.py` | Demo ejecutable: arma el catálogo, calcula precios, exporta y deja a la vista las decisiones de diseño. Requerimiento 5. |
| `uml/modelo_final.md` | Diagrama de clases final, con la decisión del Requerimiento 3. |
| `link_video.txt` | Link al video de defensa. |

## Cómo se distinguen las tres relaciones

**Composición — `Producto` y `ProductoCategoria`.** El vínculo lo fabrica el
producto dentro de `clasificar_en()`. El código cliente nunca lo instancia, no lo
recibe de vuelta —`clasificar_en()` devuelve `None`— y solo lo alcanza por
`categorias()`, que entrega una tupla. Si el producto deja de existir, sus
vínculos no tienen a quién clasificar y mueren con él.

**Agregación — `ProductoCombo` y sus componentes.** Los componentes llegan ya
construidos al constructor. Existen antes del combo, siguen existiendo después y
se pueden reagrupar en otro combo, como muestra `main.py`.

**Asociación — `Producto` y `Unidade construida,
puede ser `None` y varios productos comparten el mismo objeto. Ninguno es dueño
de ella.

## Decisiones que el diagrama no de

**`ProductoDestacado` no hereda de `Producto`.** El eje de la jerarquía de
`Producto` es cómo se calcula el precio: por pieza, por peso, por combo. Destacar
un producto no cambia cómo se cobra, así que la subclase no aportaba ninguna regla
de `precio_final()` —el enunciado mismo obliga a inventarle una—. La herencia se
reemplaza por una asociación: `ProductoDestacado` envuelve al producto y guarda
`_orden_vidriera`. Con eso se puede destacar **cualquier** producto del catálogo,
incluido un combo o un producto por peso, que con herencia habría requerido una
clase por cada combinación.

**Destacar es solo visibilidad.** No modifica el precio, ni el stock, ni la
disponibilidad. Un producto destaca no lo está.

**El combo no tiene precio ni stock propios.** Se arma en el momento con lo que
hay en góndola, así que ambos se derivan de sus componentes: `precio_base` es la
suma de los componentes con el descuento aplicado, y `disponible` es verdadero
solo si el combo está habilitado y todos sus componentes están disponibles. Por
eso el constructor no los recibe.

**`precio_base` del combo se calculs cambiara el
precio de un componente, `precio_final()` lo refleja pero `precio_publicado` no.
Con el modelo en memoria durante un.

## Contrato `Exportable`

Está resuelto como `Protocol`. Ninguna clase del dominio hereda de él: la
conformidad es estructural, por tenogo()` lo usa una
sola vez, como anotación de tipo en su firma, y funciona en runtime con productos
propios y con `FichaPuntoDeVenta` en la misma lista, sin tocar la librería externa.