"""Verificación Ej.1."""
from figuras import (Punto, Lado, Figura, Poligono, Triangulo, Cuadrilatero,
                     Rectangulo, Cuadrado, Elipse, Circulo)

_checks = _ok = 0
def check(desc: str, cond: bool) -> None:
    global _checks, _ok
    _checks += 1
    if cond: _ok += 1; print(f"  [OK] {desc}")
    else: print(f"  [FALLA] {desc}")


def main() -> None:
    print("=== Ejercicio 1: Figuras geometricas ===\n")

    cuad = Cuadrado()
    check("Cuadrado es Rectangulo", isinstance(cuad, Rectangulo))
    check("Cuadrado es Cuadrilatero", isinstance(cuad, Cuadrilatero))
    check("Cuadrado es Poligono", isinstance(cuad, Poligono))
    check("Cuadrado es Figura", isinstance(cuad, Figura))

    circ = Circulo(5.0)
    check("Circulo es Elipse", isinstance(circ, Elipse))
    check("Circulo es Figura", isinstance(circ, Figura))
    check("Area del circulo r=5 ~ 78.54", abs(circ.area - 78.5398) < 0.01)

    lado = Lado(Punto(0, 0), Punto(3, 4))
    check("Longitud del lado (0,0)-(3,4) = 5", abs(lado.longitud - 5.0) < 1e-9)

    tri = Triangulo()
    tri.agregar_lado(Lado(Punto(0, 0), Punto(4, 0)))
    tri.agregar_lado(Lado(Punto(4, 0), Punto(4, 3)))
    check("Triangulo con 2 lados NO es valido", not tri.estructura_valida)
    tri.agregar_lado(Lado(Punto(4, 3), Punto(0, 0)))
    check("Triangulo con 3 lados SI es valido", tri.estructura_valida)
    check("nro_lados derivado = 3", tri.nro_lados == 3)
    tri.agregar_lado(Lado(Punto(0, 0), Punto(1, 1)))
    check("Triangulo con 4 lados YA NO es valido (restriccion refinada)", not tri.estructura_valida)

    cl = Cuadrilatero()
    for i in range(4):
        cl.agregar_lado(Lado(Punto(i, 0), Punto(i + 1, 0)))
    check("Cuadrilatero con 4 lados es valido", cl.estructura_valida)
    check("Rectangulo hereda restriccion de 4 lados", Rectangulo().lados_esperados() == 4)

    compuesta = Cuadrado()
    compuesta.agregar_componente(tri)
    compuesta.agregar_componente(circ)
    check("Figura compuesta agrega 2 componentes", len(compuesta.componentes) == 2)
    check("Figura compuesta es_compuesta", compuesta.es_compuesta)
    check("Componente conoce su contenedora", tri.contenedora is compuesta)
    try:
        Cuadrado().agregar_componente(tri); rechazado = False
    except ValueError:
        rechazado = True
    check("Un componente no puede pertenecer a dos contenedoras (0..1)", rechazado)

    print(f"\n=== Resultado Ej.1: {_ok}/{_checks} verificaciones OK ===")


if __name__ == "__main__":
    main()
