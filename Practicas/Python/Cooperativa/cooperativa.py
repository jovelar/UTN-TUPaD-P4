"""Ej.4 — Cooperativa agrícola. Herencia real vs clasificación derivada; historial."""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class TipoMineral(Enum):
    PRIMARIO = "primario"
    SECUNDARIO = "secundario"


@dataclass(frozen=True)
class Mineral:
    nombre: str
    tipo: TipoMineral

    @property
    def es_primario(self) -> bool:
        return self.tipo is TipoMineral.PRIMARIO


class Cereal(ABC):
    """Herencia REAL {disjoint, complete}: tipo fijo e inmutable. Cereal * -- 1..* Mineral."""
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self._requeridos: set[Mineral] = set()

    def requiere_mineral(self, m: Mineral) -> None:
        self._requeridos.add(m)

    @property
    def requeridos(self) -> set[Mineral]:
        return set(self._requeridos)

    @abstractmethod
    def clasificacion(self) -> str: ...


class CosechaGruesa(Cereal):
    def clasificacion(self) -> str: return "Cosecha gruesa"


class CosechaFina(Cereal):
    def clasificacion(self) -> str: return "Cosecha fina"


class Pastura(Cereal):
    def clasificacion(self) -> str: return "Pastura"


class Lote:
    """Lote * -- * Mineral. es_especial() DERIVADO (no herencia). historico para regla de pastura."""
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self._contiene: set[Mineral] = set()
        self._historico: list[Cereal] = []

    def agregar_mineral(self, m: Mineral) -> None:
        self._contiene.add(m)

    @property
    def contiene(self) -> set[Mineral]:
        return set(self._contiene)

    @property
    def historico_siembra(self) -> list[Cereal]:
        return list(self._historico)

    @property
    def es_especial(self) -> bool:
        """Clasificación DERIVADA: especial si contiene algún mineral primario."""
        return any(m.es_primario for m in self._contiene)

    def satisface(self, c: Cereal) -> bool:
        """requiere ⊆ contiene [+ si es Pastura: no hubo pastura previa]."""
        if not c.requeridos <= self._contiene:
            return False
        if isinstance(c, Pastura):
            if any(isinstance(x, Pastura) for x in self._historico):
                return False
        return True

    def sembrar(self, c: Cereal) -> bool:
        if not self.satisface(c):
            return False
        self._historico.append(c)
        return True
