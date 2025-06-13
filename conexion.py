from validaciones import *
from nodo import *
from SistemaTransporte import *
import csv

class Conexion:
    '''Clase Conexión: contiene el nodo origen, el nodo destino, la distancia entre ellos, la restricción (si la hay) 
    y el valor de la restricción (si corresponde)'''

    
    def __init__(self, origen: Nodo, destino: Nodo, tipo: str, distancia: int, restriccion=None, valorRestriccion=None):
        validarNodo(origen)
        self.origen = origen
        validarNodo(destino)
        self.destino = destino
        self.tipo = validar_modo_de_transporte(tipo)
        self.distancia = validar_numero_mayor_a_cero(distancia)
        self.restriccion = restriccion
        self.valorRestriccion = valorRestriccion

    def __str__ (self):
        base = f"Conexión de {self.origen} a {self.destino} ({self.tipo}): {self.distancia} km"
        if self.restriccion:
            base += f" | Restricción: {self.restriccion} = {self.valorRestriccion}"
        return base

    def __repr__(self): #! Poner mas corto e intuitivo
        if self.restriccion is None:
            return f"Origen:{self.origen}\nDestino:{self.destino}\nModo de transporte: {self.tipo}\nDistancia: {self.distancia}\nNo hay restricciones en esta conexion\n\n"
        else:
            return f"Origen:{self.origen}\nDestino:{self.destino}\nModo de transporte: {self.tipo}\nDistancia: {self.distancia}\n Restricción:{self.restriccion}\nValor restrictivo: {self.valorRestriccion}\n\n"

    def aplica_restriccion(self, vehiculo): 
        '''Verifica si un vehículo cumple con las restricciones de la conexión'''
        if not self.restriccion:
            return True
        
        atributo = getattr(vehiculo, self.restriccion, None)
        if atributo is None:
            return False

        return atributo >= float(self.valorRestriccion)
        
        
def procesar_conexiones(path, nodos: dict): #! Juntar los lectores en un solo archivo y en una funcion
    '''función para leer las conexiones del csv, instanciar los objetos conexión a partir de eso y agregarlos a los nodos correspondientes; se le pasan como parámetros el path del archivo y el diccionario de nodos 
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
                if isinstance(conexion, Conexion):
                    '''se chequea que la conexión realmente sea un objeto de dicha clase'''
                    origen.agregarConexiones(conexion)
                    '''se agrega la conexión al nodo origen'''
                else:
                    raise TypeError("Las conexiones no se pudieron agregar a los nodos correspondientes")



'''Prueba de funcionamiento local'''
if __name__ == "__main__":
    nodos=leer_nodos("nodos.csv")
    print(nodos)

    leer_conexiones("conexiones.csv", nodos)
    print(nodos["Buenos_Aires"].conexiones)
    '''Clases nodo y conexión funcionan OK'''