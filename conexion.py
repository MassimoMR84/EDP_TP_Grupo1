from nodo import *

class Conexion:
    
    tiposDisponibles=("Ferroviaria", "Automotor", "Fluvial", "Aerea") #tupla porque no se pueden modificar
    
    def __init__(self, origen: Nodo, destino: Nodo, tipo: str, distancia: float, restriccion=None, valorRestriccion=None):
        Conexion.validarNodo(origen)
        self.origen=origen
        Conexion.validarNodo(destino)
        self.destino=destino
        Conexion.validarTipo(tipo)
        self.tipo=tipo
        Conexion.validarDistancia(distancia)
        self.distancia=distancia
        self.restriccion=restriccion
        self.valorRestriccion=valorRestriccion

    def __repr__(self): #método __repr__ para modificar el comportamoiento de la función print()
        return f"Origen: {self.origen}\nDestino: {self.destino}\nTipo: {self.tipo}\nDistancia: {self.distancia}\nRestricción: {self.restriccion}\nValor restrictivo: {self.valorRestriccion}\n"


    @staticmethod
    def validarNodo(nodo): #se valida que tanto el origen como el destino sean objetos de tipo Nodo
        if not isinstance(nodo, Nodo):
            raise TypeError("El origen y destino deben ser objetos de tipo Nodo")
        
    @staticmethod
    def validarTipo(tipo): #se valida que el tipo sea una cadena y que dicha cadena sea un tipo de transporte válido (uno de los que están presentes en la tupla inicial)
        if not isinstance(tipo,str):
            raise TypeError("El tipo debe ser una cadena")
        if tipo not in Conexion.tiposDisponibles:
            raise ValueError("El tipo de transporte debe ser uno de los siguientes: Ferroviaria, Automotor, Fluvial o Aerea")
        
    @staticmethod
    def validarDistancia(distancia: int):
        if not isinstance(distancia, int): #se asume que la distancia siempre será un número sin decimales en km
            raise TypeError("La distancia debe ser un número")
        if distancia<=0:
            raise ValueError("La distancia no puede ser menor o igual que cero")
        
def leer_conexiones(path, nodos: dict): #función para leer las conexiones del csv, se le pasan como parámetros el path del archivo y el diccionario de nodos obtenido con la función leer_nodos
    with open(path, newline='', encoding='utf-8') as f: #se abre el csv de nodos, urf-8 para leer el archivo correctamente
        reader = csv.DictReader(f) #se convierte cada fila en un diccionario
        for row in reader:
            origen = nodos.get(row['origen']) #se obtiene el nodo origen del diccionario de nodos
            destino = nodos.get(row['destino']) #se obtiene el nodo destino del diccionrio de nodos
            tipo = row['tipo']
            distancia = int(row['distancia_km']) #se lo convierte a int porque todos los valores se miden en km y no tienen decimales
            restriccion = row.get('restriccion') or None
            valor = row.get('valor_restriccion') or None #como puede haber restricción o no, valor y restricción pueden llegar a estar vacíos

            if origen and destino: #si el origen y el destino realmente son nodos y existen
                conexion = Conexion(origen, destino, tipo, distancia, restriccion, valor) #se instancia la conexión
                origen.agregarConexiones(conexion)  #se agrega la conexión al nodo origen


# nodos=leer_nodos("/Users/federicopedrotti/Desktop/Estructuras de Datos y Programación/EDP_TP_Grupo1/nodos.csv")
# conexiones=leer_conexiones("/Users/federicopedrotti/Desktop/Estructuras de Datos y Programación/EDP_TP_Grupo1/conexiones.csv",nodos)

# print(nodos["Buenos_Aires"].conexiones)
#Prueba funciona bien