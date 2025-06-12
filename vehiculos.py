from validaciones import *
from funciones import *

class Vehiculo:
    '''
    Creacion de la clase Vehiculo. Contiene informacion sobre su modo de transporte, velocidad, capacidad de carga y costos asociados
    '''
    def __init__(self, velocidad_nominal:float, capacidad_de_carga:float, costo_fijo_uso: float, costo_km_recorrido: float, costo_kg_transportado: float):
        # Validaciones
        validar_numero_positivo(velocidad_nominal)
        validar_numero_mayor_a_cero(capacidad_de_carga)
        validar_numero_positivo(costo_fijo_uso)
        validar_numero_positivo(costo_km_recorrido)
        validar_numero_positivo(costo_kg_transportado)

        # Atributos
        self.velocidad_nominal = velocidad_nominal
        self.capacidad_de_carga = capacidad_de_carga
        self.costo_fijo_uso = costo_fijo_uso
        self.costo_km_recorrido = costo_km_recorrido
        self.costo_kg_transportado = costo_kg_transportado

    def __str__(self):  
        '''
        Devuelve una representacion en forma de string del objeto Vehiculo
        '''
        return (f"Vel: {self.velocidad_nominal} km/h\n"
                f"Capacidad: {self.capacidad_de_carga} kg\n"
                f"Costo fijo: ${self.costo_fijo_uso}\n"
                f"Costo por km recorrido: ${self.costo_km_recorrido}\n"
                f"Costo por kg transportado: ${self.costo_kg_transportado}")
        
    def calcular_tiempo_tramo(self, distancia): 
        '''
        Calcula el tiempo que tarda el vehiculo en recorrer una distancia dada
        '''
        velocidad = self.velocidad_nominal
        validar_numero_positivo(distancia)
        validar_division_por_cero(velocidad)
        tiempo = distancia/velocidad
        return horas_a_hs_y_min(tiempo) # --> Tupla (horas, minutos)
    
    def calcular_costo_tramo(self, distancia, carga): 
        '''
        Calcula el costo total de transportar una carga dada por una cierta distancia con la cantidad de vehiculos necesarios
        '''
        # Validaciones
        validar_numero_positivo(distancia)
        validar_numero_positivo(carga)
        
        capacidad = self.capacidad_de_carga
        cargas_por_vehiculo = []
        
        #Se divide la carga total en partes, llenado cada vehiculo excepto el ultimo
        while carga > 0:
            if carga >= capacidad:  
                cargas_por_vehiculo.append(capacidad)
                carga -= capacidad
            else:
                cargas_por_vehiculo.append(carga)
                carga = 0
        
        #Calculamos el costo por tramo por vehiculo contemplando su carga
        costo_total = 0
        for carga in cargas_por_vehiculo:
            costo = (self.costo_fijo_uso + self.costo_km_recorrido * distancia + self.costo_kg_transportado * carga)
            costo_total += costo  
     
        return (costo_total)
    
class Tren(Vehiculo):
    def __init__(self):
        super().__init__(velocidad_nominal = 100, 
                         capacidad_de_carga = 150000,
                         costo_fijo_uso = 100, 
                         costo_km_recorrido = None, 
                         costo_kg_transportado = 3)        
        self.modo_de_transporte = 'ferroviaria'
   
    def calcular_costo_tramo(self, distancia, carga): 
        # Validaciones
        validar_numero_positivo(distancia)
        validar_numero_positivo(carga)    
        
        if distancia < 20:
            costo_km_recorrido = 20
        else:
            costo_km_recorrido = 15
        
        return costo_km_recorrido
        
        
class Auto(Vehiculo):
    def __init__(self):
        super().__init__(velocidad_nominal = 80, 
                         capacidad_de_carga = 30000,
                         costo_fijo_uso = 30, 
                         costo_km_recorrido = 5, 
                         costo_kg_transportado = None)        
        self.modo_de_transporte = 'automotor'    
        
        


class Barco(Vehiculo):
    def __init__(self):
        super().__init__(velocidad_nominal = 40, 
                         capacidad_de_carga = 100000,
                         costo_fijo_uso = None, 
                         costo_km_recorrido = 15, 
                         costo_kg_transportado = 2)        
        self.modo_de_transporte = 'fluvial'

class Avion(Vehiculo):
    def __init__(self):
        super().__init__(velocidad_nominal = None, 
                         capacidad_de_carga = 5000,
                         costo_fijo_uso = 750, 
                         costo_km_recorrido = 40, 
                         costo_kg_transportado = 10)        
        self.modo_de_transporte = 'aereo'
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
'''Ejemplo de uso'''
if __name__ == "__main__":
    try:
        v = Vehiculo('fluvial', 30, 30, 32, 24, 12)
        print(v)

        horas, minutos = v.calcular_tiempo_tramo(20)
        print(f"Tiempo de viaje: {horas} horas y {minutos} minutos")
        
        costo = v.calcular_costo_tramo(200, 20)
        print(f'Costo del tramo: ${costo}')

    except (ValueError, TypeError) as e:
        print(e)