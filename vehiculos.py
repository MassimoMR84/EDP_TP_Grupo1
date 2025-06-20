from validaciones import *
from funciones_auxiliares import *
from random import random

class Vehiculo:
    """
    Clase base para todos los vehículos de transporte.
    Define interfaz común y lógica de distribución de carga.
    """
    
    def __init__(self, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg):
        # Validar todos los parámetros
        validar_positivo(velocidad_nominal)
        validar_mayor_cero(capacidad_carga)
        validar_positivo(costo_fijo)
        validar_positivo(costo_km)
        validar_positivo(costo_kg)

        self.velocidad_nominal = velocidad_nominal
        self.capacidad_de_carga = capacidad_carga
        self.costo_fijo_uso = costo_fijo
        self.costo_km_recorrido = costo_km
        self.costo_kg_transportado = costo_kg
        self.modo_de_transporte = 'generico'

    def __str__(self):
        return (f"Modo: {self.modo_de_transporte}\n"
                f"Velocidad: {self.velocidad_nominal} km/h\n"
                f"Capacidad: {self.capacidad_de_carga} kg\n"
                f"Costo fijo: ${self.costo_fijo_uso}\n"
                f"Costo por km: ${self.costo_km_recorrido}\n"
                f"Costo por kg: ${self.costo_kg_transportado}")
        
    def getVelocidad(self):
        """Velocidad efectiva (puede ser sobrescrita por subclases)"""
        return self.velocidad_nominal
    
    def calcular_tiempo_decimal(self, distancia):
        """Calcula tiempo de viaje en horas decimales"""
        velocidad = self.getVelocidad()
        validar_positivo(distancia)
        validar_division_cero(velocidad)
        return distancia / velocidad
        
    def calcular_tiempo_tramo(self, distancia): 
        """Calcula tiempo en formato (horas, minutos)"""
        tiempo_decimal = self.calcular_tiempo_decimal(distancia)
        return horas_a_hs_y_min(tiempo_decimal)
    
    def calcular_costo_tramo(self, distancia, carga): 
        """
        Calcula costo total considerando múltiples vehículos si es necesario.
        Distribuye carga llenando vehículos al máximo antes de agregar otro.
        """
        validar_positivo(distancia)
        validar_positivo(carga)
        
        capacidad = self.capacidad_de_carga
        cargas_por_vehiculo = []
        
        # Define carga fija por carga transportada
        costo_total = 0
        
        # Algoritmo de distribución: llenar cada vehículo al máximo
        while carga > 0:
            if carga >= capacidad:  
                cargas_por_vehiculo.append(capacidad)
                carga -= capacidad
            else:
                cargas_por_vehiculo.append(carga)
                carga = 0
        
        # Calcular costo total por todos los vehículos
        cantidad_vehiculos = len(cargas_por_vehiculo)
        costo = (self.costo_fijo_uso * cantidad_vehiculos + 
                    self.costo_km_recorrido * distancia * cantidad_vehiculos)
            
        costo_total += costo  
     
        return costo_total
    
    def calcular_costo_por_carga(self, carga):
        validar_positivo(carga)
        costo_carga = self.costo_kg_transportado * carga
        return costo_carga
    
    def puede_transportar(self, peso_carga=0):
        """Verifica si puede transportar una carga (base: siempre True)"""
        return True


class Tren(Vehiculo):
    """
    Vehículo ferroviario de alta capacidad.
    Aplica descuentos por distancia (economías de escala).
    """
    
    def __init__(self,velocidad=100):
        try:
            velocidad=float(velocidad)
        except TypeError:
            velocidad=100.0
            
        super().__init__(velocidad_nominal=velocidad,   # km/h
                         capacidad_carga=150000,  # kg - muy alta capacidad
                         costo_fijo=100,          # $
                         costo_km=20,             # $/km
                         costo_kg=3)              # $/kg
        self.modo_de_transporte = 'ferroviaria'

    def calcular_costo_tramo(self, distancia, carga):
        """Aplica descuento del 25% para distancias largas (>200km)"""
        validar_positivo(distancia)
        validar_positivo(carga)    
        
        # CORREGIDO: Usar variable local en lugar de modificar self
        costo_km = self.costo_km_recorrido
        if distancia >= 200:
            costo_km = self.costo_km_recorrido * 0.75  # Descuento 25%
        
        capacidad = self.capacidad_de_carga
        cargas_por_vehiculo = []
        
        # Define carga fija por carga transportada
        costo_total = 0
        
        # Algoritmo de distribución: llenar cada vehículo al máximo
        while carga > 0:
            if carga >= capacidad:  
                cargas_por_vehiculo.append(capacidad)
                carga -= capacidad
            else:
                cargas_por_vehiculo.append(carga)
                carga = 0
        
        # Calcular costo total por todos los vehículos
        cantidad_vehiculos = len(cargas_por_vehiculo)
        costo = (self.costo_fijo_uso * cantidad_vehiculos + 
                    costo_km * distancia * cantidad_vehiculos)
            
        costo_total += costo  
     
        return costo_total


class Camion(Vehiculo):
    """
    Vehículo automotor flexible.
    Aplica sobrecosto para cargas pesadas (>15 toneladas).
    """
    
    def __init__(self):
        super().__init__(velocidad_nominal=80,     # km/h
                         capacidad_carga=30000,    # kg
                         costo_fijo=30,            # $
                         costo_km=5,               # $/km
                         costo_kg=1)               # $/kg
        self.modo_de_transporte = 'automotor'  
    
    def calcular_costo_por_carga(self, carga):
        validar_positivo(carga)
    
        capacidad = self.capacidad_de_carga
        cargas_por_vehiculo = []
        
        # Define carga fija por carga transportada
        costo_total = 0
        
        # Algoritmo de distribución: llenar cada vehículo al máximo
        while carga > 0:
            if carga >= capacidad:  
                cargas_por_vehiculo.append(capacidad)
                carga -= capacidad
            else:
                cargas_por_vehiculo.append(carga)
                carga = 0
        
        #Calcular costo por kg transportado por vehciulo
        costo_kg = self.costo_kg_transportado
        for carga_camion in cargas_por_vehiculo:
            if carga_camion > 15000:
                costo_kg = self.costo_kg_transportado*2  #Sobrecargo 100%
            else: 
                costo_kg = self.costo_kg_transportado
            costo_total += carga_camion*costo_kg 
                
        return costo_total
        

class Barco(Vehiculo):
    """
    Vehículo acuático con costos diferenciados.
    Fluvial: $500 base, Marítimo: $1500 base.
    """
    
    def __init__(self, tipo_navegacion='maritimo'):
        # Costo diferente según tipo de navegación
        if tipo_navegacion == 'fluvial':
            costo = 500   # Navegación en ríos
        else:
            costo = 1500  # Navegación marítima
            
        super().__init__(velocidad_nominal=40,      # km/h
                         capacidad_carga=100000,    # kg - alta capacidad
                         costo_fijo=costo,          # $ - variable según tipo
                         costo_km=15,               # $/km
                         costo_kg=2)                # $/kg
        
        self.modo_de_transporte = tipo_navegacion


class Avion(Vehiculo):
    """
    Vehículo aéreo de alta velocidad.
    Velocidad variable según condiciones climáticas.
    """
    
    def __init__(self, prob_mal_tiempo=0):
        super().__init__(velocidad_nominal=600,     # km/h - muy rápido
                         capacidad_carga=5000,      # kg - limitada
                         costo_fijo=750,            # $ - alto costo
                         costo_km=40,               # $/km - costoso
                         costo_kg=10)               # $/kg - el más caro
        
        self.modo_de_transporte = 'aerea'
        self.prob_mal_tiempo = prob_mal_tiempo
 
    def getVelocidad(self):
        """
        Velocidad efectiva considerando clima.
        Mal tiempo reduce velocidad de 600 a 400 km/h.
        """
        if random() <= self.prob_mal_tiempo:
            return 400  # Velocidad reducida por mal tiempo
        else:
            return self.velocidad_nominal  # Velocidad nominal


# Código de prueba
if __name__ == "__main__":
    print("Probando vehículos...")
    
    # Crear instancia de cada tipo
    camion = Camion()
    tren = Tren()
    barco = Barco('maritimo')
    avion = Avion(0.1) # type: ignore
    
    vehiculos = [camion, tren, barco, avion]
    
    # Probar con parámetros de ejemplo
    for vehiculo in vehiculos:
        print(f"\n--- {vehiculo.modo_de_transporte.upper()} ---")
        print(vehiculo)
        
        # Calcular métricas para 300km, 25000kg
        distancia_prueba = 300
        carga_prueba = 25000
        
        tiempo_tupla = vehiculo.calcular_tiempo_tramo(distancia_prueba)
        tiempo_decimal = vehiculo.calcular_tiempo_decimal(distancia_prueba)
        costo = vehiculo.calcular_costo_tramo(distancia_prueba, carga_prueba)
        
        print(f"Tiempo para {distancia_prueba}km: {tiempo_tupla}")
        print(f"Tiempo decimal: {tiempo_decimal:.2f}h")
        print(f"Costo para {carga_prueba}kg: ${costo:.2f}")
    
    print("\nPruebas completadas")

 
