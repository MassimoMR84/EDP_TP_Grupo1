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


# Código de prueba
if __name__ == "__main__":
    print("Probando conexiones con restricciones...")
    
    try:
        from nodo import Nodo
        
        # Crear nodos de prueba
        zarate = Nodo("Zarate")
        buenos_aires = Nodo("Buenos_Aires")
        junin = Nodo("Junin")
        
        print("Nodos creados:")
        print(f"- {zarate}")
        print(f"- {buenos_aires}")
        print(f"- {junin}")
        
        # Crear conexiones con diferentes restricciones
        print(f"\nCreando conexiones...")
        
        # Conexión ferroviaria con velocidad máxima
        conexion1 = Conexion(zarate, buenos_aires, "Ferroviaria", 85, "velocidad_max", "80")
        print(f"OK {conexion1}")
        print(f"   {conexion1.obtener_info_restriccion()}")
        
        # Conexión automotor con peso máximo
        conexion2 = Conexion(zarate, junin, "Automotor", 185, "peso_max", "15000")
        print(f"OK {conexion2}")
        print(f"   {conexion2.obtener_info_restriccion()}")
        
        # Conexión fluvial con tipo específico
        conexion3 = Conexion(zarate, buenos_aires, "Fluvial", 85, "tipo", "fluvial")
        print(f"OK {conexion3}")
        print(f"   {conexion3.obtener_info_restriccion()}")
        
        # Conexión aérea con probabilidad de mal tiempo
        conexion4 = Conexion(junin, buenos_aires, "Aerea", 238, "prob_mal_tiempo", "0.1")
        print(f"OK {conexion4}")
        print(f"   {conexion4.obtener_info_restriccion()}")
        
        # Probar compatibilidad con cargas
        print(f"\nProbando cargas:")
        cargas_test = [10000, 20000]
        for carga in cargas_test:
            compatible = conexion2.es_compatible_con_carga(carga)
            resultado = "OK" if compatible else "NO"
            print(f"Carga {carga}kg en conexión automotor: {resultado}")
        
        print("\nPruebas completadas")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()