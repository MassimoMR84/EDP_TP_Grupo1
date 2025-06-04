from nodo import *
from conexion import *
from vehiculos import *

class RedTransporte:
    '''
    Clase que representa la red de transporte del sistema
    Contiene los nodos, las conexiones y los vehiculos del sistema
    '''
    def __init__(self):
        self.nodos = {}
        self.conexiones = [] # podria ser un set? 
        self.vehiculos = []
    
    def agregar_nodo(self,nodo):
        if not isinstance(nodo,Nodo):
            raise ValueError('El nodo debe ser un objeto de tipo Nodo.')
        if nodo.nombre not in self.nodos:
            self.nodos[nodo.nombre] = nodo

    def agregar_conexiones(self,conexion):
        if not isinstance(conexion,Conexion):
            raise ValueError('La conexion debe ser un objeto de tipo Conexion')
        if conexion not in self.conexiones: 
            self.conexiones.append(conexion)

    def agregar_vehiculos(self,vehiculo):
        if not isinstance(vehiculo,Vehiculo):
            raise ValueError('La conexion debe ser un objeto de tipo Conexion')
        if vehiculo not in self.vehiculos: 
            self.vehiculos.append(vehiculo)
