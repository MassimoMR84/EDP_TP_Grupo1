'''========== Validaciones de datos =========='''

def validar_numero(dato): 
    '''
    Valida que el dato sea un número (int o float)
    '''
    if not dato.isdigit():
        raise TypeError('Tipo de dato no valido. Debe ser de tipo int')
    return int (dato)

def validar_numero_positivo(dato): 
    '''
    Valida que un numero sea positivo (mayor o igual a cero)
    '''
    if validar_numero(dato) < 0:
        raise ValueError('Tipo de dato no valido. Debe ser un numero positivo.')
    return dato  

def validar_numero_mayor_a_cero(dato): 
    '''
    Valida que un numero sea estrictamente mayor a cero
    '''
    if validar_numero_positivo(dato) == 0:
        raise ValueError('Numero debe ser estrictamente mayor a cero')
    return dato

def validar_cadena(dato): 
    '''
    Valida que el dato sea una cadena de texto str
    '''
    if not isinstance(dato, str):
        raise TypeError('Tipo de dato no valido. Debe ser una cadena de texto.')
    return dato

def validar_division_por_cero(denominador):
    '''
    Lanza un error si el denominador de una division es cero
    '''
    if validar_numero_positivo(denominador) == 0:
        raise ValueError('No se puede dividir por 0')
    return denominador

'''========== Validaciones de clase Vehiculos =========='''

def validar_modo_de_transporte(modo_de_transporte): 
    '''
    Valida que el modo de transporte sea automotor, ferroviaria, aerea, fluvial
    '''
    if validar_cadena(modo_de_transporte).strip().lower() not in ['automotor', 'ferroviaria', 'aerea', 'fluvial']:
        raise ValueError('Modo de transporte no valido. Debe ser: automotor, ferroviaria, aerea o fluvial.')
    return modo_de_transporte.strip().lower()

def validar_vehiculo(vehiculo): 
    '''
    Valida que el vehiculo sea un objeto de tipo Vehiculo
    '''
    from vehiculos import Vehiculo  # ← Import dentro de la función
    if not isinstance(vehiculo, Vehiculo):
        raise TypeError("El vehiculo debe ser un objeto de tipo Vehiculo")
    return vehiculo

'''========== Validaciones de clase Solicitudes =========='''

def validar_origen_destino(origen, destino): 
    '''
    Valida que el origen y destino no sean iguales
    '''
    if origen == destino:
        raise ValueError("El origen y el destino no pueden ser iguales.")
    return origen, destino

'''========== Validaciones de clase Conexiones =========='''

def validarNodo(nodo):
    from nodo import Nodo  # ← Import dentro de la función
    if not isinstance(nodo, Nodo):
        raise TypeError("El origen y destino deben ser objetos de tipo Nodo")
    return nodo