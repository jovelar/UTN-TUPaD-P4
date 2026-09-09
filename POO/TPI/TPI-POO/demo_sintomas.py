#1. Atributo estatico
#"Javaismo" 3

class Familia:
    integrantes: list[str]=[]
    def __init__(self,apellido:str) -> None:
        self._apellido=apellido
    
    def agregar(self,nombre:str) -> None:
        self.integrantes.append(nombre)
        
    def mostrar(self)->None:
        for i in self.integrantes:
            print(self._apellido,", ",i)
            

gimenez=Familia("Gimenez")

gimenez.agregar("Pablo")
gimenez.agregar("Pepe")
gimenez.agregar("Pipo")

hernandez=Familia("Hernandez")
hernandez.agregar("Lidia")
hernandez.agregar("Lucia")
hernandez.agregar("Lucrecia")

#Al pretender mostrar los integrantes de la familia Hernandez, muestra tambien los de Gimenez
hernandez.mostrar()