from catalogo import *
from libreria_externa import *
from dataclasses import FrozenInstanceError
import os


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
jamon=ProductoPorPeso("Jamon cocido",1800.90,4.0,True,fiambreria,kilogramo)
aceitunas=ProductoSimple("Aceitunas x200g",4700.00,25,True,almacen,gramo)

#los 4 productos del catalogo
gaseosa=ProductoSimple("Gaseosa 1.5L",2500.00,30,True,bebidas,litro)
fideos=ProductoSimple("Fideos 500g",1900.00,40,True,almacen,None)
queso=ProductoPorPeso("Queso cremoso",6500.00,6.5,True,fiambreria,kilogramo)
queso_azul=ProductoPorPeso("Queso azul",9500.00,6.5,True,fiambreria,kilogramo)
combo=ProductoCombo("Picada para dos",True,promos,None,[jamon,aceitunas],0.10)

catalogo=[gaseosa,fideos,queso,jamon,aceitunas,combo]




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


print("Definidos Productos. unidades y categoirias")
print("presione enter para continuar")
input("")
os.system('cls')



print("Solo un producto principal \n")
#invariante siempre tiene una sola principal
principales=[v for v in gaseosa.categorias() if v.es_principal]
print(f"\n  Clasificaciones principales de la gaseosa: {len(principales)}")

print("\n\nIntentando registrar un queso 2 veces")
try:
    queso.clasificar_en(fiambreria)
except ValueError as error:
    print(f"  Clasificar dos veces en la misma categoria: {error}")

print("presione enter para continuar")
input("")
os.system('cls')

print("Solo se aceptan unidades enteras")

print("\n-- Precios finales --")
print(f"  6 gaseosas          -> $ {gaseosa.precio_final(6):.2f}")
print(f"  0.250 kg de queso   -> $ {queso.precio_final(0.250):.2f}")
print(f"  2 picadas           -> $ {combo.precio_final(2):.2f}")

try:
    gaseosa.precio_final(2.5)
except ValueError as error:
    print(f"  2.5 gaseosas        -> {error}")

print("presione enter para continuar")
input("")
os.system('cls')

print("Se cambia la disponibilidad de los productos mediante el metodo habilitar()/desabilitar()")

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


print("presione enter para continuar")
input("")
os.system('cls')
print("\n-- Composicion: Producto es dueño de sus vinculos --")

temporal=ProductoSimple("Producto temporal",100.00,1,True,almacen,None)
print(f"  Vinculo del temporal: {temporal.categorias()[0].categoria.nombre}")

del temporal
try:
    temporal.categorias()
except NameError as error:
    print(f"  Tras borrar el producto: {error}")


print("presione enter para continuar")
input("")
os.system('cls')

print("\n-- Agregacion: los componentes sobreviven al combo --")
print(f"  Jamon sigue vivo y disponible: {jamon.disponible}")

#los mismos objetos se vuelven a agrupar en otro combo
otro=ProductoCombo("Picada XL",True,promos,None,[jamon,aceitunas,queso],0.15)
print(f"  Reagrupados en otro combo: {otro.precio_publicado}")
print(f"  Es el mismo jamon: {otro.componentes()[0] is combo.componentes()[0]}")

del otro
print(f"  Combo borrado. El jamon sigue vivo: {jamon.nombre} {jamon.precio_publicado}")
print(f"  Y se puede seguir vendiendo: $ {jamon.precio_final(0.5):.2f}")


print("presione enter para continuar")
input("")
os.system('cls')

print("\n-- UnidadMedida es inmutable --")
try:
    kilogramo.simbolo="kgs"
except FrozenInstanceError as error:
    print(f"  Reasignar simbolo: {error}")

print("presione enter para continuar")
input("")
os.system('cls')


print("\n-- Falla temprana al intentar instancias una clase que no implemente precio_final" \
": revienta al construir, no al usar --")

#subclase definida solo para la demostracion: no implementa precio_final
class ProductoRoto(Producto):
    pass

try:
    Producto("Abstracto",1.0,1,True,almacen,None)
except TypeError as error:
    print(f"  Instanciar Producto: {error}")

try:
    ProductoRoto("Incompleto",1.0,1,True,almacen,None)
except TypeError as error:
    print(f"  Instanciar subclase sin precio_final: {error}")



print("presione enter para continuar")
input("")
os.system('cls')
print("Wrapper implementado como solucion a ProductoDestacado ")



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


#la misma lista lleva productos propios y fichas de un tercero
fichas=[FichaPuntoDeVenta("t1","cierre de punto de venta turno mañana"),
        FichaPuntoDeVenta("t2","cierre de punto de venta turno tarde")]

print("presione enter para continuar")
input("")
os.system('cls')
print("Demostracion salida funcion exportar")

for linea in exportar_catalogo(catalogo+fichas):
    print(f"  {linea}")

print("\n"+"="*60)