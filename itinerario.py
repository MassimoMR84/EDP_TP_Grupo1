from validaciones import *
from funciones_auxiliares import *
from nodo import Nodo
from vehiculos import Vehiculo

class Tramo:
    """Un segmento del viaje completo"""

    def __init__(self, vehiculo, origen, destino, distancia, carga=0):
        self.vehiculo = validar_vehiculo(vehiculo)
        self.origen = origen  
        self.destino = destino
        self.distancia = validar_positivo(distancia)
        self.carga = validar_positivo(carga)
        
        # Calcular tiempo y costo automáticamente
        self.tiempo = self._calcular_tiempo_decimal()
        self.costo = self._calcular_costo()
    
    def _calcular_tiempo_decimal(self):
        """Usa el método del vehículo para calcular tiempo"""
        return self.vehiculo.calcular_tiempo_decimal(self.distancia)
    
    def _calcular_costo(self):
        """Usa el método del vehículo para calcular costo"""
        return self.vehiculo.calcular_costo_tramo(self.distancia, self.carga)
    
    def _obtener_nombre_nodo(self, nodo):
        """Extrae el nombre del nodo"""
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

class Itinerario:
    """Plan de viaje completo"""
    
    def __init__(self, kpi_usado="tiempo"):
        validar_texto(kpi_usado)
        if kpi_usado not in ["tiempo", "costo"]:
            raise ValueError("KPI debe ser 'tiempo' o 'costo'")
        
        self.tramos = []
        self.costo_total = 0.0
        self.tiempo_total = 0.0
        self.kpi_usado = kpi_usado
    
    def _obtener_nombre_nodo(self, nodo):
        """Extrae nombre del nodo"""
        if hasattr(nodo, 'nombre'):  
            return nodo.nombre
        return str(nodo)  
    
    def agregar_tramo(self, tramo):
        """Agrega un tramo al itinerario"""
        if not isinstance(tramo, Tramo):
            raise TypeError("Debe ser un tramo válido")
        
        # Verificar continuidad
        if self.tramos:
            ultimo_destino = self._obtener_nombre_nodo(self.tramos[-1].destino)
            nuevo_origen = self._obtener_nombre_nodo(tramo.origen)
            if nuevo_origen != ultimo_destino:
                raise ValueError(f"Tramo no es continuo. Último destino: {ultimo_destino}, Nuevo origen: {nuevo_origen}")
        
        # Evitar ciclos
        if self._tiene_ciclo_basico(tramo):
            destino_nombre = self._obtener_nombre_nodo(tramo.destino)
            raise ValueError(f"Ciclo detectado: nodo {destino_nombre} ya visitado")
        
        self.tramos.append(tramo)
        self.calcular_totales()
    
    def _tiene_ciclo_basico(self, nuevo_tramo):
        """Verifica que no regrese a un nodo ya visitado"""
        nodos_visitados = set()
        
        # Agregar nodos ya visitados
        for tramo in self.tramos:
            nodos_visitados.add(self._obtener_nombre_nodo(tramo.origen))
        
        # Agregar último destino si hay tramos
        if self.tramos:
            nodos_visitados.add(self._obtener_nombre_nodo(self.tramos[-1].destino))
        
        # Verificar si el nuevo destino ya fue visitado
        nuevo_destino = self._obtener_nombre_nodo(nuevo_tramo.destino)
        return nuevo_destino in nodos_visitados
    
    def calcular_totales(self):
        """Recalcula totales"""
        self.costo_total = sum(tramo.costo for tramo in self.tramos)
        self.tiempo_total = sum(tramo.tiempo for tramo in self.tramos)
    
    def obtener_distancia_total(self):
        """Suma todas las distancias"""
        return sum(tramo.distancia for tramo in self.tramos)
    
    def obtener_carga_total(self):
        """Suma toda la carga transportada"""
        return sum(tramo.carga for tramo in self.tramos)
    
    def obtener_ruta_completa(self):
        """Lista de nodos en la ruta"""
        if not self.tramos:
            return []
        
        ruta = [self._obtener_nombre_nodo(self.tramos[0].origen)]
        for tramo in self.tramos:
            ruta.append(self._obtener_nombre_nodo(tramo.destino))
        return ruta
    
    def obtener_vehiculos_utilizados(self):
        """Tipos de vehículos usados"""
        return [tramo.vehiculo.modo_de_transporte for tramo in self.tramos]
    
    def obtener_tiempo_total_formateado(self):
        """Tiempo total en formato legible"""
        return tiempo_a_string(self.tiempo_total)
    
    def obtener_resumen_kpi(self):
        """Valor del KPI optimizado"""
        if self.kpi_usado == "tiempo":
            return f"{self.obtener_tiempo_total_formateado()}"
        else:
            return f"${self.costo_total:.2f}"
    
    def __str__(self):
        if not self.tramos:
            return "Itinerario vacío"
        
        resultado = "=" * 50
        resultado += f"\nITINERARIO DE TRANSPORTE\n"
        resultado += "=" * 50
        resultado += f"\nCriterio: {self.kpi_usado.upper()}\n"
        resultado += f"Ruta: {' -> '.join(self.obtener_ruta_completa())}\n"
        resultado += f"\nDETALLE DE TRAMOS:\n"
        resultado += "-" * 50
        
        for i, tramo in enumerate(self.tramos, 1):
            resultado += f"\n{i}. {tramo}"
        
        resultado += f"\n\nRESUMEN:\n"
        resultado += "-" * 50
        resultado += f"\nTramos: {len(self.tramos)}"
        resultado += f"\nDistancia total: {self.obtener_distancia_total():.1f} km"
        resultado += f"\nCarga total: {self.obtener_carga_total():.1f} kg"
        resultado += f"\nTiempo total: {self.obtener_tiempo_total_formateado()}"
        resultado += f"\nCosto total: ${self.costo_total:.2f}"
        resultado += f"\nVehículos: {', '.join(set(self.obtener_vehiculos_utilizados()))}"
        resultado += f"\nKPI ({self.kpi_usado}): {self.obtener_resumen_kpi()}"
        resultado += "\n" + "=" * 50
        
        return resultado
    
    def __repr__(self):
        return f"Itinerario(tramos={len(self.tramos)}, kpi='{self.kpi_usado}', costo=${self.costo_total:.2f}, tiempo={self.tiempo_total:.1f}h)"

if __name__ == "__main__":
    print("Probando sistema de itinerarios...")
    
    try:
        from vehiculos import Camion, Tren
        
        # Crear vehículos
        camion = Camion()
        tren = Tren()
        
        # Crear nodos
        ba = Nodo("Buenos_Aires")
        rosario = Nodo("Rosario")
        cordoba = Nodo("Cordoba")
        
        print("Vehículos:")
        print(f"- {camion.modo_de_transporte}: {camion.velocidad_nominal} km/h")
        print(f"- {tren.modo_de_transporte}: {tren.velocidad_nominal} km/h")
        
        print(f"\nNodos:")
        print(f"- {ba}")
        print(f"- {rosario}")
        print(f"- {cordoba}")
        
        # Crear itinerario optimizado por tiempo
        print(f"\nItinerario por TIEMPO:")
        itinerario_tiempo = Itinerario(kpi_usado="tiempo")
        
        tramo1 = Tramo(camion, ba, rosario, 300, 15000)
        tramo2 = Tramo(tren, rosario, cordoba, 400, 80000)
        
        print(f"Agregando: {tramo1}")
        itinerario_tiempo.agregar_tramo(tramo1)
        
        print(f"Agregando: {tramo2}")
        itinerario_tiempo.agregar_tramo(tramo2)
        
        print(f"\n{itinerario_tiempo}")
        
        # Itinerario por costo
        print(f"\nItinerario por COSTO:")
        itinerario_costo = Itinerario(kpi_usado="costo")
        
        tramo1_costo = Tramo(tren, ba, rosario, 300, 15000)
        tramo2_costo = Tramo(tren, rosario, cordoba, 400, 80000)
        
        itinerario_costo.agregar_tramo(tramo1_costo)
        itinerario_costo.agregar_tramo(tramo2_costo)
        
        print(f"\n{itinerario_costo}")
        
        # Comparación
        print(f"\nCOMPARACIÓN:")
        print("="*50)
        print(f"TIEMPO - Duración: {itinerario_tiempo.obtener_tiempo_total_formateado()}, Costo: ${itinerario_tiempo.costo_total:.2f}")
        print(f"COSTO  - Duración: {itinerario_costo.obtener_tiempo_total_formateado()}, Costo: ${itinerario_costo.costo_total:.2f}")
        
        print("\nPruebas completadas")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()