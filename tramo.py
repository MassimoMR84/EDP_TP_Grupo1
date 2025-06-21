from validaciones import validar_vehiculo, validar_positivo
from funciones_auxiliares import *

class Tramo:
    """
    Un segmento individual del viaje (vehículo entre dos nodos).
    Calcula automáticamente tiempo y costo basándose en el vehículo.
    """

    def __init__(self, vehiculo, origen, destino, distancia, carga=0):
        self.vehiculo = validar_vehiculo(vehiculo)
        self.origen = origen  
        self.destino = destino
        self.distancia = validar_positivo(distancia)
        self.carga = validar_positivo(carga)
        
        # Cálculos automáticos basados en el vehículo
        self.tiempo = self._calcular_tiempo_decimal()
        self.costo = self._calcular_costo()
    
    def _calcular_tiempo_decimal(self):
        """Delega cálculo al método del vehículo"""
        return self.vehiculo.calcular_tiempo_decimal(self.distancia)
    
    def _calcular_costo(self):
        """Delega cálculo al método del vehículo"""
        return self.vehiculo.calcular_costo_tramo(self.distancia, self.carga)
    
    def _obtener_nombre_nodo(self, nodo):
        """Extrae nombre del nodo de forma robusta"""
        if hasattr(nodo, 'nombre'):
            return nodo.nombre
        return str(nodo)
    
    def obtener_tiempo_formateado(self):
        """Retorna tiempo en formato (horas, minutos)"""
        return self.vehiculo.calcular_tiempo_tramo(self.distancia)
    
    def __str__(self):
        origen = self._obtener_nombre_nodo(self.origen)
        destino = self._obtener_nombre_nodo(self.destino)
        horas, minutos = self.obtener_tiempo_formateado()
        return f"{origen} -> {destino} ({self.vehiculo.modo_de_transporte}): {self.distancia}km, {horas}h {minutos}min, ${self.costo:.2f}"
    
    def __repr__(self):
        return self.__str__()