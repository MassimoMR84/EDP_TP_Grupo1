from nodo import Nodo

class Planificador: 
    '''
    Clase princiapal, planifica intinerarios dependiendo del KPI para solicitudes de transporte 
    '''   
    
    def __init__(self, red_transporte):
        '''
        Inicializa el planificador para una red de transportes que contiene nodos, conexiones y vehiculos
        '''
        self.red_transporte = red_transporte
        
    def buscar_rutas(self, nodo_actual, destino, modo, recorrido=None):
        """
        Devuelve todas las rutas posibles entre nodo_actual y destino,
        usando solo conexiones del tipo `modo`, sin repetir nodos.
        """
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

    
    
    
    def evaluar_ruta(ruta, peso_carga, kpi):
        pass
    
    def generar_itinerario(solicitud, kpi):
        pass
    
    
    