def validar_numero(dato):
    """Verifica que sea un número válido (int o float)"""
    if not isinstance(dato, (int, float)):
        raise TypeError('Debe ser un número')
    return dato


def validar_positivo(dato):
    """Verifica que sea positivo o cero (>= 0)"""
    validar_numero(dato)
    if dato < 0:
        raise ValueError('Debe ser positivo')
    return dato  


def validar_mayor_cero(dato):
    """Verifica que sea estrictamente mayor a cero (> 0)"""
    validar_positivo(dato)
    if dato == 0:
        raise ValueError('Debe ser mayor a cero')
    return dato


def validar_texto(dato):
    """Verifica que sea una cadena de texto válida"""
    if not isinstance(dato, str):
        raise TypeError('Debe ser texto')
    return dato


def validar_division_cero(denominador):
    """Previene divisiones por cero en cálculos"""
    if denominador == 0:
        raise ValueError('No se puede dividir por cero')
    return denominador


def validar_modo_transporte(modo):
    """
    Valida y normaliza modos de transporte.
    Acepta variaciones y sinónimos, retorna valores estándar.
    """
    modo = validar_texto(modo).strip().lower()
    
    # Mapeo para normalización (acepta variaciones)
    modos_validos = {
        'automotor': 'automotor',
        'ferroviaria': 'ferroviaria', 
        'aerea': 'aerea',
        'aereo': 'aerea',  # Sin tilde
        'fluvial': 'fluvial',
        'maritimo': 'maritimo',
        'marítimo': 'maritimo'  # Con tilde
    }
    
    if modo not in modos_validos:
        modos_disponibles = list(set(modos_validos.values()))
        raise ValueError(f'Modo inválido. Usar: {modos_disponibles}')
    
    return modos_validos[modo]


def validar_vehiculo(vehiculo): 
    """Verifica que sea una instancia válida de Vehículo"""
    # Importación tardía para evitar dependencias circulares
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
    """Verifica que sea una instancia válida de Nodo"""
    from nodo import Nodo
    if not isinstance(nodo, Nodo):
        raise TypeError("Debe ser un nodo")
    return nodo


# Validaciones específicas para restricciones

def validar_velocidad(valor):
    """Valida restricción de velocidad máxima"""
    if valor is None:
        return None
    try:
        velocidad = float(valor)
        return validar_positivo(velocidad)
    except (ValueError, TypeError):
        raise ValueError("Velocidad debe ser un número positivo")


def validar_peso(valor):
    """Valida restricción de peso máximo"""
    if valor is None:
        return None
    try:
        peso = float(valor)
        return validar_positivo(peso)
    except (ValueError, TypeError):
        raise ValueError("Peso debe ser un número positivo")


def validar_tipo_barco(valor):
    """Valida tipo de navegación (fluvial/marítimo)"""
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
    """
    Dispatcher que valida restricciones según su tipo.
    Delega a validadores específicos.
    """
    if restriccion is None or valor is None:
        return valor
        
    restriccion = restriccion.strip().lower()
    
    # Dispatch a validador específico
    if restriccion == 'velocidad_max':
        return validar_velocidad(valor)
    elif restriccion == 'peso_max':
        return validar_peso(valor)
    elif restriccion == 'tipo':
        return validar_tipo_barco(valor)
    elif restriccion == 'prob_mal_tiempo':
        return validar_probabilidad(valor)
    else:
        # Restricción no reconocida: permitir para extensibilidad
        return valor


# Código de prueba
if __name__ == "__main__":
    print("Probando validaciones...")
    
    # Probar modos de transporte
    print("\n=== Validación de Modos ===")
    modos_test = ['Automotor', 'Ferroviaria', 'Aerea', 'Fluvial', 'maritimo']
    
    for modo in modos_test:
        try:
            resultado = validar_modo_transporte(modo)
            print(f"✓ {modo} -> {resultado}")
        except ValueError as e:
            print(f"✗ {modo}: {e}")
    
    # Probar restricciones específicas
    print("\n=== Validación de Restricciones ===")
    try:
        print(f"✓ Velocidad 80: {validar_velocidad('80')}")
        print(f"✓ Peso 15000: {validar_peso('15000')}")
        print(f"✓ Tipo fluvial: {validar_tipo_barco('fluvial')}")
        print(f"✓ Probabilidad 0.3: {validar_probabilidad('0.3')}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Casos de error esperados
    print("\n=== Casos de Error ===")
    try:
        validar_mayor_cero(0)
    except ValueError as e:
        print(f"✓ Error esperado: {e}")
    
    try:
        validar_probabilidad(1.5)
    except ValueError as e:
        print(f"✓ Error esperado: {e}")
    
    try:
        validar_modo_transporte("submarino")
    except ValueError as e:
        print(f"✓ Error esperado: {e}")
    
    print("\n=== Pruebas completadas ===")