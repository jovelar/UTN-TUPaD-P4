## 1

| # | Java-Ismo | Donde (Clase.metodo) | Inversion que lo explica | Sintoma observable |
|---|---|---|---|---|
| 1 | Uso de getters y setters | Figura.getNombre, Figura.getColor, Lado.getLongitud, Lado.setLongitud, Poligono.getlados | De imposicion al acuerdo | No se aprecian sintomas en ejecucion |
| 2 | Uso de Setter con validacion "tipo java"| lado.setLongitud | De imposicion al acuerdo | Ninguno en tiempo de ejecucion |
| 3 | Atributos deben definirse dentro del constructor | Poligono.catalogo | De declaracion al tiempo de ejecucion | Al definirse dentro de la clase y fuera del constructor, cualquier cambio en cualquier instancia lo afecta |
|4| codigo que simula un stream|Perimetro.sum| de imposicion al acuerdo| Ninguno al ejecutar|
| 5 | Argumentos por defecto mutables | Poligono (parametros constructor) | De declaracion a runtime | Sin sintomas observables |
| 6 | Type hints no validan | Poligono.area | De imposicion a acuerdo | No hay sintomas observables |
| 7 | No llamar a super desde la clase hija | `Poligono.__init__` | De la declaracion al runtime | La instancia se realiza pero no completamente, provocando error al consultar por ciertos atributos |
| 8 | Intento de implementar sobrecarga de constructor | `Triangulo.__init__`, `Cuadrado.__init__` | De declaracion al runtime | No muestra sintoma alguno |

## 2.1
 Se implemanta la funcionalidad del metodo .restaurar(). Desvincula poligonos del taller pero no los elimina.

## 3
 se opta por utilizar la clase Poligono y descartar Poligono_regular por ser conceptualmente redundante.


## 4.
 La diferencia en codigo de como se ve la agregacion y la composicion es simple:
 * En la **agregacion**, se recibe por parametro en el constructor el objeto que se va a asociar, asi mismo hay un atributo (unico, lista) que refuerza ademas el tipo de relacion.

  ```
    //Ambos objetos se crean al mismo nivel
    taller1 = Taller()
    lados_c = c.lados

    print("\nAgregando figuras al taller\n")
    taller1.recibir(c)

    //Taller tiene un metodo recibir, que asocia una figura
    def recibir(self,poligono):
        self._poligonos.append(poligono)
 ```
 * En la **Composicion**, se reciben los parametros para crear el objeto a asociar en el constructor, y se crea dentro del mismo.

    ```
        class Poligono(Figura,ABC):
            catalogo = []
            def __init__(self, nombre, color, lados=None, observaciones=None):
            ...
            self._lados = list(lados) if lados is not None else []
    ```
 * En la **asociacion** ambos objetos se crean al mismo nivel, pero al meno uno de ellos tiene un atributos que indica la relacion. Luego se asocia invocando al parametro, metodo o property:

 ```
    lados_t = t.lados
    lados_t[0].etiqueta = Etiqueta("borde exterior")
 ```


## 4.3
 No funcionaria con el caso de PlanoCad sin modificar por que no hace falta herencia, con que cumpla con Protocol es suficiente. Ademas por consignas no se puede modificar la clase PlanoCad.

La eleccion entre ABC y protocol la decide el dominio: 
 * En circunstancias donde se sea propietario se puede utilizar ABC, como en las partes 3. En ese caso particular es necesario que se valide las implementaciones al crearse, y una clase abstracta es ideal para eso.
 * Al no ser propietario, como en la parte 4, se puede compensar utilizando Protocol.


## Tabla de equivalencias

|Elemento en Java|Como quedo en tu codigo de Python|Traduccion directa o rediseño?|por que?|
|---|---|---|---|
|Getters y setters|Acceso directo por defecto (si no contiene _), uso de @property cuando hay que implementar logica|Rediseño|Por que es codigo boilerplate y en python solamente se incorpora cuando sea necesario y no "por las dudas" como se realiza en java|
|Sobrecarga de constructores|constructor unico y metodos adicionales que pueden tomar su lugar como tal con la anotacion @classmethod|Rediseño| Porque pithon no soporta sobrecarga|
|Interfaces|Uso de protocol|rediseño|Por que puede operar de forma similar, a pesar que no es una alternativa analoga: La clase que implementa el protocol no la conoce y la evaluacion para con ducktyping se realiza "desde afuera"|
|Static|atributo de clae|traduccion|Es una alternativa que opera analogamente igual|
|modificador Private/Protected|Uso de la convencion _ delante del nombre de cada atributo privado|Rediseño|Por que el interprete de python no lo impone. Es un acuerdo entre desarrolladores para interpretar el atributo como privado|



## Cierre
Mas alla de la diferencias de sintaxis es el cambio de contrato:

 * En java se aplica el encapsulamiento, es decir, se accesde a los atributos de una clase mediante getters y setters, mientras que en python se realiza directamente y/o con el uso de @property cuando sea necesario

 * La reduccion casi total de codigo boilerplate, escribiendo lo necesario solo cuando haga falta, y con @dataclass.

 * El uso de ducktyping para "suplantar" a las interfaces, aunque estas operan de forma diferente: no son obligatorias, la clase que hace uso de ella no la conoce, y se evaluan "desde afuera", para ver si es candidata. Solo importa que compartan la misma firma de metodo.