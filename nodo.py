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


# Código de prueba
if __name__=="__main__":
    print("Probando nodos...")
    
    # Prueba de carga desde archivos
    print("\n=== Carga desde Archivos ===")
    try:
        nodos = Nodo.leer_nodos("nodos.csv")
        print(f"✓ Nodos cargados: {list(nodos.keys())}")
        
        try:
            Nodo.generar_conexiones("conexiones.csv", nodos)
            
            # Mostrar información de Buenos Aires si existe
            if 'Buenos_Aires' in nodos:
                ba_nodo = nodos['Buenos_Aires']
                print(f"✓ Conexiones desde Buenos_Aires: {len(ba_nodo.conexiones)}")
                
                # Mostrar primeras 3 conexiones
                for i, conexion in enumerate(ba_nodo.conexiones[:3]):
                    print(f"  {i+1}. {conexion}")
                
                if len(ba_nodo.conexiones) > 3:
                    print(f"  ... y {len(ba_nodo.conexiones) - 3} más")
            
        except FileNotFoundError:
            print("✗ Archivo conexiones.csv no encontrado")
        except Exception as e:
            print(f"✗ Error cargando conexiones: {e}")
            
    except FileNotFoundError:
        print("✗ Archivo nodos.csv no encontrado")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Pruebas de operaciones básicas
    print("\n=== Operaciones Básicas ===")
    
    # Crear nodos de prueba
    nodo1 = Nodo("TestCity1")
    nodo2 = Nodo("TestCity2")
    nodo3 = Nodo("TestCity1")  # Mismo nombre que nodo1
    
    print(f"✓ Nodo1: {nodo1}")
    print(f"✓ Nodo2: {nodo2}")
    print(f"✓ nodo1 == nodo3: {nodo1 == nodo3}")  # True (mismo nombre)
    print(f"✓ nodo1 == nodo2: {nodo1 == nodo2}")  # False (diferente nombre)
    
    # Prueba de uso en conjunto (requiere __hash__)
    conjunto_nodos = {nodo1, nodo2, nodo3}
    print(f"✓ Nodos únicos en conjunto: {len(conjunto_nodos)}")  # Debería ser 2
    
    # Prueba como clave de diccionario
    distancias = {nodo1: 100, nodo2: 200}
    print(f"✓ Distancia a {nodo1}: {distancias[nodo1]} km")
    
    print("\n=== Pruebas completadas ===")