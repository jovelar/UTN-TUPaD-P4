#| Java-Ismo| Donde (Clase.metodo)|inversion que lo explica|Sintoma observable.

1| Uso de getters y setters| Figura.getNombre, Figura.getColor, Lado.getLongitud, Lado.setLongitud, Poligono.getlados|No se aprecian sintomas en ejecucion
2|Uso de Setter con validacion| lado.setLongitud| Getter/Setter preventivo|Ninguno en tiempo de ejecucion
3|Atributos deben definirse dentro del constructor|Poligono.catalogo|Encapsulamieto|Al definirse dentro de la clase y fuera del constuctor, cualquier cambio en cualquier instancia lo afecta.

5|Argumentos por defecto mutables|Poligono|De declaracion a runtime|
6|Type hints no validan
7|No llamar a super desde la clase hija|