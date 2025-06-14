def validar_numero(dato):
    """Verifica que sea un número"""
    if not isinstance(dato, (int, float)):
        raise TypeError('Debe ser un número')
    return dato

def validar_positivo(dato):
    """Verifica que sea positivo (>= 0)"""
    validar_numero(dato)
    if dato < 0:
        raise ValueError('Debe ser positivo')
    return dato  

def validar_mayor_cero(dato):
    """Verifica que sea mayor a cero"""
    validar_positivo(dato)
    if dato == 0:
        raise ValueError('Debe ser mayor a cero')
    return dato

def validar_texto(dato):
    """Verifica que sea texto"""
    if not isinstance(dato, str):
        raise TypeError('Debe ser texto')
    return dato

def validar_division_cero(denominador):
    """Evita división por cero"""
    if denominador == 0:
        raise ValueError('No se puede dividir por cero')
    return denominador

def validar_modo_transporte(modo):
    """Valida modos de transporte válidos"""
    modo = validar_texto(modo).strip().lower()
    
    modos_validos = {
        'automotor': 'automotor',
        'ferroviaria': 'ferroviaria', 
        'aerea': 'aerea',
        'fluvial': 'fluvial',
        'maritimo': 'maritimo',
        'aereo': 'aerea',
        'marítimo': 'maritimo'
    }
    
    if modo not in modos_validos:
        raise ValueError(f'Modo inválido. Usar: {list(set(modos_validos.values()))}')
    
    return modos_validos[modo]

def validar_vehiculo(vehiculo): 
    """Verifica que sea un vehículo válido"""
    from vehiculos import Vehiculo
    if not isinstance(vehiculo, Vehiculo):
        raise TypeError("Debe ser un vehículo")
    return vehiculo

def validar_origen_destino(origen, destino): 
    """Verifica que origen y destino sean diferentes"""
    if origen == destino:
        raise ValueError("Origen y destino no pueden ser iguales")
    return origen, destino

def validar_nodo(nodo):
    """Verifica que sea un nodo válido"""
    from nodo import Nodo
    if not isinstance(nodo, Nodo):
        raise TypeError("Debe ser un nodo")
    return nodo

# Validaciones para restricciones específicas
def validar_velocidad(valor):
    """Valida restricción de velocidad"""
    if valor is None:
        return None
    try:
        velocidad = float(valor)
        return validar_positivo(velocidad)
    except (ValueError, TypeError):
        raise ValueError("Velocidad debe ser un número positivo")

def validar_peso(valor):
    """Valida restricción de peso"""
    if valor is None:
        return None
    try:
        peso = float(valor)
        return validar_positivo(peso)
    except (ValueError, TypeError):
        raise ValueError("Peso debe ser un número positivo")

def validar_tipo_barco(valor):
    """Valida tipo de barco"""
    if valor is None:
        return None
    tipo = validar_texto(valor).strip().lower()
    if tipo not in ['fluvial', 'maritimo']:
        raise ValueError("Tipo debe ser 'fluvial' o 'maritimo'")
    return tipo

def validar_probabilidad(valor):
    """Valida probabilidad entre 0 y 1"""
    if valor is None:
        return None
    try:
        prob = float(valor)
        if not 0 <= prob <= 1:
            raise ValueError("Probabilidad debe estar entre 0 y 1")
        return prob
    except (ValueError, TypeError):
        raise ValueError("Probabilidad debe ser un número entre 0 y 1")

def validar_restriccion_conexion(restriccion, valor):
    """Valida restricciones según su tipo"""
    if restriccion is None or valor is None:
        return valor
        
    restriccion = restriccion.strip().lower()
    
    if restriccion == 'velocidad_max':
        return validar_velocidad(valor)
    elif restriccion == 'peso_max':
        return validar_peso(valor)
    elif restriccion == 'tipo':
        return validar_tipo_barco(valor)
    elif restriccion == 'prob_mal_tiempo':
        return validar_probabilidad(valor)
    else:
        return valor

if __name__ == "__main__":
    print("Probando validaciones...")
    
    # Probar modos de transporte
    modos_test = ['Automotor', 'Ferroviaria', 'Aerea', 'Fluvial', 'maritimo']
    
    for modo in modos_test:
        try:
            resultado = validar_modo_transporte(modo)
            print(f"OK {modo} -> {resultado}")
        except ValueError as e:
            print(f"Error {modo}: {e}")
    
    # Probar restricciones
    try:
        print(f"Velocidad 80: {validar_velocidad('80')}")
        print(f"Peso 15000: {validar_peso('15000')}")
        print(f"Tipo fluvial: {validar_tipo_barco('fluvial')}")
        print(f"Probabilidad 0.3: {validar_probabilidad('0.3')}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("Pruebas completadas")