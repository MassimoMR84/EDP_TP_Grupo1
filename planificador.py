from nodo import Nodo
from itinerario import Itinerario, Tramo
from vehiculos import Vehiculo, Camion, Tren, Barco, Avion
import heapq

class Planificador: 
    """Planifica itinerarios optimizados según diferentes KPIs"""   
    
    def __init__(self, red_transporte):
        """Inicializa el planificador con una red de transporte"""
        self.red_transporte = red_transporte
        
        # Mapeo de tipos de vehículos
        self.tipos_vehiculos = {
            'ferroviaria': Tren,
            'automotor': Camion,
            'fluvial': Barco,
            'aerea': Avion
        }
        self.vehiculos_disponibles = self.tipos_vehiculos
        
    def _crear_vehiculo_para_conexion(self, conexion):
        """Crea vehículo específico según conexión y restricciones"""
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
        """Busca todas las rutas posibles entre nodos usando un modo específico"""
        if recorrido is None:
            recorrido = []

        recorrido = recorrido + [nodo_actual]

        if nodo_actual == destino:
            return [recorrido]

        caminos = []
        for conexion in nodo_actual.conexiones:
            if conexion.tipo.lower() == modo.lower():
                siguiente_nodo = conexion.destino
                if siguiente_nodo not in recorrido:
                    nuevos_caminos = self.buscar_rutas(siguiente_nodo, destino, modo, recorrido)
                    caminos.extend(nuevos_caminos)

        return caminos

    def encontrar_ruta_optima(self, solicitud, kpi="tiempo"):
        """Encuentra la ruta óptima usando Dijkstra"""
        origen_nombre = solicitud.origen if isinstance(solicitud.origen, str) else solicitud.origen.nombre
        destino_nombre = solicitud.destino if isinstance(solicitud.destino, str) else solicitud.destino.nombre
        
        # Buscar nodos en la red
        nodo_origen = None
        nodo_destino = None
        
        for nodo in self.red_transporte.nodos.values():
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
                    itinerario = self._construir_itinerario_con_conexiones(ruta_conexiones, solicitud.peso_kg, kpi)
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
        """Implementación de Dijkstra que retorna conexiones utilizadas"""
        # Verificar que origen tenga conexiones del modo especificado
        tiene_conexion_origen = any(conexion.tipo.lower() == modo.lower() 
                                  for conexion in origen.conexiones)
        if not tiene_conexion_origen:
            return None
        
        distancias = {origen: 0}
        predecesores = {origen: None}
        conexiones_usadas = {origen: None}
        visitados = set()
        heap = [(0, origen)]
        
        while heap:
            distancia_actual, nodo_actual = heapq.heappop(heap)
            
            if nodo_actual in visitados:
                continue
                
            visitados.add(nodo_actual)
            
            if nodo_actual == destino:
                # Reconstruir ruta
                ruta_conexiones = []
                nodo = destino
                while conexiones_usadas[nodo] is not None:
                    ruta_conexiones.append(conexiones_usadas[nodo])
                    nodo = predecesores[nodo]
                return ruta_conexiones[::-1]
            
            for conexion in nodo_actual.conexiones:
                if (conexion.tipo.lower() == modo.lower() and 
                    conexion.destino not in visitados):
                    
                    # Verificar restricciones
                    if self._verificar_restricciones(conexion, peso_carga):
                        
                        # Crear vehículo para esta conexión
                        vehiculo_creado = False
                        try:
                            vehiculo = self._crear_vehiculo_para_conexion(conexion)
                            vehiculo_creado = True
                        except Exception as e:
                            print(f"Error creando vehículo para {conexion.tipo}: {e}")
                        
                        if vehiculo_creado:
                            # Calcular costo según KPI
                            costo_calculado = False
                            try:
                                if kpi == "tiempo":
                                    costo_tramo = vehiculo.calcular_tiempo_decimal(conexion.distancia)
                                else:
                                    costo_tramo = vehiculo.calcular_costo_tramo(conexion.distancia, peso_carga)
                                costo_calculado = True
                            except Exception as e:
                                print(f"Error calculando costo: {e}")
                            
                            if costo_calculado:
                                nueva_distancia = distancia_actual + costo_tramo
                                
                                if (conexion.destino not in distancias or 
                                    nueva_distancia < distancias[conexion.destino]):
                                    
                                    distancias[conexion.destino] = nueva_distancia
                                    predecesores[conexion.destino] = nodo_actual
                                    conexiones_usadas[conexion.destino] = conexion
                                    heapq.heappush(heap, (nueva_distancia, conexion.destino))
        
        return None
    
    def _verificar_restricciones(self, conexion, peso_carga):
        """Verifica si una carga puede usar una conexión"""
        if not conexion.restriccion:
            return True
            
        # Restricción de peso máximo para automotor
        if conexion.restriccion == "peso_max" and conexion.tipo.lower() == "automotor":
            try:
                peso_maximo = float(conexion.valorRestriccion)
                return peso_carga <= peso_maximo
            except (ValueError, TypeError):
                return True
                
        return True
    
    def _construir_itinerario_con_conexiones(self, conexiones, peso_carga, kpi):
        """Construye itinerario a partir de conexiones"""
        itinerario = Itinerario(kpi_usado=kpi)
        
        for conexion in conexiones:
            vehiculo = self._crear_vehiculo_para_conexion(conexion)
            
            tramo = Tramo(
                vehiculo=vehiculo,
                origen=conexion.origen,
                destino=conexion.destino,
                distancia=conexion.distancia,
                carga=peso_carga
            )
            itinerario.agregar_tramo(tramo)
                
        return itinerario
    
    def generar_itinerario(self, solicitud, kpi="tiempo"):
        """Método principal para generar itinerario óptimo"""
        try:
            return self.encontrar_ruta_optima(solicitud, kpi)
        except Exception as e:
            print(f"Error generando itinerario: {e}")
            return None
    
    def encontrar_todas_las_rutas(self, solicitud):
        """Encuentra todas las rutas posibles en todos los modos"""
        origen_nombre = solicitud.origen if isinstance(solicitud.origen, str) else solicitud.origen.nombre
        destino_nombre = solicitud.destino if isinstance(solicitud.destino, str) else solicitud.destino.nombre
        
        # Buscar nodos
        nodo_origen = None
        nodo_destino = None
        
        for nodo in self.red_transporte.nodos.values():
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
                for ruta in rutas_modo:
                    try:
                        # Convertir ruta de nodos a conexiones
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
                            itinerario = self._construir_itinerario_con_conexiones(conexiones, solicitud.peso_kg, "costo")
                            itinerarios_modo.append(itinerario)
                    except Exception:
                        # En caso de error, simplemente no agregar este itinerario
                        pass
                        
                if itinerarios_modo:
                    todas_las_rutas[modo] = itinerarios_modo
                    
        return todas_las_rutas

if __name__ == "__main__":
    print("Probando planificador...")
    print("Para probar completamente, ejecutar main.py con archivos CSV")
    print("El planificador maneja:")
    print("- Restricciones de velocidad (ferroviaria)")
    print("- Restricciones de peso (automotor)")
    print("- Tipos de barco (fluvial/marítimo)")
    print("- Probabilidades climáticas (aérea)")
    print("- Manejo de errores mejorado")