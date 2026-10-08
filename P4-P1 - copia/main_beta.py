from catalogo import *
from libreria_externa import *
from dataclasses import FrozenInstanceError

#from catalogo import (UnidadMedida, Categoria, ProductoSimple, ProductoPorPeso,
#                      ProductoCombo, ProductoDestacado, Producto, exportar_catalogo)
#from libreria_externa import FichaPuntoDeVenta


print("="*60)
print("CATALOGO FOOD STORE")
print("="*60)

#unidades de venta
litro=UnidadMedida("litro","L","volumen")
kilogramo=UnidadMedida("kilogramo","kg","masa")
gramo=UnidadMedida("gramo","g","masa")

#categorias
bebidas=Categoria("Bebidas","Gaseosas, aguas y jugos")
gaseosas=Categoria("Gaseosas","Bebidas con gas")
almacen=Categoria("Almacen")
fiambreria=Categoria("Fiambreria","Productos frescos cortados al momento")
promos=Categoria("Promos","Combos armados del dia")

#productos del combo: existen por su cuenta, antes de que el combo exista
jamon=ProductoPorPeso("Jamon cocido",18.90,4.0,True,fiambreria,kilogramo)
aceitunas=ProductoSimple("Aceitunas x200g",4.75,25,True,almacen,gramo)

#los 4 productos del catalogo
gaseosa=ProductoSimple("Gaseosa 1.5L",2.50,30,True,bebidas,litro)
fideos=ProductoSimple("Fideos 500g",1.80,40,True,almacen,None)
queso=ProductoPorPeso("Queso cremoso",12.50,6.5,True,fiambreria,kilogramo)
combo=ProductoCombo("Picada para dos",True,promos,None,[jamon,aceitunas],0.10)

catalogo=[gaseosa,fideos,queso,combo]

print("\n-- Productos --")
for producto in catalogo:
    print(f"  {producto.nombre:<20} {producto.precio_publicado}")

print("\n-- Clasificacion --")

#la gaseosa nace en Bebidas y se agrega a Gaseosas como nueva principal
gaseosa.clasificar_en(gaseosas,es_principal=True)
queso.clasificar_en(promos)

for producto in catalogo:
    nombres=[vinculo.categoria.nombre for vinculo in producto.categorias()]
    print(f"  {producto.nombre:<20} {nombres}  principal: {producto.categoria_principal().nombre}")

#invariante siempre tiene una sola principal
principales=[v for v in gaseosa.categorias() if v.es_principal]
print(f"\n  Clasificaciones principales de la gaseosa: {len(principales)}")

try:
    queso.clasificar_en(fiambreria)
except ValueError as error:
    print(f"  Clasificar dos veces en la misma categoria: {error}")


print("\n-- Precios finales --")
print(f"  6 gaseosas          -> $ {gaseosa.precio_final(6):.2f}")
print(f"  0.250 kg de queso   -> $ {queso.precio_final(0.250):.2f}")
print(f"  2 picadas           -> $ {combo.precio_final(2):.2f}")

try:
    gaseosa.precio_final(2.5)
except ValueError as error:
    print(f"  2.5 gaseosas        -> {error}")


print("\n-- Disponibilidad --")
print(f"  Fideos disponibles: {fideos.disponible}")
fideos.deshabilitar()
print(f"  Tras deshabilitar : {fideos.disponible}")
fideos.habilitar()
print(f"  Tras habilitar    : {fideos.disponible}")

#el combo no tiene stock propio: depende de sus componentes
print(f"\n  Picada disponible : {combo.disponible}")
jamon.deshabilitar()
print(f"  Sin jamon         : {combo.disponible}")
jamon.habilitar()




print("\n-- Composicion: Producto es dueño de sus vinculos --")

#clasificar_en no devuelve el vinculo: la unica via de acceso es categorias()
devuelto=queso.clasificar_en(gaseosas)
print(f"  Lo que devuelve clasificar_en(): {devuelto}")

#categorias() devuelve una tupla, no la lista interna
vinculos=queso.categorias()
try:
    vinculos.append("algo")
except AttributeError as error:
    print(f"  append sobre categorias(): {error}")

#el vinculo no tiene setter: es_principal no es asignable desde afuera
try:
    vinculos[0].es_principal=True
except AttributeError as error:
    print(f"  Asignar es_principal: {error}")


print("\n-- Agregacion: los componentes sobreviven al combo --")
print(f"  Jamon sigue vivo y disponible: {jamon.disponible}")

#los mismos objetos se vuelven a agrupar en otro combo
otro=ProductoCombo("Picada XL",True,promos,None,[jamon,aceitunas,queso],0.15)
print(f"  Reagrupados en otro combo: {otro.precio_publicado}")
print(f"  Es el mismo jamon: {otro.componentes()[0] is combo.componentes()[0]}")


print("\n-- UnidadMedida es inmutable --")
try:
    kilogramo.simbolo="kgs"
except FrozenInstanceError as error:
    print(f"  Reasignar simbolo: {error}")


print("\n-- Falla temprana: revienta al construir, no al usar --")

#subclase definida solo para la demostracion: no implementa precio_final
class ProductoIncompleto(Producto):
    pass

try:
    Producto("Abstracto",1.0,1,True,almacen,None)
except TypeError as error:
    print(f"  Instanciar Producto: {error}")

try:
    ProductoIncompleto("Incompleto",1.0,1,True,almacen,None)
except TypeError as error:
    print(f"  Instanciar subclase sin precio_final: {error}")

print("\n-- Vidriera: destacar no es una forma de vender --")

#ProductoDestacado envuelve al producto, no hereda de el:
#por eso se puede destacar un combo o un producto por peso
destacados=[ProductoDestacado(combo,1),
            ProductoDestacado(queso,2),
            ProductoDestacado(gaseosa,3)]

for destacado in sorted(destacados,key=lambda d:d.orden_vidriera):
    producto=destacado.producto
    print(f"  {destacado.orden_vidriera}. {producto.nombre:<20} {producto.precio_publicado}")

print(f"\n  ProductoDestacado hereda de Producto: {issubclass(ProductoDestacado,Producto)}")
print(f"  El producto destacado es el mismo objeto: {destacados[0].producto is combo}")


print("\n-- Exportacion al punto de venta --")

#la misma lista lleva productos propios y fichas de un tercero
fichas=[FichaPuntoDeVenta("POS-001","Cierre de caja turno mañana"),
        FichaPuntoDeVenta("POS-002","Cierre de caja turno tarde")]

for linea in exportar_catalogo(catalogo+fichas):
    print(f"  {linea}")

print("\n"+"="*60)