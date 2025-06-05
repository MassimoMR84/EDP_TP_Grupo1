from validaciones import *
from funciones import *

class Vehiculo:
    '''
    Clase que representa un vehiculo de transporte dentro del sistema
    Contiene informacion sobre su modo de transporte, velocidad, capacidad de carga y costos asociados
    '''
    def __init__(self, modo_de_transporte:str, velocidad_nominal:float, capacidad_de_carga:float, costo_fijo_uso, costo_km_recorrido, costo_kg_transportado):
        '''
        Inicializacion de un objeto Vehiculo
        Se validan todos los valores antes de asignarlos como atributos del objeto
        '''
        #validacion de modo de transporte
        validar_cadena(modo_de_transporte)
        validar_modo_de_transporte(modo_de_transporte)
        
        #validacion de velocidad nominal
        validar_numero_positivo(velocidad_nominal)
                
        #validacion de capacidad de carga
        validar_numero_mayor_a_cero(capacidad_de_carga)
        
        #validacion de costos
        validar_numero_positivo(costo_fijo_uso)
        validar_numero_positivo(costo_km_recorrido)
        validar_numero_positivo(costo_kg_transportado)
        
        #Construccion del init
        self.modo_de_transporte = modo_de_transporte
        self.velocidad_nominal = velocidad_nominal
        self.capacidad_de_carga = capacidad_de_carga
        self.costo_fijo_uso = costo_fijo_uso
        self.costo_km_recorrido = costo_km_recorrido
        self.costo_kg_transportado = costo_kg_transportado
        
    def __str__(self):
        '''
        Devuelve una representacion en forma de string del objeto Vehiculo
        '''
        return f"Vehículo tipo: {self.modo_de_transporte}\nVel: {self.velocidad_nominal} km/h\nCapacidad: {self.capacidad_de_carga} kg\nCosto fijo: ${self.costo_fijo_uso}\nCosto por km recorrido: ${self.costo_km_recorrido}\nCosto por kg transportado: ${self.costo_kg_transportado}"

    def calcular_tiempo_tramo(self, distancia): 
        '''
        Calcula el tiempo que tarda el vehiculo en recorrer una distancia dada
        Devuele el resultado en formato (horas, minutos)
        '''
        velocidad = self.velocidad_nominal
        validar_division_por_cero(velocidad)
        validar_numero_positivo(distancia)
        tiempo = distancia/velocidad
        horas, minutos = horas_a_hs_y_min(tiempo)
        return horas, minutos
    
    def calcular_costo_tramo(self, distancia, carga):
        '''
        Calcula el costo total de transportar una carga dada por una cierta distancia con el vehiculo
        Lanza un error si la carga supera la capacidad de carga maxima del vehiculo
        '''        
        #valido que distancia y peso sean numeros positivos
        validar_numero_positivo(distancia)
        validar_numero_positivo(carga) 
        
        #chequeo si la carga supera la carga maxima permitida
        if carga > self.capacidad_de_carga:
            raise ValueError(f'La carga de {carga} excede la capacidad de carga maxima del vehiculo que es de {self.capacidad_de_carga}')
        
        #calculo el costo total
        costo_total = self.costo_fijo_uso + self.costo_km_recorrido*distancia + self.costo_kg_transportado*carga
        return costo_total    
    
   