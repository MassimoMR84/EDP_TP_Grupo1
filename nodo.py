from validaciones import validar_texto
from conexion import Conexion
import csv

class Nodo():
    '''Representa una ciudad de la red'''

    def __init__(self, nombre:str):
        self.nombre = validar_texto(nombre)
        self.conexiones=[]
        '''Las conexiones de un nodo serán aquellos objetos conexión que tengan a ese nodo como origen'''

    def __str__(self):  #! Falta explicacion 
        return f"{self.nombre}"
    
    def __repr__(self):
        return f"{self.nombre}"

    def __eq__(self, otro): 
        '''Compara si dos nodos son iguales basandose en su nombre'''
        return isinstance(otro, Nodo) and self.nombre == otro.nombre

    def __hash__(self): 
        '''Permite que el nodo sea usado como clave en un diccionario'''
        return hash(self.nombre)

    def agregarConexiones(self, conexion):
        self.conexiones.append(conexion)