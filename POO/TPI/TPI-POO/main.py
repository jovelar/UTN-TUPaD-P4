from figuras import *
from libreria_externa import PlanoCAD

#abs = Hexagono('pipo','rojo',[Lado(6),Lado(6),Lado(6),Lado(6),Lado(6),Lado(6)])

taller1 = Taller()

#Parte 5
t = Triangulo("t", "rojo", [Lado(3), Lado(4), Lado(5)])
c = Cuadrado("c", "azul", [Lado(2), Lado(2), Lado(2), Lado(2)])
p = Pentagono("p","violeta",[Lado(1),Lado(1),Lado(1),Lado(1),Lado(1)])
h = Hexagono("h","Amarillo",[Lado(5),Lado(5),Lado(5),Lado(5),Lado(5),Lado(5)])

lados_t = t.lados
lados_t[0].etiqueta = Etiqueta("borde exterior")

lados_c = c.lados
lados_c[0].etiqueta = Etiqueta("cateto A")


print("\nAgregando figuras al taller\n")
taller1.recibir(t)
taller1.recibir(c)
taller1.recibir(p)
taller1.recibir(h)

def mostrar_taller(taller):
    """Funcion auxiliar para revisar el contenido de un taller"""
    for poligono in taller.inventario():
        print(poligono.exportar())
        for lado in poligono.lados:
            if lado.etiqueta is not None:
                print(f"\tlado etiqueta: {lado.etiqueta.texto}")

print("Contenido del taller:\n")
mostrar_taller(taller1)

print("\n\nRestaurando una figura del taller, demostrando que solo se retiro la referencia y la figura sigue existiendo:\n")
taller1.restaurar(c)

mostrar_taller(taller1)

print("\nFigura retirada: ",c.exportar(),"\n\n")

#Instanciando Planocad y creando una lista mixta
print("\n\nCreando lista mixta entre Figuras y Planocad\n")
pl1 = PlanoCAD("Plano1","1:1500")

lista_mixta=[t,c,p,pl1]

#aplicando la funcionn exportar_todo()
lista_exportada_texto=exportar_todo(lista_mixta)

print("\n\nMostrando contenido de la lista mixta\n")
for item in lista_exportada_texto:
    print(item)
    
print("\n\nDemostracion falla trempana:\n")

try:
    Poligono("figura sin lados", "gris")
except TypeError as e:
    print(f"Error al instanciar: {e}")
    
