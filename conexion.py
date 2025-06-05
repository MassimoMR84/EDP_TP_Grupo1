from validaciones import *
from nodo import *

class Conexion:
    '''Clase Conexión: contiene el nodo origen, el nodo destino, la distancia entre ellos, la restricción (si la hay) 
    y el valor de la restricción (si corresponde)'''

    def __init__(self, origen: Nodo, destino: Nodo, tipo: str, distancia: int, restriccion=None, valorRestriccion=None):
        Conexion.validarNodo(origen)
        self.origen=origen
        Conexion.validarNodo(destino)
        self.destino=destino
        validar_cadena(tipo)
        validar_modo_de_transporte(tipo)
        self.tipo=tipo
        validar_numero_mayor_a_cero(distancia)
        self.distancia=distancia
        self.restriccion=restriccion
        self.valorRestriccion=valorRestriccion

    def __repr__(self):
        '''método __repr__ para modificar el comportamoiento de la función print()'''
        return f"Origen: {self.origen}\nDestino: {self.destino}\nTipo: {self.tipo}\nDistancia: {self.distancia}\nRestricción: {self.restriccion}\nValor restrictivo: {self.valorRestriccion}\n"


    @staticmethod
    def validarNodo(nodo):
        '''se valida que tanto el origen como el destino sean objetos de tipo Nodo'''
        if not isinstance(nodo, Nodo):
            raise TypeError("El origen y destino deben ser objetos de tipo Nodo")
        
        
def leer_conexiones(path, nodos: dict): 
    '''función para leer las conexiones del csv, se le pasan como parámetros el path del archivo y el diccionario de nodos 
    obtenido con la función leer_nodos'''
    with open(path, newline='', encoding='utf-8') as f: 
        '''se abre el csv de nodos, urf-8 para leer el archivo correctamente'''
        reader = csv.DictReader(f) 
        '''se convierte cada fila en un diccionario'''
        for row in reader:
            origen = nodos.get(row['origen']) 
            '''se obtiene el nodo origen del diccionario de nodos'''
            destino = nodos.get(row['destino']) 
            '''se obtiene el nodo destino del diccionrio de nodos'''
            tipo = row['tipo']
            distancia = int(row['distancia_km']) 
            '''se lo convierte a int porque todos los valores se miden en km y no tienen decimales'''
            restriccion = row.get('restriccion') or None
            valor = row.get('valor_restriccion') or None 
            '''como puede haber restricción o no, valor y restricción pueden llegar a estar vacíos'''

            if origen and destino: 
                '''si el origen y el destino realmente son nodos y existen'''
                conexion = Conexion(origen, destino, tipo, distancia, restriccion, valor)
                '''se instancia la conexión'''
                origen.agregarConexiones(conexion)
                '''se agrega la conexión al nodo origen'''