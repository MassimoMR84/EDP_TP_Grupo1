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

    @staticmethod
    def leer_nodos(path):
        '''Carga los nodos provenientes de un archivo csv de una columna denominada "nombre"
        Retorna diccionario de la forma {nombre: objeto_nodo}'''
        nodos = {} 
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
    
    @staticmethod
    def generar_conexiones(path, nodos: dict):
        '''función para leer las conexiones del csv, instanciar los objetos conexión a partir de eso 
        y agregarlos a los nodos correspondientes; se le pasan como parámetros el path del archivo 
        y el diccionario de nodos obtenido con la función leer_nodos'''

        with open(path, newline='', encoding='utf-8') as f:
            '''se abre el csv de nodos, utf-8 para leer el archivo correctamente'''
            reader = csv.DictReader(f)
            '''se convierte cada fila en un diccionario'''
            for row in reader:
                '''recorre las filas creadas'''
                origen = row['origen'].strip()
                '''se obtiene el nodo origen del diccionario de nodos'''
                destino = row['destino'].strip()
                '''se obtiene el nodo destino del diccionario de nodos'''
                tipo = row['tipo']
                distancia = float(row['distancia_km'])
                '''se lo convierte a int porque todos los valores se miden en km y no tienen decimales'''
                restriccion = row.get('restriccion') or None
                valor = row.get('valor_restriccion') or None
                '''como puede haber restricción o no, valor y restricción pueden llegar a estar vacíos'''

                if origen in nodos and destino in nodos:
                    '''si el origen y el destino realmente son nodos y existen'''
                    nodo_origen = nodos[origen]
                    nodo_destino = nodos[destino]
                    conexion = Conexion(nodo_origen, nodo_destino, tipo, distancia, restriccion, valor)
                    nodo_origen.agregarConexiones(conexion)
                    '''se agrega la conexión al nodo origen'''
                else:
                    raise TypeError(f"Las conexiones no se pudieron agregar a los nodos correspondientes. Nodo faltante: {origen} o {destino}")
            