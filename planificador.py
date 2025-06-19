from nodo import Nodo
from itinerario import Itinerario, Tramo
from vehiculos import Vehiculo, Camion, Tren, Barco, Avion
import heapq

class Planificador: 
    """
    Planificador que optimiza itinerarios según tiempo o costo usando Dijkstra.
    Maneja restricciones específicas de cada tipo de conexión.
    """   
    
    def __init__(self, sistema_transporte):
        self.sistema_transporte = sistema_transporte
        
        # Mapeo de tipos de conexión a clases de vehículos
        self.tipos_vehiculos = {
            'ferroviaria': Tren,
            'automotor': Camion,
            'fluvial': Barco,
            'aerea': Avion
        }
        self.vehiculos_disponibles = self.tipos_vehiculos
        
    def _crear_vehiculo_para_conexion(self, conexion):
        """
        Crea vehículo específico adaptado a las restricciones de la conexión.
        """
        tipo = conexion.tipo.lower()
        
        if tipo == 'ferroviaria':
            vehiculo = Tren()
            # Aplicar restricción de velocidad si existe
            if conexion.restriccion == 'velocidad_max' and conexion.valorRestriccion:
                try:
                    velocidad_max = float(conexion.valorRestriccion)
                    if vehiculo.velocidad_nominal > velocidad_max:
                        vehiculo.velocidad_nominal = velocidad_max
                except (ValueError, TypeError):
                    pass
            return vehiculo
            
        elif tipo == 'automotor':
            return Camion()
            
        elif tipo == 'fluvial':
            # Determinar tipo según restricción
            tipo_barco = 'fluvial'
            if conexion.restriccion == 'tipo' and conexion.valorRestriccion:
                tipo_barco = conexion.valorRestriccion
            return Barco(tipo_barco)
            
        elif tipo == 'aerea':
            # Obtener probabilidad de mal tiempo
            prob_mal_tiempo = 0
            if conexion.restriccion == 'prob_mal_tiempo' and conexion.valorRestriccion:
                try:
                    prob_mal_tiempo = float(conexion.valorRestriccion)
                except (ValueError, TypeError):
                    prob_mal_tiempo = 0
            return Avion(prob_mal_tiempo) # type: ignore
            
        else:
            raise ValueError(f"Tipo de vehículo no reconocido: {tipo}")

    def buscar_rutas(self, nodo_actual, destino, modo, recorrido=None):
        """
        Busca todas las rutas posibles entre dos nodos usando búsqueda en profundidad.
        Evita ciclos manteniendo registro de nodos visitados.
        """
        if recorrido is None:
            recorrido = []

        recorrido = recorrido + [nodo_actual]

        # Caso base: llegamos al destino
        if nodo_actual == destino:
            return [recorrido]

        caminos = []
        for conexion in nodo_actual.conexiones:
            if conexion.tipo.lower() == modo.lower():
                siguiente_nodo = conexion.destino
                # Evitar ciclos
                if siguiente_nodo not in recorrido:
                    nuevos_caminos = self.buscar_rutas(siguiente_nodo, destino, modo, recorrido)
                    caminos.extend(nuevos_caminos)

        return caminos

    def encontrar_ruta_optima(self, solicitud, kpi="tiempo"):
        """
        Encuentra la ruta óptima probando todos los modos de transporte.
        Usa Dijkstra para cada modo y selecciona el mejor según KPI.
        """
        # Obtener nodos de origen y destino
        origen_nombre = solicitud.origen if isinstance(solicitud.origen, str) else solicitud.origen.nombre
        destino_nombre = solicitud.destino if isinstance(solicitud.destino, str) else solicitud.destino.nombre
        
        nodo_origen = None
        nodo_destino = None
        
        for nodo in self.sistema_transporte.nodos.values():
            if nodo.nombre == origen_nombre:
                nodo_origen = nodo
            if nodo.nombre == destino_nombre:
                nodo_destino = nodo
                
        if not nodo_origen or not nodo_destino:
            raise ValueError(f"Nodos no encontrados: {origen_nombre} o {destino_nombre}")
        
        mejores_rutas = {}
        
        # Probar cada modo de transporte
        modos_disponibles = ['Ferroviaria', 'Automotor', 'Fluvial', 'Aerea']
        for modo in modos_disponibles:
            try:
                ruta_conexiones = self._dijkstra(nodo_origen, nodo_destino, modo, solicitud.peso_kg, kpi)
                if ruta_conexiones:
                    # Pasar la carga real de la solicitud
                    itinerario = self._construir_itinerario_con_conexiones(
                        ruta_conexiones, solicitud.peso_kg, kpi)
                    mejores_rutas[modo] = itinerario
            except Exception as e:
                print(f"Error calculando ruta para {modo}: {e}")
                
        if not mejores_rutas:
            return None
            
        # Seleccionar mejor según KPI
        if kpi == "tiempo":
            mejor = min(mejores_rutas.values(), key=lambda x: x.tiempo_total)
        else:
            mejor = min(mejores_rutas.values(), key=lambda x: x.costo_total)
            
        return mejor
    
    def _dijkstra(self, origen, destino, modo, peso_carga, kpi):
        """
        Implementación de Dijkstra para encontrar camino óptimo.
        Usa cola de prioridad para eficiencia O((V+E) log V).
        """
        # Verificar que origen tenga conexiones del modo especificado
        tiene_conexion_origen = any(conexion.tipo.lower() == modo.lower() 
                                  for conexion in origen.conexiones)
        if not tiene_conexion_origen:
            return None
        
        # Estructuras para Dijkstra
        distancias = {origen: 0}
        predecesores = {origen: None}
        conexiones_usadas = {origen: None}
        visitados = set()
        heap = [(0, origen)]  # Cola de prioridad
        
        while heap:
            distancia_actual, nodo_actual = heapq.heappop(heap)
            
            if nodo_actual in visitados:
                continue
                
            visitados.add(nodo_actual)
            
            # Si llegamos al destino, reconstruir camino
            if nodo_actual == destino:
                ruta_conexiones = []
                nodo = destino
                while conexiones_usadas[nodo] is not None:
                    ruta_conexiones.append(conexiones_usadas[nodo])
                    nodo = predecesores[nodo]
                return ruta_conexiones[::-1]  # Invertir para orden correcto
            
            # Explorar conexiones adyacentes
            for conexion in nodo_actual.conexiones:
                if (conexion.tipo.lower() == modo.lower() and 
                    conexion.destino not in visitados):
                    
                    if self._verificar_restricciones(conexion, peso_carga):
                        try:
                            vehiculo = self._crear_vehiculo_para_conexion(conexion)
                            
                            # Calcular costo según KPI
                            if kpi == "tiempo":
                                costo_tramo = vehiculo.calcular_tiempo_decimal(conexion.distancia)
                            else:
                                # CORREGIDO: Usar método que existe
                                costo_tramo = vehiculo.calcular_costo_tramo(conexion.distancia, peso_carga)
                            
                            nueva_distancia = distancia_actual + costo_tramo
                            
                            # Actualizar si encontramos mejor camino
                            if (conexion.destino not in distancias or 
                                nueva_distancia < distancias[conexion.destino]):
                                
                                distancias[conexion.destino] = nueva_distancia
                                predecesores[conexion.destino] = nodo_actual
                                conexiones_usadas[conexion.destino] = conexion
                                heapq.heappush(heap, (nueva_distancia, conexion.destino))
                                
                        except Exception as e:
                            print(f"Error procesando conexión: {e}")
        
        return None
    
    def _verificar_restricciones(self, conexion, peso_carga):
        """
        Verifica si una carga puede usar una conexión específica.
        Principalmente maneja restricciones de peso máximo en automotor.
        """
        if not conexion.restriccion:
            return True
            
        # Restricción de peso máximo para conexiones automotrices
        if conexion.restriccion == "peso_max" and conexion.tipo.lower() == "automotor":
            try:
                peso_maximo = float(conexion.valorRestriccion)
                return peso_carga <= peso_maximo
            except (ValueError, TypeError):
                return True
                
        return True
    
    def _construir_itinerario_con_conexiones(self, conexiones, peso_carga, kpi):
        """
        Construye objeto Itinerario a partir de secuencia de conexiones.
        Pasa la carga real de la solicitud al itinerario.
        """
        # CORREGIDO: Usar constructor que acepta carga_solicitud
        itinerario = Itinerario(kpi_usado=kpi, carga_solicitud=peso_carga)
        
        for conexion in conexiones:
            vehiculo = self._crear_vehiculo_para_conexion(conexion)
            
            tramo = Tramo(
                vehiculo=vehiculo,
                origen=conexion.origen,
                destino=conexion.destino,
                distancia=conexion.distancia,
                carga=peso_carga  # Cada tramo lleva la carga completa
            )
            itinerario.agregar_tramo(tramo)
                
        return itinerario
    
    def generar_itinerario(self, solicitud, kpi="tiempo"):
        """
        Método principal para generar itinerario óptimo.
        Punto de entrada usado por otros módulos.
        """
        try:
            return self.encontrar_ruta_optima(solicitud, kpi)
        except Exception as e:
            print(f"Error generando itinerario: {e}")
            return None
    
    def encontrar_todas_las_rutas(self, solicitud):
        """
        Encuentra todas las rutas posibles en todos los modos de transporte.
        Útil para análisis y comparación de alternativas.
        """
        origen_nombre = solicitud.origen if isinstance(solicitud.origen, str) else solicitud.origen.nombre
        destino_nombre = solicitud.destino if isinstance(solicitud.destino, str) else solicitud.destino.nombre
        
        # Buscar nodos
        nodo_origen = None
        nodo_destino = None
        
        for nodo in self.sistema_transporte.nodos.values():
            if nodo.nombre == origen_nombre:
                nodo_origen = nodo
            if nodo.nombre == destino_nombre:
                nodo_destino = nodo
                
        if not nodo_origen or not nodo_destino:
            return {}
        
        todas_las_rutas = {}
        modos_disponibles = ['Ferroviaria', 'Automotor', 'Fluvial', 'Aerea']
        
        for modo in modos_disponibles:
            rutas_modo = self.buscar_rutas(nodo_origen, nodo_destino, modo)
            if rutas_modo:
                itinerarios_modo = []
                
                # Convertir rutas de nodos a itinerarios
                for ruta in rutas_modo:
                    try:
                        conexiones = []
                        for i in range(len(ruta) - 1):
                            nodo_origen_tramo = ruta[i]
                            nodo_destino_tramo = ruta[i + 1]
                            
                            # Buscar conexión correcta
                            for conexion in nodo_origen_tramo.conexiones:
                                if (conexion.destino == nodo_destino_tramo and 
                                    conexion.tipo.lower() == modo.lower() and
                                    self._verificar_restricciones(conexion, solicitud.peso_kg)):
                                    conexiones.append(conexion)
                                    break
                        
                        if len(conexiones) == len(ruta) - 1:
                            itinerario = self._construir_itinerario_con_conexiones(
                                conexiones, solicitud.peso_kg, "costo")
                            itinerarios_modo.append(itinerario)
                    except Exception:
                        pass  # Saltar rutas con errores
                        
                if itinerarios_modo:
                    todas_las_rutas[modo] = itinerarios_modo
                    
        return todas_las_rutas