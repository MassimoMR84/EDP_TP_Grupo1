from conexion import *
from solicitud_transporte import *
from vehiculos import *
from nodo import *
import csv

class SistemaTransporte:
    def __init__(self):
        self.nodos = []
        self.conexiones = []
        self.solicitudes = []

    def __str__(self):
        return (f"Sistema de Transporte con {len(self.nodos)} nodos, {len(self.conexiones)} conexiones y {len(self.solicitudes)} solicitudes."
                f"\nNodos: {self.nodos}\n\nConexiones: {self.conexiones}\n\nSolicitudes: {self.solicitudes}")
        
    def agregar_nodo(self, nodo):
        self.nodos.append(nodo)

    def agregar_conexion(self, conexion):
        self.conexiones.append(conexion)

    def agregar_solicitud(self, solicitud):
        self.solicitudes.append(solicitud)
        
    def procesar_csv (self, file, tipo):
        print("Procesando archivo CSV de tipo:", tipo)
        
        if tipo == "nodo":
            """Procesa el archivo CSV para nodos"""
            lector = csv.DictReader(file)
            for row in lector:
                self.agregar_nodo (row)

        elif tipo == "conexion":
            """Procesa el archivo CSV para conexiones"""
            lector = csv.DictReader(file)
            for row in lector:
                self.agregar_conexion (row)

        elif tipo == "solicitudes":
            """Procesa el archivo CSV para solicitudes"""
            lector = csv.DictReader(file)
            for row in lector:
                self.agregar_solicitud (row)

        else:
            raise ValueError("Tipo no soportado. Use 'nodo', 'conexion' o 'solicitudes'.")

    def lector_csv(self, archivo, tipo = str ):
        '''Función para leer un archivo CSV '''
        with open (archivo, newline='', encoding='utf-8') as file:
            lector = self.procesar_csv(file, tipo) 
            return lector
        '''Procesa el lector CSV y devuelve una lista de elementos del tipo especificado'''

# Ejemplo de uso:
if __name__ == '__main__':
    try:
        ST = SistemaTransporte()
        ST.lector_csv('nodos.csv', "nodo")
        ST.lector_csv('conexiones.csv', "conexion")
        ST.lector_csv('solicitudes.csv', "solicitudes")

        print(ST)

    except ValueError as e:
        print("Error al procesar el CSV:", e)
