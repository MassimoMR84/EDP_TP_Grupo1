'''Validaciones de datos'''
def validar_numero(dato):
    '''
    Valida que el dato sea un numero (int o float)
    Lanza un error si no lo es
    '''
    if not isinstance(dato, (float, int)):
        raise TypeError('Tipo de dato no valido. Debe ser de tipo float')

def validar_numero_positivo(dato):
    '''
    Valida que un numero sea positivo (mayor o igual a cero)
    Reutiliza validar_numero
    '''
    #valido que sea un dato del tipo float o int
    validar_numero(dato)
    #valido que sea positivo
    if dato < 0:
        raise ValueError('Tipo de dato no valido. Debe ser un numero positivo.')

def validar_numero_mayor_a_cero(dato):
    '''
    Valida que un numero sea estrictamente mayor a cero
    Reutiliza validar_numero_positivo
    '''
    validar_numero_positivo(dato)
    if dato == 0:
        raise ValueError('Numero debe ser estrictamente mayor a cero')
    
def validar_cadena(dato):
    '''
    Valida que el dato sea una cadena de texto str
    '''
    if not isinstance(dato, str):
        raise TypeError('Tipo de dato no valido. Debe ser una cadena de texto.')
    
def validar_division_por_cero(denominador):
    '''
    Lanza un error si el denominador de una division es cero
    '''
    validar_numero_positivo(denominador)
    if denominador == 0:
        raise ValueError('No se puede dividir por 0')


'''Validaciones clase Vehiculos'''
def validar_modo_de_transporte(modo_de_transporte):
    '''
    Valida que el modo de transporte sea valido 
    (este dentro de los modos aceptados: automotor, ferroviaria, aerea, fluvial)
    '''
    #valido que sea del tipo cadena
    validar_cadena(modo_de_transporte)
    #valido que sea un modo valido
    if modo_de_transporte.strip().lower() not in ['automotor', 'ferroviaria', 'aerea', 'fluvial']:
        raise ValueError('Modo de transporte no valido. Debe ser: automotor, ferroviaria, aerea o fluvial.')