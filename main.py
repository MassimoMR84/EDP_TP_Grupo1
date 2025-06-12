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

if __name__ == '__main__':
    #main()
    nodos=leer_nodos("nodos.csv")
    conexiones= leer_conexiones("conexiones.csv", nodos)
    print(conexiones)
