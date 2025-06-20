from nodo import Nodo
from itinerario import Itinerario, Tramo
from vehiculos import Vehiculo, Camion, Tren, Barco, Avion

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
            return Tren(velocidad=conexion.valorRestriccion)
            
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
    
    def encontrar_ruta_optima(self, solicitud, kpi="costo"):
        """
        Devuelve:
        - mejor_itinerario (Itinerario): el más óptimo según el KPI
        - itinerarios_optimos_por_modo (dict[str, Itinerario]): los mejores por cada modo
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
        
        carga = solicitud.peso_kg
        
        modos_disponibles = list(self.vehiculos_disponibles)
        mejor_itinerario = None
        mejor_valor = float('inf')
        itinerarios_optimos_por_modo = {}
        
        for modo in modos_disponibles:
            rutas = self.buscar_rutas(nodo_origen, nodo_destino, modo)
            mejor_itinerario_por_modo = None
            mejor_valor_modo = float('inf')
            
            #Convertir rutas de nodos a itinerario
            for ruta in rutas:
                conexiones = []
                for i in range(len(ruta) - 1):
                    nodo_origen_tramo = ruta[i]
                    nodo_destino_tramo = ruta[i + 1]

                    # Buscar la conexión válida para ese tramo
                    for conexion in nodo_origen_tramo.conexiones:
                        if (conexion.destino == nodo_destino_tramo and 
                            conexion.tipo.lower() == modo.lower() and 
                            self._verificar_restricciones(conexion, carga)):
                            conexiones.append(conexion)
                            break

                #Construir todas las conexiones
                if len(conexiones) == len(ruta) - 1:
                    itinerario = self._construir_itinerario_con_conexiones(conexiones, carga, kpi)
                    valor_kpi = itinerario.tiempo_total if kpi == "tiempo" else itinerario.costo_total

                    #Analiza para cada modo si su valor segun el kpi es el mejor
                    if valor_kpi < mejor_valor_modo:
                        mejor_valor_modo = valor_kpi
                        mejor_itinerario_por_modo = itinerario
                        
            if mejor_itinerario_por_modo:
                itinerarios_optimos_por_modo[modo] = mejor_itinerario_por_modo
                
                #Analizo si es el mejor entre todos los modos posibles
                if mejor_valor_modo < mejor_valor:
                    mejor_valor = mejor_valor_modo
                    mejor_itinerario = mejor_itinerario_por_modo
                        

        return mejor_itinerario, itinerarios_optimos_por_modo
    
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
            aux,_ = self.encontrar_ruta_optima(solicitud,kpi)
            return aux
        except Exception as e:
            print(f"Error generando itinerario: {e}")
            return None
        
    def optimos_por_modo(self, solicitud, kpi='tiempo'):
        try: 
            _,dicc = self.encontrar_ruta_optima(solicitud,kpi)
            return dicc
        except Exception as e:
            print(f"Error generando itinerario: {e}")
            return None
