from validaciones import *

class Nodo():
    
    def __init__(self, nombre:str):
        validar_cadena(nombre)
        self.nombre=nombre
        self.conexiones=[] #lista de conexiones; se elige una lista ya que se va a almacenar un conjunto de datos que pueden variar duarnte la ejecución
                            # (se agregan conexiones cuando se lee el csv) y no se usa una pila o una cola porque no hace fakta utilizar lógicas como FIFO 
                            # o LIFO; por eso la lista parece ser lo más adecuado

    def agregarConexiones(self, conexion):
        self.conexiones.append(conexion) #método de instancia para agregar una conexión a un nodo
    
    def __repr__(self):
        return f"{self.nombre}" #método __repr__ para modificar el comportamoiento de la función print()
        

import csv

def leer_nodos(path):
    nodos = {} #diccionario para almacenar los datos: key: nombre del nodo--> value: objeto nodo con ese nombre
    with open(path, newline='', encoding='utf-8') as f: #se abre el csv de nodos, urf-8 para leer el archivo correctamente
        reader = csv.DictReader(f) #se convierte cada fila en un diccionario
        for row in reader: #recorre las filas creadas
            nombre = row['nombre']
            if nombre not in nodos:
                nodos[nombre] = Nodo(nombre) #se crea un nodo si no estaba ya creado
    return nodos #devuelve el diccionario con los nodos del csv

