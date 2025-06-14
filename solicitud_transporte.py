from validaciones import *
from nodo import Nodo
import csv

class SolicitudTransporte:
    def __init__(self, id_carga: str, peso_kg: float, origen: Nodo, destino: Nodo):
        self.id_carga = validar_cadena (id_carga)
        self.peso_kg = validar_numero_mayor_a_cero (peso_kg)
        origen, destino = validar_origen_destino (validarNodo (origen), validarNodo (destino))  # Validamos que origen y destino no sean iguales
        self.origen = origen
        self.destino = destino

    def __str__(self):
        return (f"IdCarga: #{self.id_carga} | Peso: {self.peso_kg} kg | Origen: {self.origen} → "
                f"Destino: {self.destino}")


    def __eq__(self, other):
        if not isinstance(other,SolicitudTransporte):
            raise TypeError ('Ambos objetos deben ser de la clase SolicitudTransporte')
        if self.id_carga == other.id_carga:
            return True
        else:
            return False
        
    def leer_solicitudes(file):
        with open(file,'r',encoding='utf-8') as archivo:
            lector=csv.DictReader(archivo)
            return list(lector)
    
    
    
# Ejemplo de uso:
if __name__ == '__main__':
    try:
        from nodo import Nodo  # Importar la clase Nodo para crear instancias
        n1 = Nodo("Buenos Aires")
        n2 = Nodo("Rosario")
        s = SolicitudTransporte("CARGA-001", 1500, n1, n2)

        print(s)
    except ValueError as e:
        print("Error en la solicitud:", e)
