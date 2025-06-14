from validaciones import *
from nodo import Nodo
import csv

class SolicitudTransporte:
    """Representa una solicitud de envío de carga"""
    
    def __init__(self, id_carga, peso_kg, origen, destino):
        self.id_carga = validar_texto(id_carga)
        self.peso_kg = validar_mayor_cero(peso_kg)
        origen, destino = validar_origen_destino(origen, destino)
        self.origen = origen
        self.destino = destino

    def __str__(self):
        return (f"IdCarga: #{self.id_carga} | Peso: {self.peso_kg} kg | "
                f"Origen: {self.origen} → Destino: {self.destino}")

    def __repr__(self):
        return f"Solicitud #{self.id_carga}"

    def __eq__(self, other):
        if not isinstance(other, SolicitudTransporte):
            raise TypeError('Ambos deben ser SolicitudTransporte')
        return self.id_carga == other.id_carga

    @staticmethod   
    def leer_solicitudes(file):
        """Lee solicitudes desde archivo CSV"""
        with open(file, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            return list(lector)
    
    @classmethod
    def cargar_solicitudes(cls, file):
        """Carga solicitudes desde CSV y las convierte a objetos"""
        datos = cls.leer_solicitudes(file)
        solicitudes = []
        for fila in datos:
            try:
                solicitud = SolicitudTransporte(
                    id_carga=fila['id_carga'], 
                    peso_kg=float(fila['peso_kg']), 
                    origen=fila['origen'], 
                    destino=fila['destino']
                )
                solicitudes.append(solicitud)
            except Exception as e:
                print(f"Error en fila {fila}: {e}")
        return solicitudes

if __name__ == '__main__':
    print("Probando solicitudes...")
    
    try:
        from nodo import Nodo
        
        n1 = Nodo("Buenos_Aires")
        n2 = Nodo("Rosario")
        s = SolicitudTransporte("CARGA-001", 1500, n1, n2)

        print(s)
        
        # Probar carga desde CSV
        try:
            solicitudes = SolicitudTransporte.cargar_solicitudes('solicitudes.csv')
            print("Solicitudes cargadas:")
            for solicitud in solicitudes:
                print(solicitud)
        except FileNotFoundError:
            print("Archivo solicitudes.csv no encontrado")
            
    except ValueError as e:
        print("Error:", e)
        
    print("Pruebas completadas")