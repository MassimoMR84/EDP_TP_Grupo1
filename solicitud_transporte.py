from validaciones import *
from nodo import Nodo
import csv

class SolicitudTransporte:
    """
    Solicitud individual de envío que especifica qué transportar y dónde.
    Define la demanda que el sistema debe resolver con itinerarios optimizados.
    """
    def __init__(self, id_carga: str, peso_kg: float, origen: Nodo, destino: Nodo):
        self.id_carga = validar_texto(id_carga)
        self.peso_kg = validar_mayor_cero(peso_kg)
        # Valida que origen y destino sean diferentes
        origen, destino = validar_origen_destino(origen, destino)
        self.origen = origen
        self.destino = destino

    def __str__(self):
        return (f"IdCarga: #{self.id_carga} | Peso: {self.peso_kg} kg | Origen: {self.origen} → "
                f"Destino: {self.destino}")

    def __repr__(self):
        return (f"Solicitud #{self.id_carga}")

    def __eq__(self, other):
        """Dos solicitudes son iguales si tienen el mismo ID"""
        if not isinstance(other, SolicitudTransporte):
            raise TypeError('Ambos deben ser SolicitudTransporte')
        return self.id_carga == other.id_carga

    
# Código de prueba
if __name__ == '__main__':
    print("Probando solicitudes...")
    
    # Creación manual
    print("\n=== Creación Manual ===")
    try:
        from nodo import Nodo
        
        n1 = Nodo("Buenos_Aires")
        n2 = Nodo("Rosario")
        s = SolicitudTransporte("CARGA-001", 1500, n1, n2)

        print(f"✓ Solicitud creada: {s}")
        print(f"✓ Repr técnica: {repr(s)}")
        
    except ValueError as e:
        print(f"✗ Error de validación: {e}")
    
    # Carga desde archivo CSV
    print("\n=== Carga desde CSV ===")
    try:
        solicitudes = SolicitudTransporte.cargar_solicitudes('solicitudes.csv')
        print(f"✓ Solicitudes cargadas: {len(solicitudes)}")
        for solicitud in solicitudes:
            print(f"  - {solicitud}")
            
    except FileNotFoundError:
        print("✗ Archivo solicitudes.csv no encontrado")
        print("  Formato esperado: id_carga,peso_kg,origen,destino")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Validaciones y casos de error
    print("\n=== Validaciones ===")
    try:
        from nodo import Nodo
        n1 = Nodo("CityA")
        n2 = Nodo("CityB")
        
        # Caso válido
        s1 = SolicitudTransporte("TEST-001", 100, n1, n2)
        print(f"✓ {s1}")
        
        # Casos de error
        try:
            SolicitudTransporte("TEST-002", 0, n1, n2)  # Peso cero
        except ValueError as e:
            print(f"✓ Error esperado (peso cero): {e}")
        
        try:
            SolicitudTransporte("TEST-003", 100, n1, n1)  # Mismo origen/destino
        except ValueError as e:
            print(f"✓ Error esperado (mismo origen/destino): {e}")
        
        # Prueba de comparación
        s2 = SolicitudTransporte("TEST-001", 200, n2, n1)  # Mismo ID
        print(f"✓ s1 == s2: {s1 == s2}")  # True (mismo ID)
        
        s3 = SolicitudTransporte("TEST-004", 100, n1, n2)  # Diferente ID
        print(f"✓ s1 == s3: {s1 == s3}")  # False (diferente ID)
        
    except Exception as e:
        print(f"✗ Error en validaciones: {e}")
        
    print("\n=== Pruebas completadas ===")
