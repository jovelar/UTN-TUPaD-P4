# TP Integrador — Unidad 3 — POO

Trabajo Práctico Integrador de Programación IV (TUPaD - UTN): dominio Figura / Polígono / Lado
traducido de Java a Python, aplicando encapsulamiento por convención, herencia justificada por
dominio, composición/agregación/asociación, y contratos estructurales (Protocol) vs ABC.

## Qué resuelve cada archivo

| Archivo | Qué resuelve |
|---|---|
| `parte1_diagnostico.py` | Parte 1: los 8 java-ismos de diseño diagnosticados y corregidos sobre el dominio original, con el antes/después de la única property justificada (`Lado.longitud`). |
| `figuras.py` | Dominio completo y funcional (Partes 1 a 4): `Figura`, `Poligono` (ABC), `Triangulo`/`Cuadrado`/`Pentagono`/`Hexagono`, `Taller` (agregación), `Etiqueta` (asociación, `@dataclass(frozen=True)`), y el contrato `Exportable` (`Protocol`) con la función `exportar_todo`. Importa `libreria_externa` sin modificarla. |
| `libreria_externa.py` | Clase `PlanoCAD` de terceros, entregada sin modificar — cumple `Exportable` estructuralmente, sin heredar de nada propio. |
| `demo_sintomas.py` | Demuestra 2 de los 8 java-ismos de la Parte 1 de forma reproducible (atributo de clase compartido, y `__init__` que no llama a `super()`). |
| `main.py` | Demo ejecutable: arma un `Taller` con 4 polígonos (uno de cada subclase), etiqueta 2 lados, exporta una lista mixta de polígonos y un `PlanoCAD`, muestra el inventario, y demuestra falla temprana (instanciar `Poligono` abstracto) y agregación (un polígono sobrevive a `Taller.restaurar()`). |
| `informe.md` | Tabla de los 8 java-ismos, tabla de equivalencias Java↔Python, la decisión sobre `PoligonoRegular` (descartada por redundante), y las respuestas de las Partes 2 y 4. |
| `uml/modelo_final.md` | Diagrama de clases final (Mermaid), reflejando las decisiones de las Partes 3 y 4. |

## Cómo ejecutar

python main.py
python demo_sintomas.py