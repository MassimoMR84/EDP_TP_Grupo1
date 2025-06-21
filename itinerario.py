from validaciones import *
from funciones_auxiliares import *
from tramo import Tramo

class Itinerario:
    """
    Plan de viaje completo con validaciones de continuidad y anti-ciclos.
    Mantiene métricas totales y información del KPI usado.
    """
    
    # CORREGIDO: Acepta parámetro carga_solicitud que usa el planificador
    def __init__(self, kpi_usado="tiempo", carga_solicitud=0):
        validar_texto(kpi_usado)
        if kpi_usado not in ["tiempo", "costo"]:
            raise ValueError("KPI debe ser 'tiempo' o 'costo'")
        
        self.tramos = []
        self.costo_total = 0.0
        self.tiempo_total = 0.0
        self.kpi_usado = kpi_usado
        self.carga_solicitud = validar_positivo(carga_solicitud)
    
    def _obtener_nombre_nodo(self, nodo):
        """Extrae nombre del nodo de forma robusta"""
        if hasattr(nodo, 'nombre'):  
            return nodo.nombre
        return str(nodo)  
    
    def agregar_tramo(self, tramo):
        """
        Agrega tramo con validaciones:
        - Continuidad geográfica
        - Prevención de ciclos
        - Recálculo de totales
        """
        if not isinstance(tramo, Tramo):
            raise TypeError("Debe ser un tramo válido")
        
        # Verificar continuidad con tramo anterior
        if self.tramos:
            ultimo_destino = self._obtener_nombre_nodo(self.tramos[-1].destino)
            nuevo_origen = self._obtener_nombre_nodo(tramo.origen)
            if nuevo_origen != ultimo_destino:
                raise ValueError(f"Tramo no es continuo. Último destino: {ultimo_destino}, Nuevo origen: {nuevo_origen}")
        
        # Evitar ciclos básicos
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
        """Recalcula totales sumando todos los tramos"""
        #Calcular costo total
        self.costo_total = 0
        
        #Sumamos los costos varibles por tramo
        self.costo_total += sum(tramo.costo for tramo in self.tramos)
        
        #Sumamos los costos de carga por transportar
        self.costo_total += self.tramos[0].vehiculo.calcular_costo_por_carga(self.carga_solicitud)
        
        #Calcular tiempo total
        self.tiempo_total = sum(tramo.tiempo for tramo in self.tramos)
    
    def obtener_distancia_total(self):
        """Suma todas las distancias"""
        return sum(tramo.distancia for tramo in self.tramos)
    
    def obtener_carga_total(self):
        """Suma toda la carga transportada"""
        return sum(tramo.carga for tramo in self.tramos)
    
    def obtener_ruta_completa(self):
        """Lista de nodos en orden de visita"""
        if not self.tramos:
            return []
        
        ruta = [self._obtener_nombre_nodo(self.tramos[0].origen)]
        for tramo in self.tramos:
            ruta.append(self._obtener_nombre_nodo(tramo.destino))
        return ruta
    
    def obtener_vehiculos_utilizados(self):
        """Lista de tipos de vehículos usados"""
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
        
        # Mostrar carga de la solicitud si está disponible
        if self.carga_solicitud > 0:
            resultado += f"Carga: {self.carga_solicitud} kg\n"
            
        resultado += f"\nDETALLE DE TRAMOS:\n"
        resultado += "-" * 50
        
        for i, tramo in enumerate(self.tramos, 1):
            resultado += f"\n{i}. {tramo}"
        
        resultado += f"\n\nRESUMEN:\n"
        resultado += "-" * 50
        resultado += f"\nTramos: {len(self.tramos)}"
        resultado += f"\nDistancia total: {self.obtener_distancia_total():.1f} km"
        resultado += f"\nCarga total: {self.obtener_carga_total():.1f} kg"
        if self.carga_solicitud > 0:
            resultado += f"\nCarga de la solicitud: {self.carga_solicitud:.1f} kg"
        resultado += f"\nTiempo total: {self.obtener_tiempo_total_formateado()}"
        resultado += f"\nCosto total: ${self.costo_total:.2f}"
        resultado += f"\nVehículos: {', '.join(set(self.obtener_vehiculos_utilizados()))}"
        resultado += f"\nKPI ({self.kpi_usado}): {self.obtener_resumen_kpi()}"
        resultado += "\n" + "=" * 50
        
        return resultado
    
    def __repr__(self):
        return f"Itinerario(tramos={len(self.tramos)}, kpi='{self.kpi_usado}', costo=${self.costo_total:.2f}, tiempo={self.tiempo_total:.1f}h)"