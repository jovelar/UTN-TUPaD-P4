#1. Atributo estatico
#"Javaismo" 3
#Atributo definido fuera del constructor se vuelve static, siendo compartido por todas las instancias
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


#2 Uso de super

#Si no se llama a super, el objeto se construye a media, siendo algunos atributos como
#el contruido ignorados, causando error en ejecucion al averiguar su estado
class Fruta:
    def __init__(self,peso,color):
        self._peso=peso
        self._color=color
        self.construido=True

class Banana(Fruta):
    def __init__(self,peso,color):
        self._peso=peso
        self._color=color
        
        
fruta_generica=Fruta("Rojo",200)

print("\n\n",fruta_generica.construido)

banana_ecuatoriana=Banana("Amarillo",350)
print("\n\n",banana_ecuatoriana.construido)