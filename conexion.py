from validaciones import *

class Conexion:
    """
    Representa una ruta entre dos nodos con posibles restricciones.
    Encapsula información de distancia, tipo de transporte y limitaciones.
    """
    
    def __init__(self, origen, destino, tipo, distancia, restriccion=None, valorRestriccion=None):
        self.origen = origen
        self.destino = destino
        self.tipo = validar_modo_transporte(tipo)
        self.distancia = validar_mayor_cero(distancia)
        
        # Procesar restricciones opcionales
        self.restriccion = restriccion.strip() if restriccion and restriccion.strip() else None
        self.valorRestriccion = None
        
        if self.restriccion and valorRestriccion:
            self.valorRestriccion = validar_restriccion_conexion(self.restriccion, valorRestriccion)

    def __str__(self):
        base = f"Conexión de {self.origen} a {self.destino} ({self.tipo}): {self.distancia} km"
        if self.restriccion and self.valorRestriccion is not None:
            base += f" | Restricción: {self.restriccion} = {self.valorRestriccion}"
        return base

    def __repr__(self): 
        if self.restriccion is None or self.valorRestriccion is None:
            return f"Origen:{self.origen}\nDestino:{self.destino}\nModo: {self.tipo}\nDistancia: {self.distancia}\nSin restricciones\n\n"
        else:
            return f"Origen:{self.origen}\nDestino:{self.destino}\nModo: {self.tipo}\nDistancia: {self.distancia}\nRestricción:{self.restriccion}\nValor: {self.valorRestriccion}\n\n"

    def __eq__(self, otra_conexion):
        """Dos conexiones son iguales si conectan los mismos nodos con el mismo modo"""
        return (isinstance(otra_conexion, Conexion) 
                and self.origen == otra_conexion.origen 
                and self.destino == otra_conexion.destino 
                and self.tipo == otra_conexion.tipo)

    def aplica_restriccion(self, vehiculo): 
        """Verifica si un vehículo puede usar esta conexión"""
        if not self.restriccion or self.valorRestriccion is None:
            return True
        
        # Restricción de velocidad máxima (principalmente trenes)
        if self.restriccion == "velocidad_max":
            if hasattr(vehiculo, 'velocidad_nominal'):
                return vehiculo.velocidad_nominal <= float(self.valorRestriccion)
            return True
        
        return True  # Otras restricciones se manejan en el planificador
        
    def es_compatible_con_carga(self, peso_carga):
        """
        Verifica si una carga puede pasar por esta conexión.
        Principalmente para restricciones de peso en puentes.
        """
        if self.restriccion == "peso_max" and self.valorRestriccion is not None:
            try:
                peso_maximo = float(self.valorRestriccion)
                return peso_carga <= peso_maximo
            except (ValueError, TypeError):
                return True
        return True
    
    def obtener_velocidad_efectiva(self, vehiculo):
        """Calcula velocidad considerando restricciones de la conexión"""
        velocidad_base = vehiculo.getVelocidad() if hasattr(vehiculo, 'getVelocidad') else vehiculo.velocidad_nominal
        
        if self.restriccion == "velocidad_max" and self.valorRestriccion is not None:
            try:
                velocidad_max = float(self.valorRestriccion)
                return min(velocidad_base, velocidad_max)
            except (ValueError, TypeError):
                return velocidad_base
        
        return velocidad_base
    
    def obtener_info_restriccion(self):
        """Genera descripción legible de las restricciones"""
        if not self.restriccion or self.valorRestriccion is None:
            return "Sin restricciones"
        
        if self.restriccion == "velocidad_max":
            return f"Velocidad máxima: {self.valorRestriccion} km/h"
        elif self.restriccion == "peso_max":
            return f"Peso máximo: {self.valorRestriccion} kg"
        elif self.restriccion == "tipo":
            return f"Tipo de navegación: {self.valorRestriccion}"
        elif self.restriccion == "prob_mal_tiempo":
            return f"Probabilidad de mal tiempo: {float(self.valorRestriccion)*100:.1f}%"
        else:
            return f"{self.restriccion}: {self.valorRestriccion}"