#| Java-Ismo| Donde (Clase.metodo)|inversion que lo explica|Sintoma observable.

1| Uso de getters y setters| Figura.getNombre, Figura.getColor, Lado.getLongitud, Lado.setLongitud, Poligono.getlados|De imposicion al acuerdo|No se aprecian sintomas en ejecucion
2|Uso de Setter con validacion| lado.setLongitud| De imposicion al acuerdo|Ninguno en tiempo de ejecucion
3|Atributos deben definirse dentro del constructor|Poligono.catalogo|De declaracion al tiempo de ejecucion|Al definirse dentro de la clase y fuera del constuctor, cualquier cambio en cualquier instancia lo afecta.

5|Argumentos por defecto mutables|Poligono|De declaracion a runtime|Sin sintomas observables
7|No llamar a super desde la clase hija|Poligono.__init__|De la declaracion al runtime|La instancia se realiza pero no completamente, provocando error al consultar por ciertos atributos
6|Type hints no validan|De imposicion a acuerdo|Poligono.area|No hay sintomas observables
8|Intento de implementar sobrecarga de constructor|Triangulo.__init__,Cuadrado.__init__|de declaracion al runtime|No muestra sintoma alguno