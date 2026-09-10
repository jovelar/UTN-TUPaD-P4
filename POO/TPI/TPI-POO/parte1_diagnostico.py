"""parte1_diagnostico.py — El dominio Figura / Polígono / Lado, funcionando.

⚠️ Este módulo corre de punta a punta sin lanzar un solo traceback. No tiene bugs
de sintaxis: tiene ACENTO DE JAVA.

Contiene exactamente 8 java-ismos de DISEÑO. Siete están en el checklist de la
Actividad 4; el octavo no está en ese checklist y hay que encontrarlo con criterio,
no con la lista.

Además hay ruido sintáctico (punto y coma al final de línea, comparaciones contra
True, concatenación con + donde iría un f-string). Ese ruido también se limpia, pero
NO cuenta dentro de los 8.

Tu trabajo (Parte 1): encontrarlos, listarlos en informe.md y corregirlos, cada uno
justificado con la inversión conceptual que lo explica.
"""

import math


class Figura:
    def __init__(self, nombre, color):
        self._nombre = nombre
        self._color = color
        self._construida = True   # marca de que Figura.__init__ realmente corrió
        
    #Se eliminaron getters y setters innecesarios, uso de anotacion property para area

    def area(self):
        return 0.0


class Lado:
    def __init__(self, longitud):
        self._longitud = longitud
    
    #Se elimino getter innecesario e uso de la anotacion @property por que realiza evaluacion
    #antes de asignar
    
    #Antes
    def setLongitud(self, valor):
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        self._longitud = valor
    
    #Despues
    @property
    def setLongitud(self, valor):
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        self._longitud = valor


class Poligono(Figura):
    #Se incorporo catalogo como aatributo de la clase
    def __init__(self, nombre, color, lados=None, observaciones=None):
        #Uso de super
        super().__init__(nombre,color)
        #se realiza una copia defensiva para desvincular
        self._lados = list(lados) if lados is not None else []
        self._observaciones = observaciones if observaciones is not None else []
        self.catalogo = []
        Poligono.catalogo.append(self)

    def lados_esperados(self):
        return 0

    # >>> bucle acumulador manual en vez de comprehension <<<
    def perimetro(self):
        return sum(l.getLongitud() for l in self._lados)

    # >>> el type hint miente (-> int y devuelve str) y el "@Override" no existe <<<
    def area(self) -> str:
        return "area sin calcular"

    def agregar_observacion(self, texto):
        self._observaciones.append(texto)


    def getLados(self):
        #devuelve una copia
        return list(self._lados)


# >>> sobrecarga de constructor estilo Java: un __init__ con ramas isinstance <<<
#Se agregaron constructores alternativos
class Triangulo(Poligono):
    def __init__(self, nombre="triángulo", color="negro", lados=None):
        super().__init__(nombre, color, lados if lados is not None else [])

    @classmethod
    def desde_lista_lados(cls, lista_lados, nombre="triángulo", color="negro"):
        return cls(nombre, color, lista_lados)


    def lados_esperados(self):
        return 3




class Cuadrado(Poligono):
    def __init__(self, nombre="cuadrado", color="negro", lados=None):
        super().__init__(nombre, color, lados if lados is not None else [])
    #Se agragaron constructores alternativos
    @classmethod
    def desde_lista_lados(cls, lista_lados, nombre="cuadrado", color="negro"):
        return cls(nombre, color, lista_lados)


    def lados_esperados(self):
        return 4


class PoligonoRegular(Poligono):
    """Polígono de N lados de igual longitud.

    ⚠️ PARTE 3 — esta clase NO es uno de los 8 java-ismos de la Parte 1.

    Se modeló heredando de Poligono para poder guardarla en la misma lista que
    los demás polígonos y recorrerla con un único tipo común. En Java esa
    herencia hacía falta; en Python no. Si su lugar en la jerarquía lo justifica
    el dominio («un polígono regular ES-UN polígono») o solamente la ceremonia
    del compilador es, exactamente, la decisión que se te pide tomar, justificar
    e IMPLEMENTAR en la Parte 3.
    """

    def __init__(self, nombre, color, medida, cantidad):
        super().__init__(nombre, color, [Lado(medida) for _ in range(cantidad)])
        self._cantidad = cantidad

    def lados_esperados(self):
        return self._cantidad


if __name__ == "__main__":
    activo = True
    if activo == True:                                      # ruido: == True
        t = Triangulo("Triángulo", "rojo", [Lado(3), Lado(4), Lado(5)]);   # ruido: ;
        c = Cuadrado("Cuadrado", "azul", [Lado(2), Lado(2), Lado(2), Lado(2)])
        print("Perímetro del triángulo: " + str(t.perimetro()))            # ruido: +
        print("Perímetro del cuadrado: " + str(c.perimetro()))
        t.agregar_observacion("revisar el vértice A")
        print("Figuras en el catálogo: " + str(len(Poligono.catalogo)))
        print("Nombre (via getter): " + t.getNombre())
        r = PoligonoRegular("Pentágono", "verde", 4, 5)
        print("Perímetro del pentágono: " + str(r.perimetro()))
