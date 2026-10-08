## ProductoDestacado
Se prefirio rediseñarla, haciendo un "wrap":
 * Es mas flexible, se puede crear y eliminar un objeto ProductoDestacado, eso no afecta la existencia del Producto.
 * Se puede otorgar una propiedad orden_vidriera, sin tener que alterar la clase Producuto
 *  El hecho de destacar un producto no afectaria los atributos del mismo, como precio, stock, etc.
 * Se asume que el hecho de destacar un producto tiene dimension temporal: Si el producto descatacado fuera cargarado como un nuevo producto, el dia de mañana que se termine la promocion y no sea un producto destacado, se tendria que eliminar el producto asi como su stock.

## ProductoCombo

Se utilizar el precio de los productos base, se suman y se aplica un coeficiente que seria el descuento. Es un numero periodico que va desde 0 hasta 1