from validaciones import *
from funciones import *
from random import random
from conexion import * 

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
        
    def getVelocidad(self):
        return self.velocidad_nominal
        
    def calcular_tiempo_tramo(self, distancia): 
        '''
        Calcula el tiempo que tarda el vehiculo en recorrer una distancia dada
        '''
        velocidad = self.getVelocidad()
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
    
    def puede_transportar(self):
        '''
        Se asume que todos los vehiculos pueden transportar.
        En las subclases necesarias se tiene en cuenta si hay restricciones especificas'''
        return True
    
class Tren(Vehiculo):
    def __init__(self):
        super().__init__(velocidad_nominal = 100,
                         capacidad_de_carga = 150000,
                         costo_fijo_uso = 100,
                         costo_km_recorrido = 20, #valor 20 arbitrario (puede cambiar dsps)
                         costo_kg_transportado = 3)        
        self.modo_de_transporte = 'ferroviaria'
   
    def calcular_costo_tramo(self, distancia, carga):
        # Validaciones
        validar_numero_positivo(distancia)
        validar_numero_positivo(carga)    
        if distancia < 20:
            self.costo_km_recorrido = 20
        else:
            self.costo_km_recorrido = 15      
        return super().calcular_costo_tramo(distancia, carga)
       
       
class Camion(Vehiculo):
    def __init__(self):
        super().__init__(velocidad_nominal = 80,
                         capacidad_de_carga = 30000,
                         costo_fijo_uso = 30,
                         costo_km_recorrido = 5,
                         costo_kg_transportado = 1)  #valor 1 arbitrario (puede cambiar dsps)      
        self.modo_de_transporte = 'automotor'    
       
    def calcular_costo_tramo(self, distancia, carga):
        # Validaciones
        validar_numero_positivo(distancia)
        validar_numero_positivo(carga)    
        if carga < 15000:
            self.costo_kg_transportado = 1
        else:
            self.costo_kg_transportado = 2    
        return super().calcular_costo_tramo(distancia, carga)

    '''
    def puede_transportar(self, conexion): #PASAR A CONEXION (pasa cm atributo cantiad d kilos q se estan pasando)
        
        #Evalua si la capacidad del camion no supera el peso meximo permitido.
        #Devuelve True si el camion puede circular por el tramo
       
        from conexion import Conexion #lo importo adentro xq me hace ciruclar sino (MIRAR)
        
        if not isinstance(conexion, Conexion):
            raise TypeError('Tipo de dato invalido. Debe ser una conexion')
        
        if conexion.restriccion == "peso_max":
            try:
                peso_maximo = float(conexion.valorRestriccion)
                return self.capacidad_de_carga <= peso_maximo
            except (TypeError, ValueError) as e:
                print (e)
        else:
            return True
    '''
    
    
class Barco(Vehiculo):
    def __init__(self, modo_de_transporte):
        if modo_de_transporte == 'fluvial':
            costo = 500
        else:
            costo = 1500       
        super().__init__(velocidad_nominal = 40,
                         capacidad_de_carga = 100000,
                         costo_fijo_uso = costo, 
                         costo_km_recorrido = 15,
                         costo_kg_transportado = 2)        
        self.modo_de_transporte = modo_de_transporte 

class Avion(Vehiculo):
    def __init__(self, prob_mal_tiempo):
        #velocidad = 600 - 200*prob_mal_tiempo (PREGUNTAR Q FORMA VA)
        super().__init__(velocidad_nominal = 600,
                         capacidad_de_carga = 5000,
                         costo_fijo_uso = 750,
                         costo_km_recorrido = 40,
                         costo_kg_transportado = 10)        
        self.modo_de_transporte = 'aereo'
        if prob_mal_tiempo == None:
            prob_mal_tiempo = 0
        self.prob_mal_tiempo = prob_mal_tiempo
 
    def getVelocidad(self):
        if random() <= self.prob_mal_tiempo:
            velocidad = 400
        else:
            velocidad = 600
        return velocidad
 
 


if __name__ == "__main__":
        from nodo import Nodo
        from conexion import Conexion
        # Simular nodos y conexiones
        origen = Nodo("Zarate")
        destino = Nodo("Buenos Aires")

        conexion_camion = Conexion(origen, destino, tipo="automotor", distancia=100,
                                   restriccion="peso_max", valorRestriccion="25000")

        conexion_avion = Conexion(origen, destino, tipo="aerea", distancia=300,
                                  restriccion="prob_mal_tiempo", valorRestriccion="malo")

        conexion_barco = Conexion(origen, destino, tipo="maritimo", distancia=500)

        print("\n--- CAMION ---")
        camion = Camion()
        print(camion)
        print("¿Puede transportar por conexión?:", camion.puede_transportar(conexion_camion))
        print("Costo para 75.000 kg y 100 km:", camion.calcular_costo_tramo(100, 75000))

        print("\n--- TREN ---")
        tren = Tren()
        print(tren)
        print("Costo para 300.000 kg y 250 km:", tren.calcular_costo_tramo(250, 300000))

        print("\n--- BARCO ---")
        barco = Barco()
        print(barco)
        print("Costo para 200.000 kg y 500 km:", barco.calcular_costo_tramo(500, 200000, conexion=conexion_barco))

        print("\n--- AVION ---")
        avion = Avion()
        print(avion)
        tiempo = avion.calcular_tiempo_tramo(300, conexion=conexion_avion)
        print("Tiempo de vuelo con mal clima (300 km):", tiempo)

 
