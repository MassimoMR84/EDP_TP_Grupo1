class Planificador: 
    '''
    Clase princiapal, planifica intinerarios dependiendo del KPI para solicitudes de transporte 
    '''
    
    def __init__(self, red_transporte):
        '''
        Inicializa el planificador para una red de transportes que contiene nodos, conexiones y vehiculos
        '''
        self.red_transporte = red_transporte
        
    def 