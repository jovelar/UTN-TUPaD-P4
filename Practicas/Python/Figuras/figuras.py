"""Ej.1 — Figuras geométricas. Herencia en profundidad, composición vs. agregación, derivados."""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from math import hypot, pi


@dataclass(frozen=True)
class Punto:
    """Punto del plano. Inmutable: no tiene vida propia fuera de un Lado."""
    x: float
    y: float

    def distancia(self, otro: "Punto") -> float:
        return hypot(self.x - otro.x, self.y - otro.y)


@dataclass(frozen=True)
class Lado:
    """Composición de EXACTAMENTE 2 Puntos (Lado *-- 2 Punto)."""
    inicio: Punto
    fin: Punto

    @property
    def longitud(self) -> float:            # atributo derivado
        return self.inicio.distancia(self.fin)


class Figura(ABC):
    """Raíz {disjoint, incomplete}. Agregación reflexiva: una figura puede componerse de otras."""

    def __init__(self) -> None:
        self._componentes: list[Figura] = []
        self._contenedora: Figura | None = None

    def agregar_componente(self, f: "Figura") -> None:
        if f is self:
            raise ValueError("Una figura no puede componerse de sí misma")
        if f._contenedora is not None:
            raise ValueError("La figura ya pertenece a otra contenedora")
        f._contenedora = self
        self._componentes.append(f)

    @property
    def componentes(self) -> list["Figura"]:
        return list(self._componentes)

    @property
    def contenedora(self) -> "Figura | None":
        return self._contenedora

    @property
    def es_compuesta(self) -> bool:
        return bool(self._componentes)

    @abstractmethod
    def tipo(self) -> str: ...


class Poligono(Figura):
    """Composición Poligono *-- 3..* Lado. nro_lados es DERIVADO. Subclases refinan la cantidad."""

    def __init__(self) -> None:
        super().__init__()
        self._lados: list[Lado] = []

    def agregar_lado(self, lado: Lado) -> None:
        self._lados.append(lado)

    @property
    def nro_lados(self) -> int:              # derivado
        return len(self._lados)

    @property
    def perimetro(self) -> float:            # derivado
        return sum(l.longitud for l in self._lados)

    @abstractmethod
    def lados_esperados(self) -> int:
        """Cantidad exacta de lados que exige la subclase; -1 = solo mínimo 3."""

    @property
    def estructura_valida(self) -> bool:
        esperados = self.lados_esperados()
        if esperados == -1:
            return self.nro_lados >= 3           # regla general 3..*
        return self.nro_lados == esperados       # restricción refinada


class Triangulo(Poligono):
    def lados_esperados(self) -> int: return 3
    def tipo(self) -> str: return "Triangulo"


class Cuadrilatero(Poligono):
    def lados_esperados(self) -> int: return 4
    def tipo(self) -> str: return "Cuadrilatero"


class Rectangulo(Cuadrilatero):
    def tipo(self) -> str: return "Rectangulo"


class Cuadrado(Rectangulo):
    def tipo(self) -> str: return "Cuadrado"


class Elipse(Figura):
    def __init__(self, semi_mayor: float, semi_menor: float) -> None:
        super().__init__()
        self.semi_mayor = semi_mayor
        self.semi_menor = semi_menor

    @property
    def area(self) -> float:
        return pi * self.semi_mayor * self.semi_menor

    def tipo(self) -> str: return "Elipse"


class Circulo(Elipse):
    """Un círculo ES una elipse con ambos semiejes iguales (radio)."""
    def __init__(self, radio: float) -> None:
        super().__init__(radio, radio)

    @property
    def radio(self) -> float:
        return self.semi_mayor

    def tipo(self) -> str: return "Circulo"
