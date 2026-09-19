classDiagram
class Exportable {
    <<Protocol>>
    +exportar() str
}
class Figura {
    <<abstract>>
    #_nombre str
    #_color str
    +area()* float
}
class Poligono {
    <<abstract>>
    #_lados list~Lado~
    #_observaciones list~str~
    +catalogo list~Poligono~$
    +lados_esperados()* int
    +perimetro() float
    +lados list~Lado~
    +exportar() str
    +agregar_observacion(texto)
}
class Lado {
    #_longitud float
    +etiqueta Etiqueta
    +longitud float
}
class Etiqueta {
    <<frozen dataclass>>
    +texto str
}
class Taller {
    #_poligonos list~Poligono~
    +recibir(poligono)
    +restaurar(poligono)
    +inventario() tuple~Poligono~
}
class Triangulo {
    +lados_esperados() int
    +area() float
}
class Cuadrado {
    +lados_esperados() int
    +area() float
}
class Pentagono {
    +lados_esperados() int
    +area() float
}
class Hexagono {
    +lados_esperados() int
    +area() float
}
class PlanoCAD {
    <<librería externa>>
    +exportar() str
}
Figura <|-- Poligono : herencia
Poligono <|-- Triangulo
Poligono <|-- Cuadrado
Poligono <|-- Pentagono
Poligono <|-- Hexagono
Poligono "1" *-- "3..*" Lado : composición
Lado "1" --> "0..1" Etiqueta : asociación
Taller "1" o-- "0..*" Poligono : agregación
Poligono ..|> Exportable : cumple
PlanoCAD ..|> Exportable : cumple