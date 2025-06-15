from validaciones import *
#from vehiculos import *

class Conexion:
    '''Clase Conexión: contiene el nodo origen, el nodo destino, la distancia entre ellos, la restricción (si la hay) 
    y el valor de la restricción (si corresponde)'''

    
    def __init__(self, origen, destino, tipo: str, distancia: int, restriccion=None, valorRestriccion=None):
        self.origen = origen
        self.destino = destino
        self.tipo=tipo
        
        
        #comentario posible implementacion a mirar:
    
        '''
        tipo q me pasan es un str entonces:
        '''
        '''vlidar q tipo es un vehiculo'''
        ''' match tipo:
            case "avion":
                self.tipo = Avion(valorRestriccion)
            case "automotor":
                self.tipo = Camion()
            case "fluvial":
                self.tipo = Barco(valorRestriccion)
            case "ferroviaria":
                self.tipo = Tren()
            case _:
                raise ValueError("No esta en la lista")'''
        
               
        self.distancia = validar_numero_mayor_a_cero(distancia)
        self.restriccion = restriccion
        self.valorRestriccion = valorRestriccion

    def __str__ (self):
        base = f"Conexión de {self.origen} a {self.destino} ({self.tipo}): {self.distancia} km"
        if self.restriccion:
            base += f" | Restricción: {self.restriccion} = {self.valorRestriccion}"
        return base

    def __repr__(self): #! Poner mas corto e intuitivo
        if self.restriccion is None:
            return f"Origen:{self.origen}\nDestino:{self.destino}\nModo de transporte: {self.tipo}\nDistancia: {self.distancia}\nNo hay restricciones en esta conexion\n\n"
        else:
            return f"Origen:{self.origen}\nDestino:{self.destino}\nModo de transporte: {self.tipo}\nDistancia: {self.distancia}\n Restricción:{self.restriccion}\nValor restrictivo: {self.valorRestriccion}\n\n"

    def __eq__ (self, otra_conexion):
        '''Compara dos conexiones para ver si son iguales'''
        return (isinstance(otra_conexion, Conexion) 
                and self.origen == otra_conexion.origen 
                and self.destino == otra_conexion.destino 
                and self.tipo == otra_conexion.tipo)

    def aplica_restriccion(self, vehiculo): 
        '''Verifica si un vehículo cumple con las restricciones de la conexión'''
        if not self.restriccion:
            return True
        
        atributo = getattr(vehiculo, self.restriccion, None)
        if atributo is None:
            return False

        return atributo >= float(self.valorRestriccion)
        
        #AGREGAS RESTRICCION DEL PESO DE LOS CAMIONES