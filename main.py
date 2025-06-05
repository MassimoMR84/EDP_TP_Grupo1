import csv
def leer_csv(file):
    with open(file,'r',encoding='utf-8') as archivo:
        lector=csv.DictReader(archivo)
        return list(lector)

print(leer_csv('conexiones.csv'))


'''BORRAR LO DE ABAJO (estamos probando que funcione)'''
from nodo import Nodo
from conexion import leer_nodos, leer_conexiones
from red_transporte import RedTransporte
from planificador import Planificador

# 1. Leer los nodos y conexiones desde CSV
nodos = leer_nodos("nodos.csv")
leer_conexiones("conexiones.csv", nodos)

# 2. Crear red y cargar los nodos
red = RedTransporte()
for nodo in nodos.values():
    red.agregar_nodo(nodo)

# 3. Crear el planificador
planificador = Planificador(red)

# 4. Seleccionar nodos desde el diccionario
origen = red.nodos["Zarate"]
destino = red.nodos["Mar del Plata"]

# 5. Buscar rutas posibles
rutas = planificador.buscar_rutas(origen, destino)

# 6. Mostrar resultados
print(f"\nSe encontraron {len(rutas)} rutas desde {origen.nombre} hasta {destino.nombre}:\n")
for i, ruta in enumerate(rutas, 1):
    nombres = " → ".join(n.nombre for n in ruta)
    print(f"{i}. {nombres}")
