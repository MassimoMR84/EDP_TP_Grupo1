from validaciones import validar_texto
from conexion import Conexion
import csv

class Nodo():
    """Representa una ciudad o punto de la red de transporte"""

    def __init__(self, nombre):
        self.nombre = validar_texto(nombre)
        self.conexiones = []

    def __str__(self):
        return f"{self.nombre}"
    
    def __repr__(self):
        return f"{self.nombre}"

    def __eq__(self, otro): 
        """Compara nodos por nombre"""
        return isinstance(otro, Nodo) and self.nombre == otro.nombre

    def __hash__(self): 
        """Permite usar nodos como claves de diccionario"""
        return hash(self.nombre)

    def agregarConexiones(self, conexion):
        self.conexiones.append(conexion)

    @staticmethod
    def leer_nodos(path):
        """Lee nodos desde archivo CSV"""
        nodos = {} 
        with open(path, newline='', encoding='utf-8') as f: 
            reader = csv.DictReader(f) 
            for row in reader:
                nombre = row['nombre']
                if nombre not in nodos:
                    nodos[nombre] = Nodo(nombre) 
        return nodos
    
    @staticmethod
    def generar_conexiones(path, nodos):
        """Lee conexiones desde CSV y las asigna a los nodos"""
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                origen = row['origen'].strip()
                destino = row['destino'].strip()
                tipo = row['tipo']
                distancia = float(row['distancia_km'])
                restriccion = row.get('restriccion') or None
                valor = row.get('valor_restriccion') or None

                if origen in nodos and destino in nodos:
                    nodo_origen = nodos[origen]
                    nodo_destino = nodos[destino]
                    conexion = Conexion(nodo_origen, nodo_destino, tipo, distancia, restriccion, valor)
                    nodo_origen.agregarConexiones(conexion)
                else:
                    raise TypeError(f"Nodos no encontrados: {origen} o {destino}")

if __name__=="__main__":
    print("Probando nodos...")
    nodos = Nodo.leer_nodos("nodos.csv")
    print("Nodos cargados:", list(nodos.keys()))
    
    try:
        Nodo.generar_conexiones("conexiones.csv", nodos)
        print("Conexiones de Buenos_Aires:", len(nodos['Buenos_Aires'].conexiones))
    except FileNotFoundError:
        print("Archivos CSV no encontrados")
    except Exception as e:
        print(f"Error: {e}")
        
    print("Pruebas completadas")