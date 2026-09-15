from parte1_diagnostico import *
from figuras import *

abs = Hexagono('pipo','rojo',[Lado(6),Lado(6),Lado(6),Lado(6),Lado(6),Lado(6)])

taller1 = Taller()

#Parte 5
t = Triangulo("t", "rojo", [Lado(3), Lado(4), Lado(5)])
c = Cuadrado("c", "azul", [Lado(2), Lado(2), Lado(2), Lado(2)])

lados_t = t.getLados()
lados_t[0].etiqueta = Etiqueta("borde exterior")

lados_c = c.getLados()
lados_c[0].etiqueta = Etiqueta("cateto A")


print("\nSegmento taller\n")
taller1.recibir(t)
taller1.recibir(c)

def mostrar_taller(taller):
    """Funcion auxiliar para revisar el contenido de un taller"""
    for poligono in taller.inventario():
        print(poligono.exportar())
        for lado in poligono.getLados():
            if lado.etiqueta is not None:
                print(f"\tlado etiqueta: {lado.etiqueta.texto}")

mostrar_taller(taller1)