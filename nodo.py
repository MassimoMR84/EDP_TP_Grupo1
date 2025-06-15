from validaciones import validar_texto
from conexion import Conexion
import csv

class Nodo():
    """
    Representa una ciudad o punto clave en la red.
    Mantiene lista de conexiones salientes para navegación del grafo.
    """

    def __init__(self, nombre):
        self.nombre = validar_texto(nombre)
        self.conexiones = []  # Lista de conexiones salientes

    def __str__(self):
        return f"{self.nombre}"
    
    def __repr__(self):
        return f"{self.nombre}"

    def __eq__(self, otro): 
        """Dos nodos son iguales si tienen el mismo nombre"""
        return isinstance(otro, Nodo) and self.nombre == otro.nombre

    def __hash__(self): 
        """Permite usar nodos como claves de diccionario"""
        return hash(self.nombre)

    def agregarConexiones(self, conexion):
        """Agrega una conexión saliente al nodo"""
        self.conexiones.append(conexion)

    @staticmethod
    def leer_nodos(path):
        """
        Carga nodos desde archivo CSV con columna 'nombre'.
        Retorna diccionario {nombre: objeto_Nodo}.
        """
        nodos = {} 
        with open(path, newline='', encoding='utf-8') as f: 
            reader = csv.DictReader(f) 
            for row in reader:
                nombre = row['nombre']
                # Solo crear si no existe (evitar duplicados)
                if nombre not in nodos:
                    nodos[nombre] = Nodo(nombre) 
        return nodos
    
    @staticmethod
    def generar_conexiones(path, nodos):
        """
        Lee conexiones desde CSV y las asigna a nodos.
        Construye la estructura de grafo de la red.
        """
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                origen = row['origen'].strip()
                destino = row['destino'].strip()
                tipo = row['tipo']
                distancia = float(row['distancia_km'])
                # Restricciones opcionales
                restriccion = row.get('restriccion') or None
                valor = row.get('valor_restriccion') or None

                # Verificar que ambos nodos existan
                if origen in nodos and destino in nodos:
                    nodo_origen = nodos[origen]
                    nodo_destino = nodos[destino]
                    conexion = Conexion(nodo_origen, nodo_destino, tipo, distancia, restriccion, valor)
                    nodo_origen.agregarConexiones(conexion)
                else:
                    raise TypeError(f"Nodos no encontrados: {origen} o {destino}")