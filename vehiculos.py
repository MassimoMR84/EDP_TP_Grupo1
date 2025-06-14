from validaciones import *
from funciones_auxiliares import *
from random import random

class Vehiculo:
    """Clase base para todos los vehículos de transporte"""
    
    def __init__(self, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg):
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
        return self.velocidad_nominal
    
    def calcular_tiempo_decimal(self, distancia):
        """Calcula tiempo de viaje en horas decimales"""
        velocidad = self.getVelocidad()
        validar_positivo(distancia)
        validar_division_cero(velocidad)
        return distancia / velocidad
        
    def calcular_tiempo_tramo(self, distancia): 
        """Calcula tiempo de viaje y lo retorna como tupla (horas, minutos)"""
        tiempo_decimal = self.calcular_tiempo_decimal(distancia)
        return horas_a_hs_y_min(tiempo_decimal)
    
    def calcular_costo_tramo(self, distancia, carga): 
        """Calcula costo total considerando múltiples vehículos si es necesario"""
        validar_positivo(distancia)
        validar_positivo(carga)
        
        capacidad = self.capacidad_de_carga
        cargas_por_vehiculo = []
        
        # Distribuir carga entre vehículos
        while carga > 0:
            if carga >= capacidad:  
                cargas_por_vehiculo.append(capacidad)
                carga -= capacidad
            else:
                cargas_por_vehiculo.append(carga)
                carga = 0
        
        # Calcular costo total
        costo_total = 0
        for carga_vehiculo in cargas_por_vehiculo:
            costo = (self.costo_fijo_uso + 
                    self.costo_km_recorrido * distancia + 
                    self.costo_kg_transportado * carga_vehiculo)
            costo_total += costo  
     
        return costo_total
    
    def puede_transportar(self, peso_carga=0):
        """Por defecto todos los vehículos pueden transportar"""
        return True
    
class Tren(Vehiculo):
    def __init__(self):
        super().__init__(velocidad_nominal = 100,
                         capacidad_carga = 150000,
                         costo_fijo = 100,
                         costo_km = 20,
                         costo_kg = 3)        
        self.modo_de_transporte = 'ferroviaria'
   
    def calcular_costo_tramo(self, distancia, carga):
        validar_positivo(distancia)
        validar_positivo(carga)    
        
        # Descuento para distancias largas
        if distancia < 200:
            self.costo_km_recorrido = 20
        else:
            self.costo_km_recorrido = 15      
        return super().calcular_costo_tramo(distancia, carga)
       
       
class Camion(Vehiculo):
    def __init__(self):
        super().__init__(velocidad_nominal = 80,
                         capacidad_carga = 30000,
                         costo_fijo = 30,
                         costo_km = 5,
                         costo_kg = 1)      
        self.modo_de_transporte = 'automotor'    
       
    def calcular_costo_tramo(self, distancia, carga):
        validar_positivo(distancia)
        validar_positivo(carga)    
        
        # Costo extra para cargas pesadas
        if carga < 15000:
            self.costo_kg_transportado = 1
        else:
            self.costo_kg_transportado = 2    
        return super().calcular_costo_tramo(distancia, carga)
    
    
class Barco(Vehiculo):
    def __init__(self, tipo_navegacion='maritimo'):
        # Costo diferente según tipo de navegación
        if tipo_navegacion == 'fluvial':
            costo = 500
        else:
            costo = 1500       
        super().__init__(velocidad_nominal = 40,
                         capacidad_carga = 100000,
                         costo_fijo = costo, 
                         costo_km = 15,
                         costo_kg = 2)        
        self.modo_de_transporte = tipo_navegacion 

class Avion(Vehiculo):
    def __init__(self, prob_mal_tiempo = 0):
        super().__init__(velocidad_nominal = 600,
                         capacidad_carga = 5000,
                         costo_fijo = 750,
                         costo_km = 40,
                         costo_kg = 10)        
        self.modo_de_transporte = 'aerea'
        self.prob_mal_tiempo = prob_mal_tiempo
 
    def getVelocidad(self):
        # Velocidad reducida con mal tiempo
        if random() <= self.prob_mal_tiempo:
            return 400
        else:
            return 600

if __name__ == "__main__":
    print("Probando vehículos...")
    
    # Crear vehículos
    camion = Camion()
    tren = Tren()
    barco = Barco('maritimo')
    avion = Avion(0.1) # type: ignore
    
    vehiculos = [camion, tren, barco, avion]
    
    # Probar cada vehículo
    for vehiculo in vehiculos:
        print(f"\n--- {vehiculo.modo_de_transporte.upper()} ---")
        print(vehiculo)
        
        # Calcular para distancia y carga de prueba
        distancia_prueba = 300
        carga_prueba = 25000
        
        tiempo_tupla = vehiculo.calcular_tiempo_tramo(distancia_prueba)
        tiempo_decimal = vehiculo.calcular_tiempo_decimal(distancia_prueba)
        costo = vehiculo.calcular_costo_tramo(distancia_prueba, carga_prueba)
        
        print(f"Tiempo para {distancia_prueba}km: {tiempo_tupla}")
        print(f"Tiempo decimal: {tiempo_decimal:.2f}h")
        print(f"Costo para {carga_prueba}kg: ${costo:.2f}")
    
    print("\nPruebas completadas")