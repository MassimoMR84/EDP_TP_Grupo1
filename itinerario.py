from validaciones import *
from funciones import *
from nodo import Nodo
from vehiculos import Vehiculo


class Tramo:
    """Un tramo es basicamente un pedazo del viaje completo"""
    
    def __init__(self, vehiculo, nodo_origen, nodo_destino, distancia, carga=0):
        # validaciones basicas
        if not isinstance(vehiculo, Vehiculo):
            raise TypeError("El vehículo debe ser una instancia de la clase Vehiculo")
        validar_numero_positivo(distancia)
        validar_numero_positivo(carga)
        
        # datos del tramo
        self.vehiculo = vehiculo
        self.nodo_origen = nodo_origen  # puede ser objeto Nodo o string, da igual
        self.nodo_destino = nodo_destino  
        self.distancia = distancia  # en km
        self.carga = carga  # en kg
        
        # calculo automatico usando los metodos del vehiculo
        self.tiempo = self._calcular_tiempo_decimal()
        self.costo = self._calcular_costo()
    
    def _calcular_tiempo_decimal(self):
        """convierte el tiempo a decimal para que sea mas facil de trabajar"""
        horas, minutos = self.vehiculo.calcular_tiempo_tramo(self.distancia)
        return horas + (minutos / 60)
    
    def _calcular_costo(self):
        """usa el metodo del vehiculo para calcular cuanto sale"""
        return self.vehiculo.calcular_costo_tramo(self.distancia, self.carga)
    
    def _obtener_nombre_nodo(self, nodo):
        """saca el nombre del nodo, no importa si es objeto o string"""
        if hasattr(nodo, 'nombre'):  # es un objeto Nodo
            return nodo.nombre
        return str(nodo)  # es un string
    
    def obtener_tiempo_formateado(self):
        """devuelve el tiempo en formato (horas, minutos) que es mas legible"""
        return self.vehiculo.calcular_tiempo_tramo(self.distancia)
    
    def __str__(self):
        origen = self._obtener_nombre_nodo(self.nodo_origen)
        destino = self._obtener_nombre_nodo(self.nodo_destino)
        horas, minutos = self.obtener_tiempo_formateado()
        return f"{origen} -> {destino} ({self.vehiculo.modo_de_transporte}): {self.distancia}km, {horas}h {minutos}min, ${self.costo:.2f}"
    
    def __repr__(self):
        return self.__str__()


class Itinerario:
    """Representa todo el plan de viaje completo"""
    
    def __init__(self, kpi_usado="tiempo"):
        # valido que el KPI sea correcto
        validar_cadena(kpi_usado)
        if kpi_usado not in ["tiempo", "costo"]:
            raise ValueError("KPI debe ser 'tiempo' o 'costo'")
        
        # inicializo todo en vacio
        self.tramos = []
        self.costo_total = 0.0
        self.tiempo_total = 0.0
        self.kpi_usado = kpi_usado
    
    def _obtener_nombre_nodo(self, nodo):
        """mismo metodo que en Tramo, saca el nombre del nodo"""
        if hasattr(nodo, 'nombre'):  
            return nodo.nombre
        return str(nodo)  
    
    def agregar_tramo(self, tramo):
        """agrega un tramo nuevo al itinerario"""
        if not isinstance(tramo, Tramo):
            raise TypeError("El tramo debe ser una instancia de la clase Tramo")
        
        # chequeo que los tramos se conecten bien
        if self.tramos:
            ultimo_destino = self._obtener_nombre_nodo(self.tramos[-1].nodo_destino)
            nuevo_origen = self._obtener_nombre_nodo(tramo.nodo_origen)
            if nuevo_origen != ultimo_destino:
                print(f"Advertencia: El tramo no es continuo. Último destino: {ultimo_destino}, Nuevo origen: {nuevo_origen}")
        
        # evito ciclos basicos (sino termino dando vueltas)
        if self._tiene_ciclo_basico(tramo):
            destino_nombre = self._obtener_nombre_nodo(tramo.nodo_destino)
            raise ValueError(f"Se detectó un ciclo: el nodo {destino_nombre} ya fue visitado")
        
        self.tramos.append(tramo)
        self.calcular_totales()
    
    def _tiene_ciclo_basico(self, nuevo_tramo):
        """chequea que no vuelva a un nodo que ya visite"""
        nodos_visitados = set()
        
        # junto todos los nodos que ya pase
        for tramo in self.tramos:
            nodos_visitados.add(self._obtener_nombre_nodo(tramo.nodo_origen))
        
        # si ya tengo tramos, agrego el ultimo destino tambien
        if self.tramos:
            nodos_visitados.add(self._obtener_nombre_nodo(self.tramos[-1].nodo_destino))
        
        # veo si el nuevo destino ya lo visite antes
        nuevo_destino = self._obtener_nombre_nodo(nuevo_tramo.nodo_destino)
        return nuevo_destino in nodos_visitados
    
    def calcular_totales(self):
        """recalcula los totales cada vez que agrego un tramo"""
        self.costo_total = sum(tramo.costo for tramo in self.tramos)
        self.tiempo_total = sum(tramo.tiempo for tramo in self.tramos)
    
    def obtener_distancia_total(self):
        """suma todas las distancias"""
        return sum(tramo.distancia for tramo in self.tramos)
    
    def obtener_carga_total(self):
        """suma toda la carga que transporto"""
        return sum(tramo.carga for tramo in self.tramos)
    
    def obtener_ruta_completa(self):
        """devuelve la lista de nodos por los que paso"""
        if not self.tramos:
            return []
        
        ruta = [self._obtener_nombre_nodo(self.tramos[0].nodo_origen)]
        for tramo in self.tramos:
            ruta.append(self._obtener_nombre_nodo(tramo.nodo_destino))
        return ruta
    
    def obtener_vehiculos_utilizados(self):
        """que vehiculos use en el viaje"""
        return [tramo.vehiculo.modo_de_transporte for tramo in self.tramos]
    
    def __str__(self):
        if not self.tramos:
            return "Itinerario vacío"
        
        resultado = "=" * 50
        resultado += f"\nITINERARIO DE TRANSPORTE\n"
        resultado += "=" * 50
        resultado += f"\nCriterio de optimización: {self.kpi_usado.upper()}\n"
        resultado += f"Ruta: {' -> '.join(self.obtener_ruta_completa())}\n"
        resultado += f"\nDETALLE DE TRAMOS:\n"
        resultado += "-" * 50
        
        for i, tramo in enumerate(self.tramos, 1):
            resultado += f"\n{i}. {tramo}"
        
        resultado += f"\n\nRESUMEN:\n"
        resultado += "-" * 50
        resultado += f"\nTotal de tramos: {len(self.tramos)}"
        resultado += f"\nDistancia total: {self.obtener_distancia_total():.1f} km"
        resultado += f"\nCarga total: {self.obtener_carga_total():.1f} kg"
        
        # formateo el tiempo para que se vea bien
        horas_totales = int(self.tiempo_total)
        minutos_totales = int((self.tiempo_total - horas_totales) * 60)
        resultado += f"\nTiempo total: {horas_totales}h {minutos_totales}min"
        
        resultado += f"\nCosto total: ${self.costo_total:.2f}"
        resultado += f"\nVehículos utilizados: {', '.join(set(self.obtener_vehiculos_utilizados()))}"
        resultado += f"\nKPI optimizado: {self.kpi_usado}"
        resultado += "\n" + "=" * 50
        
        return resultado
    
    def __repr__(self):
        return f"Itinerario(tramos={len(self.tramos)}, kpi='{self.kpi_usado}', costo=${self.costo_total:.2f}, tiempo={self.tiempo_total:.1f}h)"


# (bloque de prueba)
# if __name__ == "__main__":
#     print("PRUEBA DEL SISTEMA DE ITINERARIOS")
    
#     try:
#         # creo algunos vehiculos para probar
#         camion = Vehiculo("automotor", 80.0, 25000.0, 500.0, 2.5, 0.05)
#         tren = Vehiculo("ferroviario", 60.0, 100000.0, 1200.0, 1.8, 0.02)
        
#         # y algunos nodos
#         ba = Nodo("Buenos Aires")
#         rosario = Nodo("Rosario")
#         cordoba = Nodo("Córdoba")
        
#         # armo un itinerario
#         itinerario = Itinerario(kpi_usado="tiempo")
        
#         # agrego un par de tramos
#         tramo1 = Tramo(camion, ba, rosario, 300, 15000)
#         tramo2 = Tramo(tren, rosario, cordoba, 400, 80000)
        
#         itinerario.agregar_tramo(tramo1)
#         itinerario.agregar_tramo(tramo2)
        
#         # veo como quedo
#         print(itinerario)
        
#         print("\nPrueba exitosa - Sistema funcionando correctamente")
        
#     except Exception as e:
#         print(f"Error en la prueba: {e}")