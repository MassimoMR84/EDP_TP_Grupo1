from SistemaTransporte import SistemaTransporte
from nodo import *
from conexion import *

def main():
    sistema = SistemaTransporte()
    # Leer nodos
    sistema.lector_csv('nodos.csv', 'nodo')
    # Leer conexiones
    sistema.lector_csv('conexiones.csv', 'conexion')
    # Leer solicitudes
    sistema.lector_csv('solicitudes.csv', 'solicitudes')
    
    # Imprimir el sistema para verificar los datos cargados
    print(sistema)



#inicializamos red de transporte y probamos todo
#NADA DE LOGICA SOLO EJECUTA
