from validaciones import validar_cadena

class Nodo():

    def __init__(self, nombre:str):
        self.nombre = validar_cadena(nombre) #falta validacion
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
        '''Permite que el nodo sea usado como clave en un diccionario o en un set'''
        return hash(self.nombre)

    def agregarConexiones(self, conexion):
        self.conexiones.append(conexion)
        

import csv

def leer_nodos(path):   #! Juntar los lectores en un solo archivo y en una funcion
    nodos = {} 
    '''diccionario para almacenar los datos: key: nombre del nodo--> value: objeto nodo con ese nombre'''
    with open(path, newline='', encoding='utf-8') as f: 
        '''se abre el csv de nodos, urf-8 para leer el archivo correctamente'''
        reader = csv.DictReader(f) 
        '''se convierte cada fila en un diccionario'''
        for row in reader:
            '''recorre las filas creadas'''
            nombre = row['nombre']
            if nombre not in nodos:
                nodos[nombre] = Nodo(nombre) 
                '''se crea un nodo si no estaba ya creado'''
    return nodos 
'''devuelve el diccionario con los nodos del csv'''

